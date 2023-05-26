#!/usr/bin/bash

file='inputs/day2.txt'
ASCII_A=65
ASCII_X=88
IFS=" "
part1=0
part2=0

score() {
    local diff="$1"
    if [[ "$diff" -eq -2 || "$diff" -eq 1 ]]; then
        result=0
    elif [[ "$diff" -eq -1 || "$diff" -eq 2 ]]; then
        result=6
    else
        result=3
    fi
    echo "$result"
}

 while read -r line; do
    opponent=$(LC_CTYPE=C printf '%d' "'${line% [ABC]}'")
    opponent="$(("$opponent" - "$ASCII_A"))"
    player=$(LC_CTYPE=C printf '%d' "'${line#[ABC] }'")
    player="$(("$player" - "$ASCII_X"))"

    diff=$(("$opponent" - "$player"))
    result=$(score "$diff")

    result=$(("$result" + "$player" + 1))
    part1=$(("$part1" + "$result"))

    # Where player is intended game outcome
    if [[ $player -eq 0 ]]; then #lose
        player=$(($(("$opponent" + 2)) % 3))
    elif [[ $player -eq 1 ]]; then #draw
        player="$opponent"
    else  # win
        player=$(($(("$opponent" + 1)) % 3))
    fi

    diff=$(("$opponent" - "$player"))
    result=$(score "$diff")
    result=$(("$result" + "$player" + 1))
    part2=$(("$part2" + "$result"))
done < <(cat "$file")

echo "part 1: $part1"
echo "part 2: $part2"
