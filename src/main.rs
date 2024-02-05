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

fn is_callable(value: i32) -> bool {
    value != 0
}

fn is_subtree(value: i32) -> bool {
    value == 0
}

fn push_path(mut path: String, part: &&str) -> String {
    path.push_str(part);
    path.push('/');
    path
}


fn find_endpoint(mut urls: Tree<&str, i32>, path: &str) -> (i32, String) {
    let endpoint_not_found: (i32, String) = (-1, "".to_string());

    let path: String = clean_path(path);
    let parts: Vec<&str> = path.split('/').collect();
    let parts_len: usize = parts.len();

    let mut found_path = String::new();
    for (i, part) in parts.iter().enumerate() {
        let last_path: bool = (i + 1) == parts_len;

        let borrowed_url = urls.clone();
        match urls.get(*part) {
            Some(found) => {
                if last_path && is_callable(found.value) {
                    println!("Found: {:?}", found.value);
                    found_path = push_path(found_path, part);
                    return (found.value, found_path.to_string());
                }
                if is_subtree(found.value) {
                    found_path = push_path(found_path, part);
                    match found.get("") {
                        Some(inner_found) => {
                            if last_path && is_callable(inner_found.value) {
                                println!("Found Inside: {:?}", inner_found);
                                return (inner_found.value, part.to_string());
                            }
                        }
                        None => {}
                    }
                    urls = found.clone();
                    continue;
                }
            }
            None => {
                for (key, value) in borrowed_url
                    .iter()
                    .filter_map(|(p, q)| {
                        if !p.is_empty() && p.get(0).unwrap().starts_with('<') {
                            Some((p.get(0).unwrap().clone(), q))
                        } else { None }
                    })
                {
                    println!("{:?}={:?}", key, value);
                    let found = urls.get(key).unwrap();

                    if last_path {
                        if is_callable(found.value) {
                            println!("Found <>: {:?}", found.value);

                            found_path = push_path(found_path, key);
                            return (found.value, found_path.to_string());
                        }
                        if is_subtree(found.value) {
                            found_path = push_path(found_path, key);

                            match found.get("") {
                                Some(inner_found) => {
                                    if last_path && is_callable(inner_found.value) {
                                        println!("Found Inside <>: {:?}", inner_found);
                                        return (inner_found.value, key.to_string());
                                    }
                                }
                                None => {}
                            }
                            urls = found.clone();
                            break;
                        }
                        return endpoint_not_found;
                    } else if is_subtree(found.value) {
                        urls = found.clone();
                        found_path = push_path(found_path, key);
                        break;
                    } else {
                        return endpoint_not_found;
                    }
                }
            }
        }
    }

    return endpoint_not_found;
}

fn main() {
    let mut urls: Tree<&str, i32> = Tree::new(0);
    let mut subtree_a = Tree::new(0);
    let mut subtree_b = Tree::new(0);

    subtree_b.entry("").or_insert(Tree::new(11));
    subtree_b.entry("ali").or_insert(Tree::new(12));

    subtree_a.entry("<user_id>").or_insert(subtree_b);
    subtree_a.entry("login").or_insert(Tree::new(13));
    urls.entry("users").or_insert(subtree_a);

    let path = "users/<user_id>";
    let (endpoint, found_path) = find_endpoint(urls, path);

    if found_path == "" {
        println!("\nNonFound.")
    } else {
        println!("\nFound: {}", endpoint)
    }
}
