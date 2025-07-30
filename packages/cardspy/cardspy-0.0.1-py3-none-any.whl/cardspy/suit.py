"""Suit"""
from dataclasses import dataclass


@dataclass
class Suit:
    """Suit"""
    key: int
    code: str
    name: str
    symbol: str

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return self.symbol


CLUB = Suit(0x1, "C", "Club", "♣")
DIAMOND = Suit(0x2, "D", "Diamond", "♦")
HEART = Suit(0x4, "H", "Heart", "♥")
SPADE = Suit(0x8, "S", "Spade", "♠")
