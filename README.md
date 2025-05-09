# URL Shortener

A professional FastAPI-based URL shortener with DuckDB persistence.

## Features
- Shorten any HTTP/HTTPS URL
- Redirect via generated short path
- Retrieve URL metadata and visit counts
- Built with FastAPI, DuckDB, and Pydantic
- Configuration via `.env`
- Comprehensive unit tests with pytest

## Repository Structure
```
.
├── app
│   ├── core
│   │   └── config.py       # Environment settings
│   ├── db
│   │   └── session.py      # DuckDB connection & schema setup
│   ├── models
│   │   └── __init__.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── url.py          # Pydantic models
│   ├── services
│   │   └── url_service.py  # Business logic: create/get/increment
│   └── routers
│       ├── __init__.py     # API router inclusion
│       └── url.py          # URL endpoints
├── tests
│   └── test_url_service.py # Unit tests for service layer
├── .env                    # Environment variables
├── main.py                 # Application entrypoint
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── LICENSE
```

## Getting Started

### Prerequisites
- Python 3.8+
- `pip` package manager

### Installation
1. Clone the repository  
   ```bash
   git clone <repo-url> && cd url-shortener
   ```
2. Create and activate a virtual environment  
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables  
   Copy `.env.example` to `.env` (if provided) or create `.env` with:  
   ```
   DATABASE_URL=duckdb:///./data.db
   HOST=127.0.0.1
   PORT=8000
   ```

### Running the Application
```bash
uvicorn main:app --reload
```
API docs available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Testing
```bash
pytest
```

## CLI Usage

To shorten a URL via the command-line tool:

1. Ensure the FastAPI service is running:
   ```bash
   python -m uvicorn main:app --reload
   ```
2. Run the CLI script:
   ```bash
   python shorten.py
   ```
3. Enter the URL when prompted (e.g., `https://example.com`).
4. The script will display the shortened URL:
   ```
   Short URL: http://127.0.0.1:8000/u/abc123
   ```

## License
This project is licensed under the MIT License.
