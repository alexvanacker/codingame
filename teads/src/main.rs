use std::io;

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
    for _i in 0..n as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let _xi = parse_input!(inputs[0], i32); // the ID of a person which is adjacent to yi
        let _yi = parse_input!(inputs[1], i32); // the ID of a person which is adjacent to xi
    }

    // Write an action using println!("message...");
    // To debug: eprintln!("Debug message...");


    // The minimal amount of steps required to completely propagate the advertisement
    println!("1");
}