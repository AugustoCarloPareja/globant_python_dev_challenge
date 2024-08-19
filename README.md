# PokeAPI Berries Statistics API

This is a FastAPI-based Poke-berries statistics API that fetches berry growth time data from the PokeAPI and calculates various statistics such as mean, median, and variance of growth times.

## Features
- Fetches berry data from PokeAPI.
- Returns statistics like min, max, mean, median, variance, and frequency of growth times.
- Caching for 2 minutes using an in-memory cache.
- Generates a histogram of berry growth times and displays it as an image in plain HTML.
- Deployed using Docker and can be deployed on any cloud service.

## Endpoints
- **`GET /`**: Welcome page with a list of main endpoints.
- **`GET /allBerryStat`**: Fetches berry growth time statistics from PokeAPI and returns them as JSON.
- **`GET /histogram`**: Generates and returns a histogram of berry growth times as an image.
- **`GET /view-histogram`**`: Displays the histogram in plain HTML.
- **`GET /docs`**: Displays the `openapi.json` of FastAPI documentation. You can also try it out the endpoints inside of it.

## Requirements
- Python 3.9+
- FastAPI
- Docker (for containerization)

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/AugustoCarloPareja/globant_python_dev_challenge.git
cd globant_python_dev_challenge
```

### 2. Install Dependencies
First, make sure you have Python 3.9 or later installed. You can install the project dependencies by running:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory of your project to store environment variables. The following variables are required:

```makefile
POKEAPI_BERRY_URL=https://pokeapi.co/api/v2/berry/ # URL for resource of pokeapi
CACHE_TTL=120  # Cache TTL in seconds
APP_PORT=8080 # To open port 8080
REDIS_HOSTNAME=your-redis-hostname # Hostname for connection of redis redis cache service
REDIS_PORT=your-redis-port # Port for connection of redis redis cache service
REDIS_PASSWORD=your-redis-pw # Password for connection of redis cache service
```

### 4. Running the Application Locally
To run the application locally, use uvicorn:

```bash
uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8080.
```

### 5. Accessing the API
Once the app is running, you can access the API endpoints:
- **`GET /`**: `http://127.0.0.1:8080/`
- **`GET /allBerryStats`**: `http://127.0.0.1:8080/allBerryStats`
- **`GET /histogram`**: `http://127.0.0.1:8080/histogram`
- **`GET /view-histogram`**: `http://127.0.0.1:8080/view-histogram`


### 6. Running Tests
Unit tests are provided for the application. To run the tests, use `pytest`:

```bash
pytest
```

## Optional steps:
### 7.  Running with Docker
You can also run the application inside a Docker container.

#### 7.1 Building the Docker Image
```bash
docker build -t pokeapi-fastapi-app .
```

#### 7.2 Running the Docker Container
```bash
docker run -p 8080:8080 pokeapi-fastapi-app
```

### 8. Additional Features
#### Caching
The app caches the fetched berry data for 2 minutes to avoid unnecessary API calls. You can configure cache settings via the `.env` file.

#### Histogram
You can generate a histogram of berry growth times via the `/histogram` endpoint and view it in HTML at `/view-histogram`.

## 9. Project Structure
```plaintext
globant_python_dev_challenge/
│
├── app/
│   ├── main.py                     # Main FastAPI app entry point
│   ├── controllers/                # API controllers
│   ├── services/                   # Business logic and services
│   ├── data_providers/             # Data fetching from PokeAPI
│   ├── cache/                      # Caching implementation
│   ├── models/                     # Pydantic models validation
│   ├── static/                     # Static for .css styles.
│
├── tests/                          # Unit tests
├── Dockerfile                      # Dockerfile for containerization
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .env                            # Environment variables
├── pytest.ini                      # Pytest init path configuration
```

## 10. Testing the Deployed API on Google Cloud Platform (using Google Cloud Run)

This app has been already deployed to `Google Cloud Platform` using `Google Cloud Run` and `Google Cloud Build` using a CI/CD pipeline from this repository. Every direct push into the `master` branch will execute that pipeline.

The code push into `master` will be only available using PRs.

### Base URL
```
https://globant-python-dev-challenge-is6dceck5a-uc.a.run.app
```

### Endpoints
You can test this following endpoints using your browser or tools like curl or Postman.
- `GET /`: Welcome page with main endpoints.
```
https://globant-python-dev-challenge-is6dceck5a-uc.a.run.app/
```
- `GET /allBerryStats`: Fetch the statistics for all berries.
```
https://globant-python-dev-challenge-is6dceck5a-uc.a.run.app/allBerryStats
```

- `GET /histogram`: Generate and view a histogram of berry growth times.
```
https://globant-python-dev-challenge-is6dceck5a-uc.a.run.app/histogram
```
- `GET /view-histogram`: View the histogram in an HTML page.
```
https://globant-python-dev-challenge-is6dceck5a-uc.a.run.app/view-histogram
```
- `GET /docs`: FastAPI interactive documentation.
```
https://globant-python-dev-challenge-is6dceck5a-uc.a.run.app/docs
```
## Thanks for reviewing this project!
 You can now share this URL to let others test the deployed API! :)