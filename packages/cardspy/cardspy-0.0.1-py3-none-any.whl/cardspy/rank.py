"""Rank"""
from dataclasses import dataclass


@dataclass
class Rank:
    """Rank"""
    key: int
    code: str
    name: str

    def __str__(self) -> str:
        return self.code

    def __repr__(self) -> str:
        return self.code


R2 = Rank(0x1, "2", "Two")
R3 = Rank(0x2, "3", "Three")
R4 = Rank(0x4, "4", "Four")
R5 = Rank(0x8, "5", "Five")
R6 = Rank(0x10, "6", "Six")
R7 = Rank(0x20, "7", "Seven")
R8 = Rank(0x40, "8", "Eight")
R9 = Rank(0x80, "9", "Nine")
RT = Rank(0x100, "10", "Ten")
RJ = Rank(0x200, "J", "Jack")
RQ = Rank(0x400, "Q", "Queen")
RK = Rank(0x800, "K", "King")
RA = Rank(0x1000, "A", "Ace")

NUM_RANKS = 13
