%%{ init: { "theme": "default", "flowchart": { "curve": "linear", "diagramPadding": 10, "htmlLabels": true, "nodeSpacing": 40 }}}%%
flowchart LR
    subgraph A[Clients]
        direction TB
        CLI[CLI Client<br><code>shorten.py</code>]:::client
        Web[Web Client / Browser]:::client
    end

    subgraph B[FastAPI Application]
        direction TB
        Main[FastAPI App<br><code>main.py</code>]:::api
        Routers[API Routers<br><code>routers/url.py</code>]:::api
        Service[Service Layer<br><code>url_service.py</code>]:::service
        Config[Config Loader<br><code>core/config.py</code>]:::config
    end

    subgraph C[Persistence Layer]
        direction TB
        DAL[Data Access Layer<br><code>db/session.py</code>]:::db
        DB[(DuckDB<br><code>data.db</code>)]:::db
        URLs["Table: urls<br><small><code>key, original_url, created_at</code></small>"]:::table
        Visits["Table: visits<br><small><code>key, count</code></small>"]:::table
    end

    %% Connections
    CLI --> Main
    Web --> Main
    Main --> Routers
    Main --> Config
    Routers --> Service
    Service --> DAL
    DAL --> DB
    DB --> URLs
    DB --> Visits

    %% Styles
    classDef client fill:#fdf6e3,stroke:#657b83,stroke-width:1px;
    classDef api fill:#e0f7fa,stroke:#00796b,stroke-width:1px;
    classDef service fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;
    classDef db fill:#ede7f6,stroke:#5e35b1,stroke-width:1px;
    classDef config fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px;
    classDef table fill:#fffde7,stroke:#fbc02d,stroke-width:1px;
