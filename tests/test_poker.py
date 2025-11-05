"""Tests for poker game logic."""

import pytest

from app.poker import Card, HandRank, Poker, Rank, Suit


class TestPoker:
    """Test cases for Poker class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.poker = Poker()

    def test_create_deck(self) -> None:
        """Test deck creation."""
        deck = self.poker.create_deck()
        assert len(deck) == 52
        assert all(isinstance(card, Card) for card in deck)

    def test_royal_flush(self) -> None:
        """Test royal flush detection."""
        cards = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.ROYAL_FLUSH
        assert "Royal Flush" in description

    def test_straight_flush(self) -> None:
        """Test straight flush detection."""
        cards = [
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.EIGHT, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.HEARTS),
            Card(Rank.SIX, Suit.HEARTS),
            Card(Rank.FIVE, Suit.HEARTS),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.STRAIGHT_FLUSH
        assert "Straight Flush" in description

    def test_four_of_a_kind(self) -> None:
        """Test four of a kind detection."""
        cards = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.CLUBS),
            Card(Rank.KING, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.FOUR_OF_A_KIND
        assert "Four of a Kind" in description

    def test_full_house(self) -> None:
        """Test full house detection."""
        cards = [
            Card(Rank.KING, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.FULL_HOUSE
        assert "Full House" in description

    def test_flush(self) -> None:
        """Test flush detection."""
        cards = [
            Card(Rank.ACE, Suit.CLUBS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.NINE, Suit.CLUBS),
            Card(Rank.SIX, Suit.CLUBS),
            Card(Rank.THREE, Suit.CLUBS),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.FLUSH
        assert "Flush" in description

    def test_straight(self) -> None:
        """Test straight detection."""
        cards = [
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.EIGHT, Suit.DIAMONDS),
            Card(Rank.SEVEN, Suit.CLUBS),
            Card(Rank.SIX, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.STRAIGHT
        assert "Straight" in description

    def test_three_of_a_kind(self) -> None:
        """Test three of a kind detection."""
        cards = [
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.SEVEN, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.KING, Suit.CLUBS),
            Card(Rank.THREE, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.THREE_OF_A_KIND
        assert "Three of a Kind" in description

    def test_two_pair(self) -> None:
        """Test two pair detection."""
        cards = [
            Card(Rank.JACK, Suit.SPADES),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.THREE, Suit.DIAMONDS),
            Card(Rank.THREE, Suit.CLUBS),
            Card(Rank.TWO, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.TWO_PAIR
        assert "Two Pair" in description

    def test_pair(self) -> None:
        """Test pair detection."""
        cards = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.JACK, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.PAIR
        assert "Pair" in description

    def test_high_card(self) -> None:
        """Test high card detection."""
        cards = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.NINE, Suit.SPADES),
        ]
        rank, description = self.poker.evaluate_hand(cards)
        assert rank == HandRank.HIGH_CARD
        assert "High Card" in description

    def test_invalid_hand_size(self) -> None:
        """Test that invalid hand size raises error."""
        cards = [
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.KING, Suit.HEARTS),
        ]
        with pytest.raises(ValueError, match="must contain exactly 5 cards"):
            self.poker.evaluate_hand(cards)
