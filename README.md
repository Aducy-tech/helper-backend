# AI Assistant API

## Quick Start

### Environment Setup
1. Fill `.env.example` file and rename it to `.env`
2. Fill `pytest.ini.example` file and rename it to `pytest.ini`

### SSL Certificate Generation
1. Create a `certs` directory in the project root
2. Generate SSL certificates using OpenSSL:
```shell
# Generate private key
openssl genrsa -out certs/private.pem 2048

# Generate public key
openssl rsa -in certs/private.pem -outform PEM -pubout -out certs/public.pem
```

### Installation
1. Create and activate virtual environment:
```shell
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```shell
pip install -r requirements.txt
```

### Running the Application
Start the development server:
```shell
uvicorn src.main:app
# or (for reloading on file changes)
uvicorn src.main:app --reload
# or
python src/main.py
```

The API will be available at `http://localhost:8000` (port by default)

### API Documentation
After starting the server, visit:
- Swagger UI: `http://localhost:8000/docs` (port by default)
