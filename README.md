# Poker API

A production-ready FastAPI application featuring poker hand evaluation, Firebase integration, and CSV processing capabilities.

## 🚀 Features

- **FastAPI Framework**: Modern, high-performance web framework
- **Data Validation**: Pydantic for robust data models
- **Database**: Firebase Firestore integration
- **CSV Processing**: Pandas-powered data processing
- **Poker Logic**: Complete poker hand evaluation system
- **Structured Logging**: JSON-formatted logs for production
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Ruff, Black, MyPy, and Bandit
- **CI/CD**: GitHub Actions workflow
- **Deployment**: Railway.app ready with Procfile

## 📋 Tech Stack

- **Framework**: FastAPI
- **Data Validation**: Pydantic
- **Database**: Firebase (Firestore)
- **Hosting**: Railway.app
- **CSV Processing**: Pandas
- **Linting**: Ruff + Black
- **Type Checking**: MyPy
- **Security Scanning**: Bandit
- **Testing**: Pytest
- **Logging**: Python built-in (structured JSON)
- **Frontend Hosting**: GitHub Pages

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/samfeldman824/putrtest.git
cd putrtest
```

2. Install dependencies:
```bash
pip install -e ".[dev]"
```

3. Copy the environment file and configure:
```bash
cp .env.example .env
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## 🎮 API Endpoints

### Health Check
```bash
GET /health
```

### Evaluate Poker Hand
```bash
POST /evaluate
Content-Type: application/json

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

### Save Game Record
```bash
POST /game/save
Content-Type: application/json

{
  "player_name": "John Doe",
  "hand": [...],
  "result": "royal_flush",
  "description": "Royal Flush"
}
```

### Get Game Records
```bash
GET /game/records?limit=10&player_name=John%20Doe
```

### Upload CSV
```bash
POST /csv/upload
Content-Type: multipart/form-data

file: poker_data.csv
```

### Download Sample CSV
```bash
GET /csv/sample
```

## 🧪 Testing

Run tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

Run specific tests:
```bash
pytest tests/test_poker.py
pytest tests/test_api.py
```

## 🔍 Code Quality

### Linting
```bash
# Run Ruff
ruff check .

# Auto-fix issues
ruff check . --fix
```

### Formatting
```bash
# Check formatting
black --check .

# Format code
black .
```

### Type Checking
```bash
mypy app tests
```

### Security Scanning
```bash
bandit -r app
```

## 🚢 Deployment

### Railway.app

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Railway will automatically detect the `Procfile` and deploy

### Firebase Configuration

1. Create a Firebase project
2. Download service account credentials
3. Set environment variables:
   - `FIREBASE_CREDENTIALS_PATH`: Path to credentials JSON
   - `FIREBASE_PROJECT_ID`: Your project ID

## 🌐 Frontend

The frontend is a static HTML page that can be hosted on GitHub Pages:

1. Go to repository Settings > Pages
2. Set source to `main` branch and `/frontend` folder
3. Save and visit your GitHub Pages URL

Update the `API_URL` in `frontend/index.html` to point to your Railway deployment.

## 📊 CSV Format

Expected CSV format for batch processing:

```csv
player_name,card1_rank,card1_suit,card2_rank,card2_suit,card3_rank,card3_suit,card4_rank,card4_suit,card5_rank,card5_suit
Alice,A,hearts,A,diamonds,A,clubs,K,hearts,Q,spades
Bob,K,spades,K,hearts,K,diamonds,K,clubs,J,hearts
```

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
APP_NAME="Poker API"
DEBUG=false
HOST=0.0.0.0
PORT=8000
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
FIREBASE_PROJECT_ID=your-project-id
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linters
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Railway Documentation](https://docs.railway.app/)

## 📞 Support

For issues and questions, please open an issue on GitHub.