# URL Shortener

A FastAPI-based URL shortener with a web UI and DuckDB persistence.

## Features
- **Web Interface:**
    - Single-page application for shortening URLs.
    - Displays a list of previously shortened URLs (last 50).
    - Table view for previously shortened URLs with:
        - Original URL
        - Shortened URL
        - Click Count
    - Table is scrollable with a sticky header.
    - Ability to sort previously shortened URLs by "Click Count".
    - "Delete All Links" functionality with confirmation.
- **Core Functionality:**
    - Shorten any HTTP/HTTPS URL.
    - Redirect via generated short path (e.g., `http://yourdomain/{short_key}`).
    - Tracks visit counts for each shortened URL.
- **Technical Features:**
    - Built with FastAPI, DuckDB, Pydantic, and vanilla JavaScript.
    - Configuration via `.env` file.
    - Rate limiting for API endpoints to prevent abuse.
    - Support for Redis-backed distributed rate limiting.
    - Unit tests with pytest.

## Repository Structure
```
.
├── app
│   ├── core
│   │   ├── config.py       # Environment settings
│   │   └── rate_limiter.py # Rate limiting configuration
│   ├── db
│   │   └── session.py      # DuckDB connection & schema setup
│   ├── models
│   │   └── __init__.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── url.py          # Pydantic models
│   ├── services
│   │   └── url_service.py  # Business logic for URL operations
│   ├── static
│   │   └── styles.css      # CSS for the web UI
│   ├── templates
│   │   └── index.html      # HTML template for the web UI
│   └── routers
│       ├── __init__.py
│       └── url.py          # API endpoints for URL operations
├── tests
│   ├── test_url_service.py # Unit tests for service layer
│   └── test_rate_limiting.py # Unit tests for rate limiting
├── .env.example            # Example environment variables
├── .gitignore
├── architecture.md         # System architecture details
├── LICENSE
├── main.py                 # Application entrypoint
├── mypy.ini                # Mypy configuration
├── README.md               # Project documentation
├── requirements.txt        # Dependencies
└── shorten.py              # CLI tool for shortening URLs (optional)
```

## Getting Started

### Prerequisites
- Python 3.8+
- `pip` package manager

### Installation
1. Clone the repository  
   ```bash
   git clone https://github.com/utkuyucel/url-shortener.git && cd url-shortener
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
   Copy `.env.example` to `.env`:  
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` to customize settings. The most important settings are:
   ```
   DATABASE_URL=duckdb:///./data.db
   HOST=127.0.0.1
   PORT=8000
   RATE_LIMIT_ENABLED=true
   ```
   
   For production environments, configure Redis-backed rate limiting:
   ```
   RATE_LIMIT_STORAGE_URI=redis://localhost:6379/0 # Example for Redis
   ```

### Running the Application
To run the application:
```bash
python main.py
```
Or for development with auto-reload:
```bash
uvicorn main:app --reload
```
The web interface will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
API documentation (Swagger UI) is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
Alternative API documentation (ReDoc) is available at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).


### Testing
```bash
pytest
```

## CLI Usage (Optional)

A command-line tool (`shorten.py`) is available for quickly shortening URLs.

1. Ensure the FastAPI service is running (see "Running the Application").
2. Run the CLI script:
   ```bash
   python shorten.py
   ```
3. Enter the URL when prompted (e.g., `https://example.com`).
4. The script will display the shortened URL. Note that the redirect path is now directly under the root (e.g., `http://127.0.0.1:8000/abc123`), not `/u/abc123`.

## API Endpoints

- `GET /`: Serves the main HTML page for the web UI.
- `GET /{short_key}`: Redirects to the original URL corresponding to `short_key` and increments its visit count.
- `POST /api/v1/url/shorten`: Creates a new shortened URL.
  - Request body: `{ "original_url": "string" }`
  - Response: `{ "id": 0, "original_url": "string", "short_path": "string", "created_at": "string", "visit_count": 0 }`
- `GET /api/v1/urls`: Fetches a list of previously shortened URLs (default last 50).
- `DELETE /api/v1/urls`: Deletes all shortened URLs.
- `GET /api/v1/urls/{short_path}/info`: Fetches metadata for a specific shortened URL.

## System Design

### Architecture Overview
The application follows a standard three-tier architecture:
1.  **Presentation Layer:** A web UI built with HTML, CSS, and vanilla JavaScript, served by FastAPI.
2.  **Application/Service Layer:** FastAPI handles API requests, routing, and business logic located in `app/services/`.
3.  **Data Layer:** DuckDB is used for data persistence, managed via `app/db/session.py`.

## Rate Limiting

The URL Shortener implements configurable rate limiting to prevent abuse and ensure service stability:

- IP-based rate limiting for all endpoints
- Configurable limits per endpoint type
- Support for in-memory or Redis-backed storage
- Comprehensive rate limit headers (X-RateLimit-*)
- Graceful 429 responses with retry information

For detailed information, see [Rate Limiting Documentation](docs/rate_limiting.md).


The URL Shortener is structured as a modular, layered system:
- **Web UI (HTML/CSS/JS):** Provides the user interface for interacting with the shortener.
- **API Layer (FastAPI):** Handles HTTP requests from the UI and other clients, routing, and OpenAPI docs.
- **Service Layer (`app/services/url_service.py`):** Contains the core business logic for URL creation, retrieval, visit incrementing, and deletion.
- **Data Access Layer (`app/db/session.py`):** Manages the DuckDB connection and executes SQL queries for data persistence.
- **Configuration (`app/core/config.py`):** Manages application settings via environment variables.
- **CLI Client (`shorten.py`):** An optional tool for command-line URL shortening.

### Data Flow

1.  **User visits Web UI (`GET /`):** FastAPI serves `index.html`.
2.  **Shorten URL (via UI):**
    *   User submits a URL in the form.
    *   JavaScript sends a `POST` request to `/api/v1/url/shorten` with the original URL.
    *   The service layer generates a unique short path, stores the mapping and initial visit count (0) in the `urls` table in DuckDB.
    *   The API returns the shortened URL details (including the short path).
    *   The UI displays the shortened URL and updates the list of previous URLs.
3.  **Redirect Short URL (`GET /{short_key}`):**
    *   User clicks or navigates to a short URL (e.g., `http://localhost:8000/xyz123`).
    *   FastAPI routes the request.
    *   The service layer retrieves the original URL from DuckDB using `short_key`.
    *   The `visit_count` for that URL is incremented in the database.
    *   An HTTP 307 redirect is issued to the original URL.
4.  **List URLs (via UI):**
    *   On page load or after an action, JavaScript sends a `GET` request to `/api/v1/urls`.
    *   The service layer fetches the latest (e.g., 50) URLs from DuckDB.
    *   The API returns the list of URL details.
    *   The UI renders the table, allowing sorting by click count.
5.  **Delete All URLs (via UI):**
    *   User clicks "Delete All Links" and confirms.
    *   JavaScript sends a `DELETE` request to `/api/v1/urls`.
    *   The service layer executes a `DELETE FROM urls` statement in DuckDB.
    *   The UI refreshes the (now empty) list of URLs.

### Scalability and Performance

- **Stateless API Servers:** FastAPI application can be scaled horizontally behind a load balancer if DuckDB is replaced with a shared database.
- **Persistent Storage:** DuckDB provides good performance for single-node deployments. For larger scale, consider a distributed database (e.g., PostgreSQL, MySQL, or a NoSQL solution).
- **Asynchronous Operations:** FastAPI's async capabilities are utilized for non-blocking I/O.

### Database Schema

The application uses a single table named `urls` in DuckDB:

| Column         | Type      | Constraints          | Description                       |
|----------------|-----------|----------------------|-----------------------------------|
| `id`           | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for the record  |
| `original_url` | `TEXT`    | `NOT NULL`           | The original, long URL            |
| `short_path`   | `TEXT`    | `NOT NULL UNIQUE`    | The generated short identifier    |
| `created_at`   | `TIMESTAMP`| `DEFAULT CURRENT_TIMESTAMP` | Timestamp of creation             |
| `visit_count`  | `INTEGER` | `NOT NULL DEFAULT 0` | Number of times the link was visited |

### Extensibility

- Add user authentication for user-specific links.
- Support custom aliases and expiration policies.
- Deploy on Kubernetes for zero-downtime scaling.

## License
This project is licensed under the MIT License.
