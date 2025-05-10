%%{ init: { "theme": "default", "flowchart": { "curve": "linear", "diagramPadding": 10, "htmlLabels": true, "nodeSpacing": 40 }}}%%
flowchart LR
    subgraph A[Presentation Layer / Clients]
        direction TB
        CLI[CLI Client<br><code>shorten.py</code>]:::client
        Web[Web Client / Browser]:::client
    end

    subgraph B[Application/Service Layer]
        direction TB
        Main[FastAPI App<br><code>main.py</code>]:::api
        Routers[API Routers<br><code>routers/url.py</code>]:::api
        Service[Service Layer<br><code>url_service.py</code>]:::service
        Config[Config Loader<br><code>core/config.py</code>]:::config
        RateLimiter[Rate Limiter<br><code>core/rate_limiter.py</code>]:::service
    end

    subgraph C[Data Layer]
        direction TB
        DAL[Data Access Layer<br><code>db/session.py</code>]:::db
        DB[(DuckDB<br><code>data.db</code>)]:::db
        URLs["Table: urls<br><small><code>id, original_url, short_path, created_at, visit_count</code></small>"]:::table
    end

    subgraph D[Optional External Services]
        direction TB
        Redis[(Redis<br><small>Optional for Rate Limiting</small>)]:::external
    end

    %% Connections
    CLI --> Main
    Web --> Main
    Main --> Routers
    Main --> Config
    Routers --> Service
    Service --> DAL
    Service --> RateLimiter
    RateLimiter --> Redis
    DAL --> DB
    DB --> URLs

    %% Styles
    classDef client fill:#fdf6e3,stroke:#657b83,stroke-width:1px;
    classDef api fill:#e0f7fa,stroke:#00796b,stroke-width:1px;
    classDef service fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;
    classDef db fill:#ede7f6,stroke:#5e35b1,stroke-width:1px;
    classDef config fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px;
    classDef table fill:#fffde7,stroke:#fbc02d,stroke-width:1px;
    classDef external fill:#f5f5f5,stroke:#757575,stroke-width:1px;
