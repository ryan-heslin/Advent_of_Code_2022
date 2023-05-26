// Pattern bug fixed by smolda from AoC discord
const fs = require('fs');

const raw_input = fs.readFileSync('inputs/day6.txt', 'utf-8');

const part1_pattern = /([a-z])(?!\1)([a-z])(?!(?:\1|\2))([a-z])(?!(?:\1|\2|\3))/
const n_chars = 4;
const part1 = raw_input.search(part1_pattern) + n_chars;
console.log(part1);

let start = 0;
let end = 14;

// From https://stackoverflow.com/questions/12870489/regex-to-match-a-word-with-unique-non-repeating-characters
// Match words with dupe characters
let part2_pattern = /^[a-z]*([a-z])[a-z]*\1[a-z]*$/
let chars = raw_input.substring(start, end);

while (part2_pattern.test(chars)) {
    start++;
    end++;
    chars = raw_input.substring(start, end);
}
const part2 = end;
console.log(part2);
