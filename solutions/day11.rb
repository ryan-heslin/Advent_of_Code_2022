class Monkey
  attr_reader :items, :divisor, :current_hazard, :targets, :inspections
  def initialize(lines)
    lines = lines.split("\n")
    @items = (lines[1].split(": "))[1].split(", ").map { |x| x.to_i }
    @current_hazard = nil
    @operation =
      (lines[2].split(": "))[1].tr("new = ", "").gsub(/old/, "@current_hazard")
    @divisor = read_right_integer(lines[3])
    @targets = [read_right_integer(lines[5]), read_right_integer(lines[4])]
    @inspections = 0
  end

  def read_right_integer(string)
    string.split(" ")[-1].to_i()
  end

  def test()
    @current_hazard % @divisor == 0
  end

  def operate()
    @current_hazard = (eval(@operation) / 3).floor()
  end

  def give()
    @items.shift() if @items.size() > 1
  end

  def receive(item)
    @items.push(item)
  end

  def round()
    result = []
    while @items.size() > 0
      @inspections = @inspections + 1
      @current_hazard = @items.shift()
      operate
      target = test ? 1 : 0
      #puts("Giving to " + @targets[target].to_s)
      result.push([@targets[target], @current_hazard])
      #@current_hazard = nil
      result
    end
    result
  end
end

#file = File.new("inputs/day11.txt")
raw_input = File.read("inputs/day11.txt")
#file.close

processed = raw_input.split(/\n\n/)
#puts(processed.len)

# Word for a group of monkeys
troop = processed.map { |x| Monkey.new(x) }
round = 1
n_monkeys = troop.size()

for round in 1..20
  for monkey in 0..(n_monkeys - 1)
    result = troop[monkey].round()
    #puts(result)
    if result.size > 0
      for i in 0..(result.size() - 1)
        troop[result[i][0]].receive(result[i][1])
      end
    end
  end
end

ranking = troop.map { |x| x.inspections }.sort { |a, b| b - a }
monkey_business = ranking[0] * ranking[1]
puts(monkey_business)

class IndivisibleMonkey < Monkey
  def operate()
    # puts("Before " + @current_hazard.to_s)
    eval(@operation)
    # puts("After " + @current_hazard.to_s)
  end
end

new_troop = processed.map { |x| IndivisibleMonkey.new(x) }
round = 1
n_monkeys = troop.size()
memo = {}

puts("PART 2")
for round in 1..20
  for monkey in 0..(n_monkeys - 1)
    # puts("Monkey " + monkey.to_s)
    # puts(" ")
    result = new_troop[monkey].round()
    #puts(result)
    if result.size > 0
      for i in 0..(result.size() - 1)
        new_troop[result[i][0]].receive(result[i][1])
      end
    end
  end
  #this_round = new_troop.map { |x| x.items.dup }
  # if memo.has_value?(this_round)
  #   puts(round)
  #   break
  # else
  #   memo[round] = this_round
  # end
end
#
puts new_troop.map { |x| x.inspections }
ranking = new_troop.map { |x| x.inspections }.sort { |a, b| b - a }
monkey_business = ranking[0] * ranking[1]
puts(monkey_business)
