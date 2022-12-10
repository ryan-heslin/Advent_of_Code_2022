local form_stacks = function(data)
    -- For each line, going backwards
    local line = data[#data]
    local start, _ = string.find(line, "%d+")
    local length = string.len(line)
    local indices = {}
    local stacks = {}
    local skip = 4

    for i = start, length + 1, skip do
        table.insert(indices, i)
        table.insert(stacks, {})
    end

    for level = #data - 1, 1, -1 do
        for i, idx in ipairs(indices) do
            value = string.sub(data[level], idx, idx)
            if value ~= "" and value ~= " " then
                table.insert(stacks[i], value)
            end
        end
    end
    return stacks
    -- Get positions of A-Z letters
    -- Insert letter in stack at each position (both 1-indexed)
end

local parse = function(filename)
    local file = io.lines(filename)
    local stacks = {}
    local instructions = {}
    target = stacks

    for line in file do
        -- Stack data done; instructions remain
        if line == "" then
            target = instructions
        else
            table.insert(target, line)
        end
    end
    return stacks, instructions
end

local move = function(crates, from, to)
    local stack_size = #stacks[from]
    for i = stack_size, stack_size - crates + 1, -1 do
        local value = table.remove(stacks[from], i)
        table.insert(stacks[to], value)
    end
end

local over_9000 = function(crates, from, to)
    local stack_size = #stacks[from]
    local bottom_crate = stack_size - crates + 1
    for _ = bottom_crate, stack_size, 1 do
        local value = table.remove(stacks[from], bottom_crate)
        table.insert(stacks[to], value)
    end
end

local top_crates = function()
    local result = {}
    local next
    for _, stack in ipairs(stacks) do
        if stack == {} then
            next = ""
        else
            next = stack[#stack]
        end
        table.insert(result, next)
    end
    return result
end

-- Get data from each instruction line
local compile = function(line)
    local args = {}
    for num in string.gmatch(line, "%d+") do
        table.insert(args, tonumber(num))
    end
    return args
end

local stack_data, instructions = parse("inputs/day5.txt")
stacks = form_stacks(stack_data)

local code = {}
for i, line in ipairs(instructions) do
    code[i] = compile(instructions[i])
end

for _, line in ipairs(code) do
    move(unpack(line))
end

local top = top_crates()
part1 = table.concat(top, "")
print(part1)

stacks = form_stacks(stack_data)
for _, line in ipairs(code) do
    over_9000(unpack(line))
end

local top = top_crates()
part2 = table.concat(top, "")
print(part2)
