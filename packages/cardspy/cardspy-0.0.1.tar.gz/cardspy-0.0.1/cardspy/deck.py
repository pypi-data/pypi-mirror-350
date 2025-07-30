"""Deck"""
from random import shuffle
from typing import List
from functools import reduce
from .rank import (
    RA,
    RK,
    RQ,
    RJ,
    RT,
    R9,
    R8,
    R7,
    R6,
    R5,
    R4,
    R3,
    R2,
)
from .card import ALL_CARDS, Card, cards_mask


CLUBS = 0x1111111111111
DIAMONDS = 0x2222222222222
HEARTS = 0x4444444444444
SPADES = 0x8888888888888

SAME_RANKS = [
    0xF, 0xF0, 0xF00, 0xF000, 0xF0000, 0xF00000,
    0xF000000, 0xF0000000, 0xF00000000, 0xF000000000,
    0xF0000000000, 0xF00000000000, 0xF000000000000
]

RANKS_DESC = [RA, RK, RQ, RJ, RT, R9, R8, R7, R6, R5, R4, R3, R2]

FULL_DECK_MASK = reduce(lambda acc, card: acc | card.key, ALL_CARDS, 0)


class Deck:
    """Deck"""
    def __init__(self) -> None:
        self.bitmask = 0
        for card in ALL_CARDS:
            self.bitmask |= card.key

    def clear(self) -> None:
        """Clear the deck"""
        self.bitmask = 0

    def reset(self) -> None:
        """Reset the deck"""
        self.bitmask = FULL_DECK_MASK

    def contains(self, cards: int) -> bool:
        """Check if the deck contains a list of cards

        Args:
            cards (int): List of cards to check

        Returns:
            bool: True if the deck contains all the cards, False otherwise
        """
        return cards & self.bitmask == cards

    def get_cards(self) -> List[Card]:
        """Get all cards in the deck

        Returns:
            List[Card]: List of cards in the deck
        """
        cards: List[Card] = []
        for card in ALL_CARDS:
            if self.contains(card.key):
                cards.append(card)
        return cards

    def shuffle(self) -> List[Card]:
        """Shuffle the deck"""
        cards = self.get_cards()
        shuffle(cards)
        return cards

    def add_card(self, card: Card) -> None:
        """Add a card to the deck"""
        self.bitmask |= card.key

    def remove_card(self, card: Card) -> None:
        """Remove a card from the deck"""
        self.bitmask &= ~card.key

    def deal_cards(self, count: int = 1) -> int:
        """Deal cards from the deck

        Args:
            count (int, optional): Number of cards to deal. Defaults to 1.

        Returns:
            List[Card]: List of cards dealt
        """
        cards: List[Card] = []
        for _ in range(count):
            card = self.shuffle().pop()
            self.remove_card(card)
            cards.append(card)
        return cards_mask(cards)

    def deal_specific_card(self, card: Card) -> int:
        """Deal a specific card from the deck"""
        if not self.contains(card.key):
            raise ValueError("Card not in deck")
        self.remove_card(card)
        return cards_mask([card])

    def deal_specific_cards(self, cards: List[Card]) -> int:
        """Deal specific cards from the deck"""
        for card in cards:
            self.deal_specific_card(card)
        return cards_mask(cards)
