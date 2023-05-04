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
      result.push([@targets[target], @current_hazard])
      #@current_hazard = nil
      result
    end
    result
  end
end

raw_input = File.read("inputs/day11.txt")

processed = raw_input.split(/\n\n/)
#puts(processed.size)

# Word for a group of monkeys
troop = processed.map { |x| Monkey.new(x) }
round = 1
n_monkeys = troop.size()

for round in 1..20
  for monkey in 0..(n_monkeys - 1)
    result = troop[monkey].round()
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

class Item
  attr_reader :value, :id

  public

  def initialize(value, id)
    @value = value
    @id = id
  end

  def value=(value)
    @value = value
  end

  def to_s
    @id.to_s + " - " + @value.to_s
  end
end

class DividingMonkey < Monkey
  def round()
    result = []
    while @items.size() > 0
      @inspections = @inspections + 1
      @current_hazard = @items.shift()
      operate
      target = test ? 1 : 0
      dividend = @current_hazard % @modulus
      # Clamp here?
      @current_hazard =
        (
          if dividend == 0
            @modulus
          else
            dividend
          end
        )
      result.push([@targets[target], @current_hazard])
      #@current_hazard = nil
      result
    end
    result
  end

  def modulus=(value)
    @modulus = value
  end
  def operate
    @current_hazard = eval(@operation)
  end
end

class ItemMonkey < Monkey
  attr_reader :items, :divisor, :current_hazard, :targets, :inspections
  def initialize(lines, next_id)
    lines = lines.split("\n")
    values = (lines[1].split(": "))[1].split(", ").map { |x| x.to_i }
    @items = Array.new(values.size())
    #ids = next_id..(next_id + values.size())

    for i in 0..(values.size - 1)
      @items[i] = Item.new(values[i], next_id)
      next_id = next_id + 1
    end

    #@items = values.zip(ids).each { |pair| Item.new(pair[0], pair[1]) }
    @current_hazard = nil
    @operation =
      (lines[2].split(": "))[1].tr("new = ", "").gsub(/old/, "@current_hazard")
    @divisor = read_right_integer(lines[3])
    @targets = [read_right_integer(lines[5]), read_right_integer(lines[4])]
    @inspections = 0
  end
  def operate()
    eval(@operation)
  end
  def round()
    result = []
    while @items.size() > 0
      @inspections = @inspections + 1
      new_item = @items.shift()
      @current_hazard = new_item.value
      operate
      target = test ? 1 : 0
      new_item.value = @current_hazard
      result.push([@targets[target], new_item])
      #@current_hazard = nil
      result
    end
    result
  end
end

next_id = 1
new_troop = []
# for i in 0..(processed.size() - 1)
#   new_monkey = ItemMonkey.new(processed[i], next_id)
#   next_id = next_id + new_monkey.items.size() + 1
#   new_troop.append(new_monkey)
# end
#
new_troop = processed.map { |x| DividingMonkey.new(x) }
product = new_troop.map { |x| x.divisor }.inject(:*)

#round = 1
rounds = 10_000
n_monkeys = troop.size()
arrangements = {}
totals = {}

for i in 0..(n_monkeys - 1)
  new_troop[i].modulus = product
end

for round in 1..rounds
  for monkey in 0..(n_monkeys - 1)
    result = new_troop[monkey].round()
    if result.size > 0
      for i in 0..(result.size() - 1)
        new_troop[result[i][0]].receive(result[i][1])
      end
    end
  end
end

ranking = new_troop.map { |x| x.inspections }.sort { |a, b| b - a }
monkey_business = ranking[0] * ranking[1]
puts(monkey_business)
