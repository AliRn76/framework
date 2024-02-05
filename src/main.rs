mod tree;

use crate::tree::Tree;


fn clean_path(raw_path: &str) -> String {
    let mut path: String = String::new();
    // Remove Query Params
    for char in raw_path.chars() {
        if char == '?' { break; }
        path.push(char);
    }
    // Remove '/' suffix & prefix
    path.trim_end_matches('/').trim_start_matches('/').to_string()
}

fn find_endpoint(mut urls: Tree<&str, i32>, path: &str) -> (i32, String){
    let path: String = clean_path(path);
    let parts: Vec<&str> = path.split('/').collect();
    let parts_len: usize = parts.len();

    let mut found_path = String::new();
    for (i, part) in parts.iter().enumerate() {
        let last_path: bool = (i + 1) == parts_len;


        match urls.get(*part) {
            Some(found) => {
                if last_path && found.value == 10 {
                    found_path.push_str(part);
                    found_path.push('/');

                    println!("Found: {:?}", found.value);

                    return (found.value, found_path.to_string());
                }

                if found.value == 0 {
                    found_path.push_str(part);
                    found_path.push('/');

                    println!("Going Inside: {:?}", found);

                    match found.get("") {
                        Some(inner_found) => {
                            println!("Found Inside: {:?}", inner_found);

                            return (inner_found.value, part.to_string());
                        },
                        None => {
                            urls = found.clone();
                            continue
                        }
                    }
                }
            }
            None => {
                println!("Found is None: {:?}", part);
                return (10, "".to_string());
            }
        }
    }

    return (10, "".to_string());
}

fn main() {
    let mut urls: Tree<&str, i32> = Tree::new(0);
    let mut subtree_a = Tree::new(0);

    subtree_a.entry("<user_id>").or_insert(Tree::new(10));
    urls.entry("users").or_insert(subtree_a);

    let path = "users/<user_id>";
    let (endpoint, found_path) = find_endpoint(urls, path);

    println!("endpoint: {:?}", endpoint);
    println!("found_path: {:?}", found_path);
}
