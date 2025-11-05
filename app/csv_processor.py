"""CSV processing utilities using Pandas."""

import io
import logging

import pandas as pd

from app.models import CardModel, GameRecord
from app.poker import Card, Poker, Rank, Suit

logger = logging.getLogger(__name__)


class CSVProcessor:
    """Process CSV files containing poker game data."""

    def __init__(self) -> None:
        """Initialize CSV processor."""
        self.poker = Poker()

    def process_csv(self, file_content: bytes) -> tuple[list[GameRecord], dict[str, int]]:
        """
        Process CSV file and return game records.

        Expected CSV format:
        player_name,card1_rank,card1_suit,card2_rank,card2_suit,...,card5_rank,card5_suit

        Args:
            file_content: Raw bytes of the CSV file

        Returns:
            Tuple of (list of GameRecords, summary statistics)
        """
        try:
            # Read CSV
            df = pd.read_csv(io.BytesIO(file_content))

            # Validate required columns
            required_columns = ["player_name"] + [
                f"card{i}_{field}" for i in range(1, 6) for field in ["rank", "suit"]
            ]

            missing_columns = set(required_columns) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")

            records: list[GameRecord] = []
            summary: dict[str, int] = {}

            # Process each row
            for _, row in df.iterrows():
                try:
                    # Extract cards
                    cards: list[Card] = []
                    for i in range(1, 6):
                        rank_str = str(row[f"card{i}_rank"]).strip().upper()
                        suit_str = str(row[f"card{i}_suit"]).strip().lower()

                        rank = self._parse_rank(rank_str)
                        suit = self._parse_suit(suit_str)

                        cards.append(Card(rank, suit))

                    # Evaluate hand
                    hand_rank, description = self.poker.evaluate_hand(cards)

                    # Create record
                    card_models = [CardModel(rank=c.rank, suit=c.suit) for c in cards]
                    record = GameRecord(
                        player_name=str(row["player_name"]),
                        hand=card_models,
                        result=hand_rank,
                        description=description,
                    )

                    records.append(record)

                    # Update summary
                    summary[hand_rank.value] = summary.get(hand_rank.value, 0) + 1

                except Exception as e:
                    logger.error(f"Error processing row: {e}")
                    continue

            logger.info(f"Processed {len(records)} records from CSV")
            return records, summary

        except Exception as e:
            logger.error(f"Error processing CSV: {e}")
            raise ValueError(f"Failed to process CSV: {str(e)}")

    def _parse_rank(self, rank_str: str) -> Rank:
        """Parse rank string to Rank enum."""
        rank_mapping = {
            "2": Rank.TWO,
            "3": Rank.THREE,
            "4": Rank.FOUR,
            "5": Rank.FIVE,
            "6": Rank.SIX,
            "7": Rank.SEVEN,
            "8": Rank.EIGHT,
            "9": Rank.NINE,
            "10": Rank.TEN,
            "J": Rank.JACK,
            "Q": Rank.QUEEN,
            "K": Rank.KING,
            "A": Rank.ACE,
        }

        if rank_str not in rank_mapping:
            raise ValueError(f"Invalid rank: {rank_str}")

        return rank_mapping[rank_str]

    def _parse_suit(self, suit_str: str) -> Suit:
        """Parse suit string to Suit enum."""
        suit_mapping = {
            "hearts": Suit.HEARTS,
            "diamonds": Suit.DIAMONDS,
            "clubs": Suit.CLUBS,
            "spades": Suit.SPADES,
            "h": Suit.HEARTS,
            "d": Suit.DIAMONDS,
            "c": Suit.CLUBS,
            "s": Suit.SPADES,
        }

        if suit_str not in suit_mapping:
            raise ValueError(f"Invalid suit: {suit_str}")

        return suit_mapping[suit_str]

    def generate_sample_csv(self) -> bytes:
        """Generate a sample CSV file for testing."""
        data = {
            "player_name": ["Alice", "Bob", "Charlie"],
            "card1_rank": ["A", "K", "2"],
            "card1_suit": ["hearts", "spades", "clubs"],
            "card2_rank": ["A", "K", "3"],
            "card2_suit": ["diamonds", "hearts", "clubs"],
            "card3_rank": ["A", "K", "4"],
            "card3_suit": ["clubs", "diamonds", "clubs"],
            "card4_rank": ["K", "K", "5"],
            "card4_suit": ["hearts", "clubs", "clubs"],
            "card5_rank": ["Q", "J", "6"],
            "card5_suit": ["spades", "hearts", "clubs"],
        }

        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode("utf-8")
