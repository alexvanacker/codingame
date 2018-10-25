#![feature(test)]
extern crate test;

use std::cmp;
use std::collections::HashMap;
use std::collections::HashSet;
use std::collections::VecDeque;
use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => {
        $x.trim().parse::<$t>().unwrap()
    };
}

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
    eprintln!("Number of vertices {:?}", graph.get_nb_vertices());
    // Write an action using println!("message...");
    // To debug: eprintln!("Debug message...");
    eprintln!("{:?}", graph);

    // The minimal amount of steps required to completely propagate the advertisement
    let propagation_time = compute_propagation_time(&graph);
    println!("{:?}", propagation_time);
}

fn compute_propagation_time(g: &Graph) -> usize {
    let root = g.find_root();
    compute_propagation_time_for_node(g, &root)
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

    fn generate_tree(nb_edges: usize) -> Graph {
        let mut graph = Graph::init();
        for i in 0..nb_edges / 2 {
            let node = i as i32;
            let mut left = node + 1;
            while graph.edges.contains_key(&left) {
                left = left + 1
            }
            let mut right = left + 1;
            while graph.edges.contains_key(&right) {
                right = right + 1;
            }
            graph.add_node_and_neighbor(node, left);
            graph.add_node_and_neighbor(node, right);
        }
        graph
    }

    fn get_nb_vertices(&self) -> usize {
        self.edges.keys().len()
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

    fn get_leaves(&self) -> Vec<i32> {
        self.edges
            .iter()
            .filter(|(_n, ref v)| *(&v.len()) == 1)
            .map(|(&n, ref _v)| n)
            .collect::<Vec<i32>>()
    }

    fn find_shortest_path(&self, start: i32, end: i32) -> Vec<i32> {
        if start == end {
            return vec![start];
        }
        let mut to_visit = VecDeque::new();
        to_visit.push_back(start);
        let mut visited = HashSet::new();
        let mut parents: HashMap<i32, i32> = HashMap::new();
        while !to_visit.is_empty() {
            let node = to_visit.pop_front().unwrap();
            eprintln!("Shorted path: visiting {:?}", node);
            self.get_neighbors(&node).unwrap().iter().for_each(|n| {
                if !visited.contains(n) {
                    to_visit.push_back(*n);
                    parents.insert(*n, node);
                }
            });
            visited.insert(node);
            if node == end {
                break;
            }
        }
        eprintln!("child parent map: {:?}", parents);
        self.build_path(parents, start, end)
    }

    fn build_path(&self, child_parent_map: HashMap<i32, i32>, start: i32, end: i32) -> Vec<i32> {
        let mut path: Vec<i32> = Vec::new();
        let mut parent = *child_parent_map.get(&end).unwrap();
        path.push(end);
        while parent != start {
            path.push(parent);
            parent = *child_parent_map.get(&parent).unwrap();
        }
        path.push(start);
        path.reverse();
        eprintln!("Path from {:?} to {:?} is {:?}", start, end, path);
        path
    }

    fn find_root(&self) -> i32 {
        // Find (u,v) vertices such that dist(u,v) is the maximum distance in tree
        // i.e. the tree diameter
        let u = self.bsf(self.get_leaves()[0]);
        let v = self.bsf(u);
        // Find shortest path between the two and get the middle node. That is the tree root.
        let path = self.find_shortest_path(u, v);
        let radius = path.len() / 2;
        let root = path[radius];
        eprintln!("Root: {:?}", root);
        root
    }

    fn bsf(&self, node: i32) -> i32 {
        let mut to_check = VecDeque::new();
        to_check.push_back(node);
        let mut visited = HashSet::new();
        eprintln!("BSF To check: {:?}", to_check);
        let mut last = node;
        while !to_check.is_empty() {
            let node = to_check.pop_front().unwrap();
            if !visited.contains(&node) {
                eprintln!("BSF Visiting: {:?}", &node);
                visited.insert(node);
                self.edges.get(&node).unwrap().iter().for_each(|x| {
                    if !to_check.contains(x) && !visited.contains(x) {
                        to_check.push_back(*x)
                    }
                });
                eprintln!("To check: {:?}", to_check);
            }
            last = node;
        }
        last
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use test::Bencher;

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
    fn find_shortest_path_self() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(0, 2);
        graph.add_node_and_neighbor(1, 3);
        graph.add_node_and_neighbor(1, 4);
        graph.add_node_and_neighbor(2, 5);
        graph.add_node_and_neighbor(2, 6);
        let path = vec![0];
        assert_eq!(path, graph.find_shortest_path(0, 0));
    }

    #[test]
    fn find_shortest_path() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(0, 2);
        graph.add_node_and_neighbor(1, 3);
        graph.add_node_and_neighbor(1, 4);
        graph.add_node_and_neighbor(2, 5);
        graph.add_node_and_neighbor(2, 6);
        let path = vec![3, 1, 0, 2, 6];
        assert_eq!(path, graph.find_shortest_path(3, 6));
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

    #[test]
    fn find_root_simple() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(0, 2);
        graph.add_node_and_neighbor(1, 3);
        graph.add_node_and_neighbor(1, 4);
        graph.add_node_and_neighbor(2, 5);
        graph.add_node_and_neighbor(2, 6);
        assert_eq!(0, graph.find_root());
    }

    #[test]
    fn test_2() {
        let mut graph = Graph::init();
        graph.add_node_and_neighbor(0, 1);
        graph.add_node_and_neighbor(1, 2);
        graph.add_node_and_neighbor(1, 4);
        graph.add_node_and_neighbor(2, 3);
        graph.add_node_and_neighbor(4, 5);
        graph.add_node_and_neighbor(4, 6);
        assert_eq!(2, compute_propagation_time(&graph));
    }

    #[bench]
    fn bench_thousands(b: &mut Bencher) {
        let graph = Graph::generate_tree(3000);
        b.iter(|| compute_propagation_time(&graph));
    }
}
