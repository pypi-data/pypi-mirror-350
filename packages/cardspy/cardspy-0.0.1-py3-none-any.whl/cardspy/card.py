"""Card"""
from typing import List
from functools import reduce
from dataclasses import dataclass
from .rank import (
    Rank,
    R2,
    R3,
    R4,
    R5,
    R6,
    R7,
    R8,
    R9,
    RT,
    RJ,
    RQ,
    RK,
    RA,
)
from .suit import Suit, CLUB, DIAMOND, HEART, SPADE


@dataclass
class Card:
    """Card"""
    key: int
    rank: Rank
    suit: Suit
    code: str
    name: str
    symbol: str

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: "Card") -> bool:
        return self.key < other.key

    def __le__(self, other: "Card") -> bool:
        return self.key <= other.key

    def __gt__(self, other: "Card") -> bool:
        return self.key > other.key

    def __ge__(self, other: "Card") -> bool:
        return self.key >= other.key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.key == other.key

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.key != other.key


C2C = Card(0x1, R2, CLUB, "2C", "Two of Clubs", "2♣")
C2D = Card(0x2, R2, DIAMOND, "2D", "Two of Diamonds", "2♦")
C2H = Card(0x4, R2, HEART, "2H", "Two of Hearts", "2♥")
C2S = Card(0x8, R2, SPADE, "2S", "Two of Spades", "2♠")

C3C = Card(0x10, R3, CLUB, "3C", "Three of Clubs", "3♣")
C3D = Card(0x20, R3, DIAMOND, "3D", "Three of Diamonds", "3♦")
C3H = Card(0x40, R3, HEART, "3H", "Three of Hearts", "3♥")
C3S = Card(0x80, R3, SPADE, "3S", "Three of Spades", "3♠")

C4C = Card(0x100, R4, CLUB, "4C", "Four of Clubs", "4♣")
C4D = Card(0x200, R4, DIAMOND, "4D", "Four of Diamonds", "4♦")
C4H = Card(0x400, R4, HEART, "4H", "Four of Hearts", "4♥")
C4S = Card(0x800, R4, SPADE, "4S", "Four of Spades", "4♠")

C5C = Card(0x1000, R5, CLUB, "5C", "Five of Clubs", "5♣")
C5D = Card(0x2000, R5, DIAMOND, "5D", "Five of Diamonds", "5♦")
C5H = Card(0x4000, R5, HEART, "5H", "Five of Hearts", "5♥")
C5S = Card(0x8000, R5, SPADE, "5S", "Five of Spades", "5♠")

C6C = Card(0x10000, R6, CLUB, "6C", "Six of Clubs", "6♣")
C6D = Card(0x20000, R6, DIAMOND, "6D", "Six of Diamonds", "6♦")
C6H = Card(0x40000, R6, HEART, "6H", "Six of Hearts", "6♥")
C6S = Card(0x80000, R6, SPADE, "6S", "Six of Spades", "6♠")

C7C = Card(0x100000, R7, CLUB, "7C", "Seven of Clubs", "7♣")
C7D = Card(0x200000, R7, DIAMOND, "7D", "Seven of Diamonds", "7♦")
C7H = Card(0x400000, R7, HEART, "7H", "Seven of Hearts", "7♥")
C7S = Card(0x800000, R7, SPADE, "7S", "Seven of Spades", "7♠")

C8C = Card(0x1000000, R8, CLUB, "8C", "Eight of Clubs", "8♣")
C8D = Card(0x2000000, R8, DIAMOND, "8D", "Eight of Diamonds", "8♦")
C8H = Card(0x4000000, R8, HEART, "8H", "Eight of Hearts", "8♥")
C8S = Card(0x8000000, R8, SPADE, "8S", "Eight of Spades", "8♠")

C9C = Card(0x10000000, R9, CLUB, "9C", "Nine of Clubs", "9♣")
C9D = Card(0x20000000, R9, DIAMOND, "9D", "Nine of Diamonds", "9♦")
C9H = Card(0x40000000, R9, HEART, "9H", "Nine of Hearts", "9♥")
C9S = Card(0x80000000, R9, SPADE, "9S", "Nine of Spades", "9♠")

CTC = Card(0x100000000, RT, CLUB, "TC", "Ten of Clubs", "10♣")
CTD = Card(0x200000000, RT, DIAMOND, "TD", "Ten of Diamonds", "10♦")
CTH = Card(0x400000000, RT, HEART, "TH", "Ten of Hearts", "10♥")
CTS = Card(0x800000000, RT, SPADE, "TS", "Ten of Spades", "10♠")

CJC = Card(0x1000000000, RJ, CLUB, "JC", "Jack of Clubs", "J♣")
CJD = Card(0x2000000000, RJ, DIAMOND, "JD", "Jack of Diamonds", "J♦")
CJH = Card(0x4000000000, RJ, HEART, "JH", "Jack of Hearts", "J♥")
CJS = Card(0x8000000000, RJ, SPADE, "JS", "Jack of Spades", "J♠")

CQC = Card(0x10000000000, RQ, CLUB, "QC", "Queen of Clubs", "Q♣")
CQD = Card(0x20000000000, RQ, DIAMOND, "QD", "Queen of Diamonds", "Q♦")
CQH = Card(0x40000000000, RQ, HEART, "QH", "Queen of Hearts", "Q♥")
CQS = Card(0x80000000000, RQ, SPADE, "QS", "Queen of Spades", "Q♠")

CKC = Card(0x100000000000, RK, CLUB, "KC", "King of Clubs", "K♣")
CKD = Card(0x200000000000, RK, DIAMOND, "KD", "King of Diamonds", "K♦")
CKH = Card(0x400000000000, RK, HEART, "KH", "King of Hearts", "K♥")
CKS = Card(0x800000000000, RK, SPADE, "KS", "King of Spades", "K♠")

CAC = Card(0x1000000000000, RA, CLUB, "AC", "Ace of Clubs", "A♣")
CAD = Card(0x2000000000000, RA, DIAMOND, "AD", "Ace of Diamonds", "A♦")
CAH = Card(0x4000000000000, RA, HEART, "AH", "Ace of Hearts", "A♥")
CAS = Card(0x8000000000000, RA, SPADE, "AS", "Ace of Spades", "A♠")

ALL_CARDS = [
    C2C, C2D, C2H, C2S,
    C3C, C3D, C3H, C3S,
    C4C, C4D, C4H, C4S,
    C5C, C5D, C5H, C5S,
    C6C, C6D, C6H, C6S,
    C7C, C7D, C7H, C7S,
    C8C, C8D, C8H, C8S,
    C9C, C9D, C9H, C9S,
    CTC, CTD, CTH, CTS,
    CJC, CJD, CJH, CJS,
    CQC, CQD, CQH, CQS,
    CKC, CKD, CKH, CKS,
    CAC, CAD, CAH, CAS,
]


def sort_cards(cards: List[Card]) -> List[Card]:
    """Sort cards by rank"""
    return sorted(cards, key=lambda card: card.rank.key)


def cards_mask(cards: List[Card]) -> int:
    """
    Given an iterable of Card objects with a .id attribute (an int bit‐mask),
    return the combined mask of all those cards.
    """
    return reduce(lambda mask, card: mask | card.key, cards, 0)


# def rank_mask_from_cards(cards: int) -> int:
#     """
#     Given an int bit-mask of cards, return the combined mask of
#     all those cards.
#     """
#     rmask = 0
#     for card in ALL_CARDS:
#         if cards & card.key != 0:
#             rmask |= card.rank.key
#     return rmask


def extract_cards(cards: int) -> List[Card]:
    """
    Given an int bit-mask of cards, return the list of Card objects
    that make up that mask.
    """
    return [
        card for card in ALL_CARDS if cards & card.key != 0
    ]
