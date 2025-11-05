"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.config import settings
from app.csv_processor import CSVProcessor
from app.firebase_client import firebase_client
from app.logging_config import setup_logging
from app.models import (
    CSVUploadResponse,
    GameRecord,
    HandEvaluationRequest,
    HandEvaluationResponse,
)
from app.poker import Card, Poker

# Setup structured logging
setup_logging(level="DEBUG" if settings.debug else "INFO")
logger = logging.getLogger(__name__)

# Initialize services
poker = Poker()
csv_processor = CSVProcessor()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifespan."""
    # Startup
    logger.info("Starting application...")
    firebase_client.initialize()
    logger.info("Application started successfully")
    yield
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="FastAPI application with Poker logic, Firebase, and CSV processing",
    version="0.1.0",
    debug=settings.debug,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Welcome to Poker API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/evaluate", response_model=HandEvaluationResponse)
async def evaluate_hand(request: HandEvaluationRequest) -> HandEvaluationResponse:
    """
    Evaluate a poker hand.

    Args:
        request: Hand evaluation request with 5 cards

    Returns:
        Hand evaluation result with rank and description
    """
    try:
        # Convert CardModels to Card objects
        cards = [Card(card_model.rank, card_model.suit) for card_model in request.cards]

        # Evaluate hand
        rank, description = poker.evaluate_hand(cards)

        logger.info(f"Evaluated hand: {description}")

        return HandEvaluationResponse(rank=rank, description=description, cards=request.cards)

    except Exception as e:
        logger.error(f"Error evaluating hand: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/game/save")
async def save_game(record: GameRecord) -> dict[str, str]:
    """
    Save a game record to Firebase.

    Args:
        record: Game record to save

    Returns:
        Success message with document ID
    """
    try:
        # Evaluate hand if not already done
        if not record.result:
            cards = [Card(card.rank, card.suit) for card in record.hand]
            rank, description = poker.evaluate_hand(cards)
            record.result = rank
            record.description = description

        doc_id = await firebase_client.save_game_record(record)

        if doc_id:
            return {"message": "Game record saved successfully", "id": doc_id}
        else:
            return {"message": "Game record saved locally (Firebase not configured)", "id": "N/A"}

    except Exception as e:
        logger.error(f"Error saving game: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/game/records")
async def get_game_records(limit: int = 10, player_name: str | None = None) -> list[dict]:
    """
    Get game records from Firebase.

    Args:
        limit: Maximum number of records to return
        player_name: Optional filter by player name

    Returns:
        List of game records
    """
    try:
        records = await firebase_client.get_game_records(limit=limit, player_name=player_name)
        return records
    except Exception as e:
        logger.error(f"Error retrieving game records: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/csv/upload", response_model=CSVUploadResponse)
async def upload_csv(file: UploadFile = File(...)) -> CSVUploadResponse:
    """
    Upload and process a CSV file with poker game data.

    Args:
        file: CSV file to process

    Returns:
        Processing results with summary statistics
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="File must be a CSV")

        # Read file content
        content = await file.read()

        # Process CSV
        records, summary = csv_processor.process_csv(content)

        # Save records to Firebase
        saved_count = 0
        for record in records:
            doc_id = await firebase_client.save_game_record(record)
            if doc_id:
                saved_count += 1

        logger.info(f"Processed {len(records)} records, saved {saved_count} to Firebase")

        return CSVUploadResponse(
            message=f"Successfully processed {len(records)} records",
            rows_processed=len(records),
            summary=summary,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/csv/sample")
async def download_sample_csv() -> Response:
    """
    Download a sample CSV file for testing.

    Returns:
        Sample CSV file
    """
    try:
        csv_content = csv_processor.generate_sample_csv()
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sample_poker_data.csv"},
        )
    except Exception as e:
        logger.error(f"Error generating sample CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
