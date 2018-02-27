
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
    let w = parse_input!(inputs[0], i32); // number of columns.
    let h = parse_input!(inputs[1], i32); // number of rows.
    let mut map: Vec<Vec<i32>> = Vec::with_capacity(h as usize);

    for i in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let line = input_line.trim_right().to_string(); // represents a line in the grid and contains W integers. Each integer represents one room of a given type.
        let mut row: Vec<i32> = Vec::with_capacity(w as usize);

        for room in line.split(" ").collect::<Vec<_>>(){
            let room = room.parse::<i32>().unwrap();
            row.push(room);
        }
        map.push(row);
    }

    //print_err!("Map is {:?}", map);
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let ex = parse_input!(input_line, i32); // the coordinate along the X axis of the exit (not useful for this first mission, but must be read).

    // game loop
    loop {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let xi = parse_input!(inputs[0], i32);
        let yi = parse_input!(inputs[1], i32);
        let pos = inputs[2].trim().to_string();

        let room_type = map[yi as usize][xi as usize];
        print_err!("Room type for ({}, {}): {}", xi, yi, room_type);
        let (x_exit, y_exit) = get_exit(room_type, xi ,yi, &pos);
        // Write an action using println!("message...");
        // To debug: print_err!("Debug message...");

        // One line containing the X Y coordinates of the room in which you believe Indy will be on the next turn.
        println!("{} {}", x_exit, y_exit);
    }
}

pub fn get_exit(room_type: i32, pos_x: i32, pos_y: i32, pos: &String) -> (i32, i32) {
    match (room_type, pos.as_ref()) {
        (0, _) => return (-1, -1),
        (1, _) => return (pos_x, pos_y + 1),
        (2, "LEFT") => return (pos_x + 1, pos_y),
        (2, "RIGHT") => return (pos_x - 1, pos_y),
        (3, _) => (pos_x, pos_y + 1),
        (4, "TOP") => (pos_x - 1, pos_y),
        (4, "RIGHT") => (pos_x, pos_y + 1),
        (5, "TOP") => (pos_x + 1, pos_y),
        (5, "LEFT") => (pos_x, pos_y + 1),
        (6, "LEFT") => return (pos_x + 1, pos_y),
        (6, "RIGHT") => return (pos_x - 1, pos_y),
        (7, _) => return (pos_x, pos_y + 1),
        (8, _) => return (pos_x, pos_y + 1),
        (9, _) => return (pos_x, pos_y + 1),
        (10, _) => return (pos_x - 1, pos_y),
        (11, _) => (pos_x + 1, pos_y),
        (12, _) => (pos_x, pos_y + 1),
        (13, _) => (pos_x, pos_y + 1),
        _ => (-1, -1)

    }
}
