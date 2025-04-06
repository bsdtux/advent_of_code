"""Module for handling Challenges"""

from typing import Any, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TestCase:
    """Represents a single test case for a challenge"""

    data: str
    expects: int | str | None
    part: int


class Challenge(ABC):
    """Abstract Class that deals with challenges"""

    TESTS: list[TestCase] = []

    def __init__(self):
        self.part_map: dict[int, Callable] = {1: self.part1, 2: self.part2}

    @abstractmethod
    def part1(self, data: Any):
        """Abstract method representing part 1 of a challenge"""
        raise NotImplementedError

    @abstractmethod
    def part2(self, data: Any):
        """Abstract Method representing part 2 of a challenge"""
        raise NotImplementedError

    def run_tests(self):
        """Test Runner"""
        for test in self.TESTS:
            part_func = self.part_map[test.part]
            assert part_func(test.data) == test.expects
    
    def run_test(self, test_case: TestCase):
        """Runs a single test"""
        assert self.part_map[test_case.part](test_case.data) == test_case.expects 
    
    def run_part(self, part, data):
        """Runs a single part with data"""
        return self.part_map[part](data)
