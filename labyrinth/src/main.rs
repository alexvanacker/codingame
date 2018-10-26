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
    let inputs = input_line.split(" ").collect::<Vec<_>>();
    let r = parse_input!(inputs[0], i32); // number of rows.
    let c = parse_input!(inputs[1], i32); // number of columns.
    let a = parse_input!(inputs[2], i32); // number of rounds between the time the alarm countdown is activated and the time the alarm goes off.

    // game loop
    loop {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let kr = parse_input!(inputs[0], i32); // row where Kirk is located.
        let kc = parse_input!(inputs[1], i32); // column where Kirk is located.
        for i in 0..r as usize {
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line).unwrap();
            let row = input_line.trim().to_string(); // C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        }

        // Write an action using println!("message...");
        // To debug: eprintln!("Debug message...");

        println!("RIGHT"); // Kirk's next move (UP DOWN LEFT or RIGHT).
    }
}