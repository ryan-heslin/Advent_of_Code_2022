make_visible <- function(length) {
    sequence <- seq_len(length)
    function(x) {
        vapply(sequence[-c(1, length)], \(i){
            x[[i]] > max(x[sequence < i]) || x[[i]] > max(x[sequence > i])
        }, FUN.VALUE = logical(1))
    }
}

score_all <- function(grid) {
    distance_to_obstruction <- function(trees, height, comparator, index, offset = 0) {
        # Clamp to length of vector
        nearest <- which(trees >= height) |>
            comparator() |>
            max(1) |>
            min(length(trees))
        abs(nearest + offset - index)
    }

    scenic_score <- function(coord) {
        i <- coord[[1]]
        j <- coord[[2]]
        height <- coord[[3]]
        # TRBL order
        c(
            distance_to_obstruction(grid[seq(
                from = 1,
                to = i - 1, by = 1
            ), j], height, max, i),
            distance_to_obstruction(grid[i, seq(
                from = j + 1,
                to = dimension, by = 1
            )], height, min, j, j),
            distance_to_obstruction(grid[seq(
                from = i + 1,
                to = dimension, by = 1
            ), j], height, min, i, i),
            distance_to_obstruction(grid[i, seq(
                from = 1,
                to = j - 1, by = 1
            )], height, max, j)
        ) |>
            prod()
    }

    dimension <- nrow(grid)
    outer_ring <- dimension - 1
    candidates <- seq(from = 2, to = outer_ring, by = 1)
    indices <- data.frame(i = candidates, j = candidates) |>
        expand.grid()
    indices[["height"]] <- grid[as.matrix(indices)]
    indices <- t(indices) |>
        asplit(MARGIN = 2)
    vapply(indices, scenic_score, FUN.VALUE = numeric(1))
}
raw_input <- readLines("inputs/day8.txt")

grid <- strsplit(raw_input, "") |>
    do.call(what = rbind) |>
    as.matrix() |>
    `class<-`("integer")

max_dim <- ncol(grid)
dimension <- ncol(grid)
sequence <- seq(from = 2, to = dimension - 1, by = 1)
if (!dimension == nrow(grid)) {
    stop()
}
# All perimeter trees visible
perimeter <- dimension * 4 - 4
is_visible <- make_visible(dimension)

rows <- grid[sequence, ] |>
    asplit(MARGIN = 1) |>
    vapply(is_visible, FUN.VALUE = logical(dimension - 2)) |>
    t()

columns <- grid[, sequence] |>
    asplit(MARGIN = 2) |>
    vapply(is_visible, FUN.VALUE = logical(dimension - 2))

part1 <- perimeter + sum(rows | columns)
print(part1)

result <- suppressWarnings(score_all(grid))
part2 <- max(result)
print(part2)
