"""Pydantic models for data validation."""

from pydantic import BaseModel, ConfigDict, Field

from app.poker import HandRank, Rank, Suit


class CardModel(BaseModel):
    """Model for a playing card."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rank": "A",
                "suit": "spades",
            }
        }
    )

    rank: Rank
    suit: Suit


class HandEvaluationRequest(BaseModel):
    """Request model for hand evaluation."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "cards": [
                    {"rank": "A", "suit": "spades"},
                    {"rank": "K", "suit": "spades"},
                    {"rank": "Q", "suit": "spades"},
                    {"rank": "J", "suit": "spades"},
                    {"rank": "10", "suit": "spades"},
                ]
            }
        }
    )

    cards: list[CardModel] = Field(..., min_length=5, max_length=5)


class HandEvaluationResponse(BaseModel):
    """Response model for hand evaluation."""

    rank: HandRank
    description: str
    cards: list[CardModel]


class GameRecord(BaseModel):
    """Model for storing game records."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "player_name": "John Doe",
                "hand": [
                    {"rank": "A", "suit": "hearts"},
                    {"rank": "A", "suit": "diamonds"},
                    {"rank": "K", "suit": "hearts"},
                    {"rank": "K", "suit": "clubs"},
                    {"rank": "Q", "suit": "hearts"},
                ],
                "result": "two_pair",
                "description": "Two Pair",
            }
        }
    )

    id: str | None = None
    player_name: str
    hand: list[CardModel]
    result: HandRank
    description: str
    timestamp: str | None = None


class CSVUploadResponse(BaseModel):
    """Response model for CSV upload."""

    message: str
    rows_processed: int
    summary: dict[str, int]
