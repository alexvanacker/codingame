use std::io;

macro_rules! print_err {
    ($($arg:tt)*) => (
        {
            use std::io::Write;
            writeln!(&mut ::std::io::stderr(), $($arg)*).ok();
        }
    )
}

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
    //let w = parse_input!(inputs[0], i32); // number of columns.
    let h = parse_input!(inputs[1], i32); // number of rows.
    let mut map: Vec<Vec<String>> = Vec::with_capacity(h as usize);

    for i in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let line = input_line.trim_right().to_string(); // represents a line in the grid and contains W integers. Each integer represents one room of a given type.
        map.push(
            line.split(" ")
                .map(|s| s.to_string())
                .collect::<Vec<String>>(),
        );
    }

    //print_err!("Map is {:?}", map);
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    //let ex = parse_input!(input_line, i32); // the coordinate along the X axis of the exit (not useful for this first mission, but must be read).

    // game loop
    loop {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let xi = parse_input!(inputs[0], i32);
        let yi = parse_input!(inputs[1], i32);
        let pos = inputs[2].trim().to_string();

        let room_type = &map[yi as usize][xi as usize];
        print_err!("Room type for ({}, {}): {}", xi, yi, room_type);
        let (x_exit, y_exit) = get_exit(room_type, xi, yi, &pos);
        // Write an action using println!("message...");
        // To debug: print_err!("Debug message...");

        // One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
        println!("{} {}", x_exit, y_exit);
    }
}

pub fn get_exit(room_type: &str, pos_x: i32, pos_y: i32, pos: &String) -> (i32, i32) {
    let bottom = (pos_x, pos_y + 1);
    let left = (pos_x - 1, pos_y);
    let right = (pos_x + 1, pos_y);
    match (room_type, pos.as_ref()) {
        ("1", _) => bottom,
        ("2", "LEFT") => right,
        ("2", "RIGHT") => left,
        ("3", _) => bottom,
        ("4", "TOP") => left,
        ("4", "RIGHT") => bottom,
        ("5", "TOP") => right,
        ("5", "LEFT") => bottom,
        ("6", "LEFT") => right,
        ("6", "RIGHT") => left,
        ("7", _) => bottom,
        ("8", _) => bottom,
        ("9", _) => bottom,
        ("10", _) => left,
        ("11", _) => right,
        ("12", _) => bottom,
        ("13", _) => bottom,
        _ => panic!("Unexpected room type: {:?}", room_type),
    }
}
