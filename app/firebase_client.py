"""Firebase Firestore client for database operations."""

import logging
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore

from app.config import settings
from app.models import GameRecord

logger = logging.getLogger(__name__)


class FirebaseClient:
    """Client for Firebase Firestore operations."""

    def __init__(self) -> None:
        """Initialize Firebase client."""
        self.db: firestore.Client | None = None
        self._initialized = False

    def initialize(self) -> None:
        """Initialize Firebase Admin SDK."""
        if self._initialized:
            return

        try:
            if settings.firebase_credentials_path:
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
            else:
                # Use default credentials (for Railway deployment)
                firebase_admin.initialize_app()

            self.db = firestore.client()
            self._initialized = True
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.warning(f"Firebase initialization failed: {e}. Running without Firebase.")
            self.db = None

    async def save_game_record(self, record: GameRecord) -> str | None:
        """
        Save a game record to Firestore.

        Args:
            record: GameRecord to save

        Returns:
            Document ID if saved successfully, None otherwise
        """
        if not self.db:
            logger.warning("Firebase not initialized, skipping save")
            return None

        try:
            record_dict = record.model_dump(exclude_none=True)
            record_dict["timestamp"] = datetime.now().astimezone().isoformat()

            doc_ref = self.db.collection("game_records").document()
            doc_ref.set(record_dict)

            doc_id: str = str(doc_ref.id)
            logger.info(f"Saved game record with ID: {doc_id}")
            return doc_id
        except Exception as e:
            logger.error(f"Failed to save game record: {e}")
            return None

    async def get_game_records(self, limit: int = 10, player_name: str | None = None) -> list[dict]:
        """
        Get game records from Firestore.

        Args:
            limit: Maximum number of records to return
            player_name: Optional filter by player name

        Returns:
            List of game records
        """
        if not self.db:
            logger.warning("Firebase not initialized, returning empty list")
            return []

        try:
            query = self.db.collection("game_records")

            if player_name:
                query = query.where("player_name", "==", player_name)

            query = query.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit)

            docs = query.stream()
            records = []
            for doc in docs:
                record = doc.to_dict()
                record["id"] = doc.id
                records.append(record)

            logger.info(f"Retrieved {len(records)} game records")
            return records
        except Exception as e:
            logger.error(f"Failed to get game records: {e}")
            return []


# Singleton instance
firebase_client = FirebaseClient()
