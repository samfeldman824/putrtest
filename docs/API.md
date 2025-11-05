# API Documentation

## Base URL

- Local: `http://localhost:8000`
- Production: `https://your-app.railway.app`

## Authentication

Currently, the API does not require authentication. For production use, consider adding API keys or OAuth.

## Endpoints

### Health Check

Check if the API is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

### Evaluate Poker Hand

Evaluate a 5-card poker hand and return its rank.

**Endpoint:** `POST /evaluate`

**Request Body:**
```json
{
  "cards": [
    {"rank": "A", "suit": "spades"},
    {"rank": "K", "suit": "spades"},
    {"rank": "Q", "suit": "spades"},
    {"rank": "J", "suit": "spades"},
    {"rank": "10", "suit": "spades"}
  ]
}
```

**Valid Ranks:** `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `J`, `Q`, `K`, `A`

**Valid Suits:** `hearts`, `diamonds`, `clubs`, `spades`

**Response:**
```json
{
  "rank": "royal_flush",
  "description": "Royal Flush",
  "cards": [...]
}
```

**Hand Rankings (from highest to lowest):**
- `royal_flush` - Royal Flush
- `straight_flush` - Straight Flush
- `four_of_a_kind` - Four of a Kind
- `full_house` - Full House
- `flush` - Flush
- `straight` - Straight
- `three_of_a_kind` - Three of a Kind
- `two_pair` - Two Pair
- `pair` - Pair
- `high_card` - High Card

### Save Game Record

Save a game record to Firebase Firestore.

**Endpoint:** `POST /game/save`

**Request Body:**
```json
{
  "player_name": "John Doe",
  "hand": [
    {"rank": "A", "suit": "hearts"},
    {"rank": "A", "suit": "diamonds"},
    {"rank": "K", "suit": "clubs"},
    {"rank": "Q", "suit": "spades"},
    {"rank": "J", "suit": "hearts"}
  ],
  "result": "pair",
  "description": "Pair"
}
```

**Response:**
```json
{
  "message": "Game record saved successfully",
  "id": "abc123xyz"
}
```

### Get Game Records

Retrieve game records from Firebase Firestore.

**Endpoint:** `GET /game/records`

**Query Parameters:**
- `limit` (optional): Maximum number of records to return (default: 10)
- `player_name` (optional): Filter by player name

**Example:**
```
GET /game/records?limit=5&player_name=John%20Doe
```

**Response:**
```json
[
  {
    "id": "abc123",
    "player_name": "John Doe",
    "hand": [...],
    "result": "pair",
    "description": "Pair",
    "timestamp": "2024-01-01T12:00:00Z"
  }
]
```

### Upload CSV

Upload a CSV file containing poker game data for batch processing.

**Endpoint:** `POST /csv/upload`

**Content-Type:** `multipart/form-data`

**Form Data:**
- `file`: CSV file

**CSV Format:**
```csv
player_name,card1_rank,card1_suit,card2_rank,card2_suit,card3_rank,card3_suit,card4_rank,card4_suit,card5_rank,card5_suit
Alice,A,hearts,A,diamonds,A,clubs,K,hearts,Q,spades
Bob,K,spades,K,hearts,K,diamonds,K,clubs,J,hearts
```

**Response:**
```json
{
  "message": "Successfully processed 2 records",
  "rows_processed": 2,
  "summary": {
    "three_of_a_kind": 1,
    "four_of_a_kind": 1
  }
}
```

### Download Sample CSV

Download a sample CSV file for testing.

**Endpoint:** `GET /csv/sample`

**Response:** CSV file download

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid input)
- `422` - Validation Error (Pydantic validation failed)
- `500` - Internal Server Error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production use.

## CORS

CORS is configured to allow all origins by default. Update `CORS_ORIGINS` in settings for production.

## Interactive Documentation

The API provides interactive documentation:

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI Schema: `/openapi.json`
