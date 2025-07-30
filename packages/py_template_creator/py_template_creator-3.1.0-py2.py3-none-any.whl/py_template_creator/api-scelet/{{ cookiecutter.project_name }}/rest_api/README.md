# REST API Service

This is the REST API service for {{ cookiecutter.project_name }}. It provides HTTP endpoints for interacting with the application, built with FastAPI, SQLAlchemy, and Pydantic with built-in authentication.

## Getting Started

### Prerequisites

- Python 3.8+
- uv (Python package installer)
- Docker (for production deployment)

### Installation

1. Navigate to the REST API directory:
```bash
cd rest_api
```

2. Set up the environment using uv:
```bash
make env
```

This will create the necessary uv.lock file and install all dependencies from pyproject.toml.

### Running the Service

#### Development Mode
To start the REST API service in development mode:

```bash
make run
```

#### Production Mode
The service runs in Docker by default for production:

```bash
docker-compose up
```

You can control whether migrations run during container startup using the `RUN_MIGRATIONS` environment variable:
```bash
# Run without migrations
RUN_MIGRATIONS=false docker-compose up

# Run with migrations (default)
RUN_MIGRATIONS=true docker-compose up
```

This is particularly useful when running multiple instances of the application (horizontal scaling).

Both environments use uvicorn as the ASGI server.

### Database Migrations

To manage database migrations:

```bash
# Generate new migrations
make migrations

# Apply migrations
make migrate
```

## API Documentation

### Available Endpoints

The following endpoints are available:

- `GET /health` - Health check endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation
- Authentication endpoints (built-in)
- User management endpoints (built-in)

For detailed API documentation, visit `/docs` or `/redoc` after starting the service.

## Development

### Project Structure

```
rest_api/
├── package/
│   ├── app/
│   │   ├── api/           # API routes and handlers
│   │   ├── auth/          # Authentication and authorization
│   │   ├── cache/         # Caching layer
│   │   ├── managers/      # Business logic
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic models
│   │   ├── services/      # External service integrations
│   │   ├── utils/         # Utility functions
│   │   ├── main.py        # Application entry point
│   │   ├── shell.py       # Custom shell for the project
│   │   ├── settings.py    # Project settings (env variables)
│   │   ├── sync_assets.py # Sync assets with the remote storage (S3, etc.)
│   ├── tests/             # Test files
│   Makefile               # Development commands
└── pyproject.toml         # Project dependencies and configuration
```

### Running Tests

To run the test suite:

```bash
make test
```

### Key Features

- FastAPI for high-performance async API
- SQLAlchemy with type annotations
- Pydantic for data validation
- Built-in authentication system
- Docker support for production
- uv package management for faster dependency resolution

### Configuration

Configuration is handled through environment variables.
.env.example should hold the required variables with mocked values ( if the value is a secret, use a dummy value).
.env should hold the actual values.

### Syncing Assets

Assets are synced with the remote storage (S3, etc.) using the `sync_assets.py` script.

This is a one-way sync, meaning that assets will be uploaded to the remote storage, but not downloaded.
This is useful for templating and one place of control and you do not have to worry about changing the storage ( switching from s3 to azure, etc.)





