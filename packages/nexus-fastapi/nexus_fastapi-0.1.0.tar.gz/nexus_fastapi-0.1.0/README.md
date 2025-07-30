# Nexus-FastAPI

A powerful FastAPI project generator and framework that helps you create scalable and maintainable FastAPI applications.

## Features

- Automatic project scaffolding
- Database integration with SQLAlchemy
- Automatic table creation
- CRUD operations generation
- API documentation with Swagger UI
- Environment configuration
- Modular application structure

## Installation

```bash
pip install nexus-fastapi
```

## Usage

### Create a new project with default settings:

```bash
nexus-fastapi create_project my_api
```

### Create a project with custom configuration:

```bash
nexus-fastapi create_project my_api --config config.json
```

### Sample Configuration File (config.json):

```json
{
  "project_name": "my_fastapi_app",
  "description": "A sample FastAPI application",
  "version": "1.0.0",
  "apps": [
    {
      "name": "users",
      "models": [
        {
          "name": "User",
          "fields": [
            {
              "name": "email",
              "type": "string",
              "nullable": false
            },
            {
              "name": "username",
              "type": "string",
              "nullable": false
            }
          ]
        }
      ]
    }
  ]
}
```

### Running the Generated Project

1. Navigate to your project directory:

   ```bash
   cd my_api
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Project Structure

```
my_api/
├── apps/
│   └── users/
│       ├── __init__.py
│       ├── models.py
│       ├── schemas.py
│       ├── crud.py
│       ├── service.py
│       └── routes.py
├── core/
│   ├── config/
│   │   └── settings.py
│   └── database/
│       └── base.py
├── tests/
├── .env
├── main.py
└── requirements.txt
```

## License

MIT License
