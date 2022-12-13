class Interval
  public

  attr_reader :lower, :upper
  def initialize(lower, upper)
    @lower = lower
    @upper = upper
  end

  def contains(other)
    @lower >= other.lower and @upper <= other.upper
  end

  def equal(other)
    @lower == other.lower and @upper == other.upper
  end

  def overlaps(other)
    (@upper == other.lower) or
      (other.lower <= @upper and @upper <= other.upper) or
      (other.lower <= @lower and @lower <= other.upper) or
      (@lower == other.upper) or equal(other)
  end
end

file = File.new("inputs/day4.txt")
raw_input = file.readlines.map(&:chomp)
file.close

intervals =
  raw_input.map do |line|
    substrings = line.split(",")
    bounds = substrings.map { |x| x.split("-") }
    bounds.map { |x| Interval.new(x[0].to_i, x[1].to_i) }
  end

part1 =
  intervals.map do |pair|
    (pair[0].contains(pair[1]) or pair[1].contains(pair[0])) ? 1 : 0
  end

part1 = part1.sum
puts(part1)

part2 =
  intervals.map do |pair|
    (pair[0].overlaps(pair[1]) or pair[1].overlaps(pair[0])) ? 1 : 0
  end
part2 = part2.sum
puts(part2)
