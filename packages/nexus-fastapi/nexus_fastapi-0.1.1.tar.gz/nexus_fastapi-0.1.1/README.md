# Nexus-FastAPI

A powerful FastAPI project generator and framework that helps you create production-ready FastAPI applications with best practices and modern architecture.

## Features

- 🚀 **Quick Start**: Generate a complete FastAPI project structure in seconds
- 📦 **Modular Design**: Built-in support for modular applications with separate apps
- 🔐 **Security**: Built-in security features with JWT authentication
- 🗄️ **Database**: SQLAlchemy integration with automatic model generation
- 📝 **Documentation**: Automatic API documentation with Swagger UI
- 🧪 **Testing**: Built-in testing setup with pytest
- 🎨 **Code Style**: Consistent code formatting with black and isort

## Installation

```bash
pip install nexus-fastapi
```

## Quick Start

Create a new FastAPI project:

```bash
# Create a project with default settings
nexus-fastapi create_project my_app

# Create a project with custom configuration
nexus-fastapi create_project my_app --config config.json
```

### Sample Configuration File (config.json)

```json
{
  "project_name": "my_app",
  "description": "My FastAPI Application",
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

## Project Structure

```
my_app/
├── apps/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── crud.py
│   │   ├── service.py
│   │   └── routes.py
│   └── __init__.py
├── core/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── base.py
│   └── security/
│       ├── __init__.py
│       └── auth.py
├── tests/
│   └── __init__.py
├── .env
├── main.py
├── requirements.txt
└── run.py
```

## Running the Project

1. Navigate to your project directory:

   ```bash
   cd my_app
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python run.py
   ```

4. Access the API documentation at: http://localhost:8000/docs

## Development

### Setting up the development environment

1. Clone the repository:

   ```bash
   git clone https://github.com/meetvelani/nexus-fastapi.git
   cd nexus-fastapi
   ```

2. Install development dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Running tests

```bash
pytest
```

### Code formatting

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Meetkumar Velani - [meetvelani2728@gmail.com](mailto:meetvelani2728@gmail.com)
- Axay Patoliya - [axaypatoliya2222@gmail.com](mailto:axaypatoliya2222@gmail.com)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
