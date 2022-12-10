library(ggplot2)

calories <- readLines("inputs/day1.txt")
calories <- data.frame(calories = calories)
calories$elf <- cumsum(calories$calories == "") + 1
calories <- calories[calories$calories != "", ]
