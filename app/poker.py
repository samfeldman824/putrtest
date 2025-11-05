"""Poker game business logic."""

from enum import Enum


class Suit(str, Enum):
    """Card suits."""

    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"


class Rank(str, Enum):
    """Card ranks."""

    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class HandRank(str, Enum):
    """Poker hand rankings."""

    HIGH_CARD = "high_card"
    PAIR = "pair"
    TWO_PAIR = "two_pair"
    THREE_OF_A_KIND = "three_of_a_kind"
    STRAIGHT = "straight"
    FLUSH = "flush"
    FULL_HOUSE = "full_house"
    FOUR_OF_A_KIND = "four_of_a_kind"
    STRAIGHT_FLUSH = "straight_flush"
    ROYAL_FLUSH = "royal_flush"


class Card:
    """Represents a playing card."""

    def __init__(self, rank: Rank, suit: Suit) -> None:
        """Initialize a card with rank and suit."""
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        """String representation of the card."""
        return f"{self.rank.value}{self.suit.value[0].upper()}"

    def __repr__(self) -> str:
        """Representation of the card."""
        return f"Card({self.rank.value}, {self.suit.value})"


class Poker:
    """Poker game logic and hand evaluation."""

    RANK_VALUES = {
        Rank.TWO: 2,
        Rank.THREE: 3,
        Rank.FOUR: 4,
        Rank.FIVE: 5,
        Rank.SIX: 6,
        Rank.SEVEN: 7,
        Rank.EIGHT: 8,
        Rank.NINE: 9,
        Rank.TEN: 10,
        Rank.JACK: 11,
        Rank.QUEEN: 12,
        Rank.KING: 13,
        Rank.ACE: 14,
    }

    def __init__(self) -> None:
        """Initialize the Poker game."""
        self.deck: list[Card] = []

    def create_deck(self) -> list[Card]:
        """Create a standard 52-card deck."""
        self.deck = [Card(rank, suit) for suit in Suit for rank in Rank]
        return self.deck

    def evaluate_hand(self, cards: list[Card]) -> tuple[HandRank, str]:
        """
        Evaluate a poker hand and return its rank.

        Args:
            cards: List of Card objects (5 cards)

        Returns:
            Tuple of (HandRank, description)
        """
        if len(cards) != 5:
            raise ValueError("A poker hand must contain exactly 5 cards")

        # Sort cards by rank value
        sorted_cards = sorted(cards, key=lambda c: self.RANK_VALUES[c.rank], reverse=True)

        # Check for various hand types
        if self._is_royal_flush(sorted_cards):
            return HandRank.ROYAL_FLUSH, "Royal Flush"
        if self._is_straight_flush(sorted_cards):
            return HandRank.STRAIGHT_FLUSH, "Straight Flush"
        if self._is_four_of_a_kind(sorted_cards):
            return HandRank.FOUR_OF_A_KIND, "Four of a Kind"
        if self._is_full_house(sorted_cards):
            return HandRank.FULL_HOUSE, "Full House"
        if self._is_flush(sorted_cards):
            return HandRank.FLUSH, "Flush"
        if self._is_straight(sorted_cards):
            return HandRank.STRAIGHT, "Straight"
        if self._is_three_of_a_kind(sorted_cards):
            return HandRank.THREE_OF_A_KIND, "Three of a Kind"
        if self._is_two_pair(sorted_cards):
            return HandRank.TWO_PAIR, "Two Pair"
        if self._is_pair(sorted_cards):
            return HandRank.PAIR, "Pair"

        return HandRank.HIGH_CARD, f"High Card: {sorted_cards[0].rank.value}"

    def _is_flush(self, cards: list[Card]) -> bool:
        """Check if all cards have the same suit."""
        return len({card.suit for card in cards}) == 1

    def _is_straight(self, cards: list[Card]) -> bool:
        """Check if cards form a straight."""
        values = sorted([self.RANK_VALUES[card.rank] for card in cards])
        return values == list(range(values[0], values[0] + 5))

    def _is_straight_flush(self, cards: list[Card]) -> bool:
        """Check if cards form a straight flush."""
        return self._is_straight(cards) and self._is_flush(cards)

    def _is_royal_flush(self, cards: list[Card]) -> bool:
        """Check if cards form a royal flush."""
        if not self._is_straight_flush(cards):
            return False
        values = [self.RANK_VALUES[card.rank] for card in cards]
        return min(values) == 10 and max(values) == 14

    def _get_rank_counts(self, cards: list[Card]) -> dict[Rank, int]:
        """Get count of each rank in the hand."""
        counts: dict[Rank, int] = {}
        for card in cards:
            counts[card.rank] = counts.get(card.rank, 0) + 1
        return counts

    def _is_four_of_a_kind(self, cards: list[Card]) -> bool:
        """Check if hand contains four of a kind."""
        counts = self._get_rank_counts(cards)
        return 4 in counts.values()

    def _is_full_house(self, cards: list[Card]) -> bool:
        """Check if hand is a full house."""
        counts = self._get_rank_counts(cards)
        return sorted(counts.values()) == [2, 3]

    def _is_three_of_a_kind(self, cards: list[Card]) -> bool:
        """Check if hand contains three of a kind."""
        counts = self._get_rank_counts(cards)
        return 3 in counts.values()

    def _is_two_pair(self, cards: list[Card]) -> bool:
        """Check if hand contains two pairs."""
        counts = self._get_rank_counts(cards)
        pairs = [count for count in counts.values() if count == 2]
        return len(pairs) == 2

    def _is_pair(self, cards: list[Card]) -> bool:
        """Check if hand contains a pair."""
        counts = self._get_rank_counts(cards)
        return 2 in counts.values()
