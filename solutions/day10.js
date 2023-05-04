const fs = require('fs');

const raw_input = fs.readFileSync('inputs/day10.txt', 'utf-8').toString().split("\n")
let X = 1;
let record = new Map();
let cycle = 1;
let all = 0;
const period = 20;
const needed = new Set([20, 60, 100, 140, 180, 220]);

for (let i = 0; i < raw_input.length; i++) {

    let inc = 0;
    let cycle_inc = 1;
    if (raw_input[i] != "noop") {
        cycle_inc = cycle_inc + 1;
        inc = parseInt(raw_input[i].split(" ")[1])
    }
    let offset = cycle % period;

    // Account for add instructions going one over period
    if (offset == 0 || (offset == period - 1 && cycle_inc == 2)) {
        let target = cycle + (offset > 0);
        record.set(target, target * X);
        if (needed.has(target)) {
            all = all + (target * X);
        }
    }
    cycle = cycle + cycle_inc;
    X = X + inc;
}

let current_cycle = 1;
let sprite = 1;
const width = 40;
const n_rows = Math.floor(cycle / width)
let image = Array(n_rows).fill().map(() => Array(width).fill("."))
//image = image.fill(".")

// Modify pixel in-place
function draw(row, i, sprite) {
    if (i >= 0 && i < 40 && i >= sprite - 1 && i <= sprite + 1) {
        image[row][i] = "#";
    }
}
for (let i = 0; i < raw_input.length; i++) {

    //If add, consume two cycles
    //Else consume 1

    let current_row = Math.floor(current_cycle / width)
    let change = 0;
    draw(current_row, (current_cycle - 1) % width, sprite);
    if (raw_input[i] != "noop") {
        change = change + parseInt(raw_input[i].split(" ")[1]);
        current_cycle++;
        draw(current_row, (current_cycle - 1) % width, sprite);
    }
    current_cycle++;
    // If add, reset sprite to new value
    sprite = sprite + change;
}


console.log(all);

for (let i = 0; i < image.length; i++) {
    console.log(image[i].toString());
}
