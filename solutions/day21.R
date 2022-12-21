raw_input <- readLines("inputs/day21.txt")

parse_expression <- function(text) {
    operator <- gsub("[a-z ]+", "", text)
    parts <- strsplit(text, "\\s.\\s") |>
        unlist()
    list(f = operator, lhs = parts[[1]], rhs = parts[[2]])
}

find_humn_branch <- function(name) {
    value <- eval_env[[name]]
    if (is.list(value)) {
        any(find_humn_branch(value$lhs), find_humn_branch(value$rhs))
    } else {
        name == "humn"
    }
}

evaluate <- function(name) {
    value <- eval_env[[name]]
    if (is.integer(value)) {
        value
    } else {
        result <- match.fun(value$f)(evaluate(value$lhs), evaluate(value$rhs))
        eval_env[[name]] <- result
        result
    }
}

make_eval_env <- function(bindings) {
    setNames(bindings$constant$value, bindings$constant$name) |>
        as.list() |>
        append(
            setNames(bindings$expr$value, bindings$expr$name) |>
                as.list()
        ) |>
        list2env()
}

create_expression <- function(name) {
    value <- eval_env[[name]]
    if (name == "humn") {
        "humn"
    } else if (is.integer(value) || (is.list(value) && names(value)[[1]] != "f")) {
        value
    } else {
        lhs <- create_expression(value$lhs)
        rhs <- create_expression(value$rhs)
        # If either operand contains humn unknown, create expression instead of evaluating
        if (is.integer(lhs) && is.integer(rhs)) {
            result <- match.fun(value$f)(lhs, rhs)
            # print(result)
        } else {
            result <- list(operator = value$f, lhs = lhs, rhs = rhs)
        }
        result
    }
}

solve_equation <- function(expression, rhs) {
    inverses <- list(
        "*" = `/`,
        "/" = `*`,
        "+" = `-`,
        "-" = `+`
    )
    while (length(expression) > 1L) {
        left_num <- is.numeric(expression$lhs)
        right_num <- is.numeric(expression$rhs)
        if (left_num || right_num) {
            if (left_num && right_num) {
                return(match.fun(expression$operator, expression$lhs, expression$rhs))
            } else if (left_num) {
                constant <- "lhs"
                nested <- "rhs"
            } else if (right_num) {
                constant <- "rhs"
                nested <- "lhs"
            }
            # Both nested
        } else if (!"humn" %in% unlist(expression$lhs, use.names = FALSE)) {
            expression$lhs <- evaluate_expression(expression$lhs)
            constant <- "lhs"
            nested <- "rhs"
        } else {
            expression$rhs <- evaluate_expression(expression$rhs)
            constant <- "rhs"
            nested <- "lhs"
        }

        inverse <- inverses[[expression$operator]]
        if (constant == "lhs" && (identical(inverse, `*`) || identical(inverse, `+`))) {
            if (identical(inverse, `*`)) { # division rhs
                rhs <- rhs / expression$lhs
            } else { # subtraction
                rhs <- expression$lhs - rhs
            }
        } else { # * or - ; simple case
            rhs <- inverse(rhs, expression[[constant]])
        }
        expression <- expression[[nested]]
    }
    rhs
}

evaluate_expression <- function(expression) {
    if (is.numeric(expression)) {
        expression
    } else {
        match.fun(expression$operator)(evaluate_expression(expression$lhs), evaluate_expression(expression$rhs))
    }
}

eval_env <- new.env()

bindings <- strsplit(raw_input, ": ") |>
    do.call(what = rbind) |>
    as.data.frame() |>
    setNames(c("name", "value"))
bindings <- split(bindings, c("expr", "constant")[grepl("\\d+", bindings$value) + 1])

bindings$constant$value <- as.integer(bindings$constant$value)
bindings$expr$value <- lapply(bindings$expr$value, parse_expression)

eval_env <- make_eval_env(bindings)


part1 <- evaluate("root")
cat(as.character(part1), "\n")

eval_env <- make_eval_env(bindings)

# Identify which branch as "humn"
possibilities <- c(eval_env$root$lhs, eval_env$root$rhs)
humn_branch <- if (find_humn_branch(possibilities[[1]])) possibilities[[1]] else possibilities[[2]]
rhs <- evaluate(setdiff(possibilities, humn_branch))
lhs <- create_expression(humn_branch)
part2 <- solve_equation(lhs, rhs)
cat(as.character(part2), "\n")
