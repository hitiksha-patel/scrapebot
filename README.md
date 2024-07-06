# Aptoide App Information Web Scraper - ScrapeBot

## Overview

This project is a web application built with Python and Falcon framework, designed to retrieve and display information about Android applications available on the Aptoide marketplace. The application uses web scraping techniques to fetch details like app name, version, downloads, release date, and description from the Aptoide platform.

### Features

- **Web Scraping**: Retrieves app details from Aptoide by parsing HTML content.
- **API Endpoint**: Accepts a POST request with an Aptoide app URL to fetch and return app information as JSON.
- **Error Handling**: Handles various error scenarios such as missing URL, invalid URL format, and app not found on Aptoide.
- **Logging**: Logs events and errors to `Scrapebot.log` for debugging and monitoring.
- **Unit Testing**: Includes unit tests to verify functionality using the `unittest` framework and mock data.

## Project Structure

The project consists of the following main files and directories:

- **`run.py`**: Initializes a WSGI server to run the Falcon application.
- **`app.py`**: Contains Falcon resources (`AppInfoResource` and `IndexResource`) for handling HTTP requests.
- **`test_app.py`**: Unit tests for `AppInfoResource` using `unittest` and `falcon.testing.TestClient`.
- **`mypy.ini`**: Configuration file for `mypy` type checker.
- **`typings/falcon_stub.pyi`**: Stub file defining types for Falcon framework objects.

## Installation and Usage

### Prerequisites

- Python 3.x
- Dependencies (`falcon`, `requests`, `beautifulsoup4`) installed via pip.

### Installation

1. Unzip the Project:

   - Unzip the downloaded file (`data_theorem_test.zip`) to a directory of your choice on your local machine.

2. Create and activate a virtual environment:

   On macOS and Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   
### Running the Application

To start the Falcon web server locate to ScrapeBot:

```bash
python run.py
```

The application will run locally at `http://localhost:8000`.

### Usage

1. **Home Page**: Access the home page at `http://localhost:8000/`. You can input an Aptoide app URL in a form and submit it.
   
2. **Get App Info**: Post a request to `/get-app-info` endpoint with a URL parameter (`url=https://en.aptoide.com/app`) to retrieve JSON formatted information about the app.


## Testing

1. **Type Checking with MyPy**: Run mypy using `mypy`:

```bash
mypy app.py run.py
```

2. **Unit test**: Run unit tests using `unittest`:

```bash
python test_app.py
```

The tests cover:
- Successful retrieval of app information.
- Handling missing URL parameter.
- Handling invalid and non-existent app URLs.

## Notes

- Ensure Python type annotations are respected throughout the codebase to maintain clarity and support type checking with `mypy`.
- Modify logging configurations (`logging.basicConfig` in `app.py`) as needed for your local environments.
