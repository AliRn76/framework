mod tree;

use crate::tree::Tree;

fn find() {}

fn main() {
    let mut tree: Tree<&str, i32> = Tree::new(0);
    let mut subtree_a = Tree::new(0);

    subtree_a.entry("<user_id>").or_insert(Tree::new(10));
    tree.entry("users").or_insert(subtree_a);

    let keys = vec!["users", "<user_id>"];


    for key in &keys {
        match tree.get(*key) {
            Some(a) => {
                if a.value == 0 {
                    println!("Going Inside: {:?}", a);
                    tree = a.clone();
                } else {
                    println!("Found: {:?}", a);
                }
            }
            None => println!("Not Found: {:?}", key)
        }
    }
}
