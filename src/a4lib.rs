use std::collections::HashMap;
use std::rc::Rc;
use pyo3::prelude::*;
use pyo3::PyResult;
use pyo3::types::PyDict;
use std::sync::OnceLock;
use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

static ROUTES: OnceLock<Url> = OnceLock::new();

#[derive(Debug, Clone)]
#[pyclass(module = "routing")]
pub struct Url {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub handler: Option<Py<PyAny>>,
    #[pyo3(get)]
    pub inner: HashMap<String, Url>,
}

impl Url {
    /// Recursively parses a PyAny (expected to be a dict or a leaf handler)
    /// into a Url node with the given name.
    fn from_pyany(py: Python, obj: &PyAny, name: String) -> PyResult<Self> {
        let mut url = Url {
            name,
            handler: None,
            inner: HashMap::new(),
        };

        // If the object is a dictionary, then process its items.
        if let Ok(dict) = obj.downcast::<PyDict>() {
            for (key_obj, value) in dict {
                // We expect the key to be a string.
                let key: &str = key_obj.extract()?;
                if key.is_empty() {
                    // An empty key means this node’s handler.
                    url.handler = Some(value.into());
                } else {
                    // Parse the child node: if value is a dict, parse recursively;
                    // otherwise, assume it is a leaf handler.
                    let mut child = if value.is_instance(py.get_type::<PyDict>())? {
                        Url::from_pyany(py, value, key.to_string())?
                    } else {
                        Url {
                            name: key.to_string(),
                            handler: Some(value.into()),
                            inner: HashMap::new(),
                        }
                    };

                    // If the key is a parameter (e.g. "<user_id>"), store it in `param`.
                    if key.starts_with('<') && key.ends_with('>') {
                        if url.inner.contains_key("param") {
                            return Err(PyValueError::new_err(
                                "Multiple parameterized routes at the same level",
                            ));
                        }
                        // Remove the angle brackets for the parameter name.
                        let param_name = key.trim_start_matches('<').trim_end_matches('>').to_string();
                        child.name = param_name;
                        url.inner.insert("param".to_string(), child);
                        // url.param = Some((param_name, Box::new(child)));
                    } else {
                        // Otherwise, insert it as a static inner route.
                        url.inner.insert(key.to_string(), child);
                    }
                }
            }

            // println!("the url struct: {:?}", url);
            Ok(url)
        } else {
            // If the object is not a dictionary, treat it as a handler for a leaf node.
            url.handler = Some(obj.into());
            // println!("the url struct: {:?}", url);
            Ok(url)
        }
    }

    fn get(&self, endpoint: String) -> Option<(String, Option<Py<PyAny>>)> {
        let parts: Vec<&str> = endpoint.split('/').filter(|s| !s.is_empty()).collect();
        let mut inner: &HashMap<String, Url> = &self.inner;
        let mut result = "".to_owned();
        for part in parts.iter() {
            let res = inner.get(*part);
            match res {
                Some(x) => {
                    result += &("/".to_owned() + &x.name);
                    if x.name == *parts.last().unwrap() {
                        return Some((result, x.handler.clone()))
                    }else{
                        inner = &x.inner;
                    }
                },
                None => {
                    let resp = inner.get("param");
                    match resp {
                        Some(x) => {
                            result += &("/".to_owned() + &x.name);
                            if x.name == *parts.last().unwrap() {
                                return Some((result, x.handler.clone()))
                            }else{
                                inner = &x.inner;
                            }
                        },
                        None => {
                            return None
                        },
                    }
                },
            }
        }
        None
    }
}

#[pyfunction]
pub fn get(py: Python, a: &Url, e: String) -> Option<(String, Option<Py<PyAny>>)> {
    a.get(e)
}
// Example wrapper function that takes a PyAny and returns a Url (the root node).
#[pyfunction]
pub fn parse_urls(py: Python, obj: &PyAny) -> PyResult<Url> {
    // We use an empty string for the root node name.
    Url::from_pyany(py, obj, "".to_string())
}

/// Module definition
#[pymodule]
fn routing(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Url>()?;
    m.add_function(wrap_pyfunction!(parse_urls, m)?)?;
    Ok(())
}
// because we can have only 1 param in 1 path
// for that the key is param
// #[pyclass(module = "routing")]
// pub struct Url {
//     name: String,
//     handler: Option<Py<PyAny>>,
//     inner: HashMap<String, Url>,
//     param: Option<(String,Box<Url>)>,
// }
//
// struct UrlResult {
//     path: String,
//     handlr: Option<Py<PyAny>>,
// }
//
// #[pymethods]
// impl Url {
//     fn get(&self, path: String) -> Option<UrlResult> {
//         let parts: Vec<&str> = path.split('/').filter(|s| !s.is_empty()).collect();
//         if parts.is_empty() {
//             return Some(UrlResult{path:"/".to_owned(), handlr: self.handler.clone()});
//         }
//         let mut res = UrlResult{path: "/".to_owned(), handlr: None};
//         self.find(&mut res,parts.last().unwrap() ,parts);
//         Some(res)
//     }
//
//     fn find(&self, res: &mut UrlResult, end: &str, x: Vec<&str>) {
//         if x.is_empty() { //this means we are in /
//             res.handlr = self.handler.clone();
//             return;
//         }
//         match self.inner.get(x[0]) {
//             Some(v) => {
//                 if v.name == *end {
//                     res.handlr = self.handler.clone();
//                     return;
//                 }
//                 res.path += &("/".to_owned() + &self.name);
//                 self.find(res, end, (x[1..]).to_vec());
//             },
//             None => {
//                 if x[0] == end {
//                     res.path += &("/".to_owned() + &self.name);
//                     res.handlr = self.handler.clone();
//                     return;
//                 }
//                 res.path += &("/".to_owned() + &self.name);
//                 self.find(res, end, (x[1..]).to_vec());
//             },
//         }
//     }
//
//     #[new]
//     fn parse_urls_dict(urls: &PyDict) -> PyResult<Self> {
//         let pydata: &PyDict = urls.downcast()?;
//         let mut res = Url{
//             name: "/".to_owned(),
//             handler: None,
//             inner: HashMap::new(),
//             param: None,
//         };
//         fn create(res: &mut Url, pd: &PyDict) {
//             for (k,v) in pd.into_iter() {
//                 let key = k.extract::<String>().unwrap();
//                 let mut new_url = Url{
//                     name: k.to_string(),
//                     handler: None,
//                     inner: HashMap::new(),
//                     param: None,
//                 };
//                 if v.is_exact_instance_of::<PyDict>() {
//                     todo!();
//                 } else {
//                     new_url.handler = Some(v.into());
//                 }
//             }
//         }
//         create(&mut res, pydata);
//         todo!()
//     }
// }

fn is_param(s: String) -> bool {
    if s.starts_with('<') && s.ends_with('>') {
        // Some(s[1..s.len()-1].to_string())
        true
    }else{
        false
    }
}

fn init() {}
