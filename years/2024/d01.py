from utils import challenge

SAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3"""

class D01(challenge.Challenge):
    TESTS = [
        challenge.TestCase(data=SAMPLE, expects=11, part=1),
        challenge.TestCase(data=SAMPLE, expects=31, part=2)
    ]

    def part1(self, data: list[list[int]]):
        return 10
    
    def part2(self, data: list[list[int]]):
        return 30