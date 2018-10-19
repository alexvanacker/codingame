use std::io;
use std::collections::HashMap;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let n = parse_input!(input_line, i32); // the number of adjacency relations
    let mut graph = Graph::init();
    for _i in 0..n as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let xi = parse_input!(inputs[0], i32); // the ID of a person which is adjacent to yi
        let yi = parse_input!(inputs[1], i32); // the ID of a person which is adjacent to xi
        graph.add_node_and_neighbor(xi, yi);
    }

    // Write an action using println!("message...");
    // To debug: eprintln!("Debug message...");
    eprintln!("{:?}", graph);

    // The minimal amount of steps required to completely propagate the advertisement
    println!("1");
}

#[derive(Debug)]
struct Graph {
    graph: HashMap<i32, Vec<i32>>
}

impl<'a> Graph {
    fn init() -> Graph {
        Graph {
            graph: HashMap::new()
        }
    }

    fn get_neighbors(&'a self, node: i32) -> Option<&'a Vec<i32>> {
        self.graph.get(&node)
    }

    fn add_node_and_neighbor(&mut self, node: i32, neighbor: i32) {
        self.graph.entry(node).or_insert(Vec::new()).push(neighbor);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_graph_is_empty() {
        let graph = Graph::init();
        assert_eq!(0, graph.graph.len());
    }

    #[test]
    fn add_a_node_and_neighbor_works() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        assert_eq!(1, graph.get_neighbors(0).unwrap().len());
    }

    #[test]
    fn add_a_node_and_two_neighbor_works() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(0, 2);
        let expected = vec![1i32, 2];
        let result = graph.get_neighbors(0).unwrap();
         for (i, x) in expected.iter().enumerate() {
            assert_eq!(x, &result[i]);
        }
    }
}