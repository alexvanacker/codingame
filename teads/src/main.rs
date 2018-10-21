use std::cmp;
use std::collections::HashMap;
use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => {
        $x.trim().parse::<$t>().unwrap()
    };
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
    let propagation_time = compute_propagation_time(&graph);
    println!("{:?}", propagation_time);
}

fn compute_propagation_time(g: &Graph) -> usize {
    let mut propagation_time = g.edges.keys().len();
    for node in g.edges.keys() {
        propagation_time = cmp::min(compute_propagation_time_for_node(g, node), propagation_time);
    }
    propagation_time
}

fn compute_propagation_time_for_node(g: &Graph, n: &i32) -> usize {
    let mut node_visit_status_map = g.build_node_visited_map();
    dfs(&g, n, &mut node_visit_status_map)
}

fn dfs(g: &Graph, n: &i32, status: &mut HashMap<i32, bool>) -> usize {
    status.insert(*n, true);
    // eprintln!("Visiting {:?}", n);
    let mut node_time = 0;
    for &neighbor in g.get_neighbors(n).unwrap() {
        if !status.get(&neighbor).unwrap() {
            node_time = cmp::max(node_time, 1 + dfs(g, &neighbor, status));
        }
    }
    // eprintln!("Node time for {:?}: {:?}", n, node_time);
    node_time
}

#[derive(Clone, Debug)]
struct Graph {
    edges: HashMap<i32, Vec<i32>>,
}

impl Graph {
    fn init() -> Graph {
        Graph {
            edges: HashMap::new(),
        }
    }

    fn add_node_and_neighbor(&mut self, node: i32, neighbor: i32) {
        self.edges.entry(node).or_insert(Vec::new()).push(neighbor);
        self.edges.entry(neighbor).or_insert(Vec::new()).push(node);
    }

    fn get_neighbors<'a>(self: &'a Graph, node: &i32) -> Option<&'a Vec<i32>> {
        self.edges.get(node)
    }

    fn build_node_visited_map(&self) -> HashMap<i32, bool> {
        let mut map: HashMap<i32, bool> = HashMap::new();
        for key in self.edges.keys() {
            map.insert(*key, false);
        }
        map
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_graph_is_empty() {
        let graph = Graph::init();
        assert_eq!(0, graph.edges.len());
    }

    #[test]
    fn add_a_node_and_neighbor_works() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        assert_eq!(1, graph.get_neighbors(&0).unwrap().len());
    }

    #[test]
    fn add_a_node_and_two_neighbor_works() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(0, 2);
        let expected = vec![1i32, 2];
        let result = graph.get_neighbors(&0).unwrap();
        for (i, x) in expected.iter().enumerate() {
            assert_eq!(x, &result[i]);
        }
    }

    #[test]
    fn simple_propagation_time_for_node() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(1, 2);
        let result = compute_propagation_time_for_node(&graph, &0);
        assert_eq!(2, result);
    }

    #[test]
    fn simple_propagation_time() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(1, 2);
        let result = compute_propagation_time(&graph);
        assert_eq!(1, result);
    }
}
