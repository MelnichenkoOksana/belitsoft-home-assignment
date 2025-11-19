# API Test Automation Framework

A lightweight and maintainable API test automation framework built with **Python, Pytest, Requests, and Allure**.  
The project uses **https://httpbin.org** as the target service and demonstrates key automation engineering practices.

---

## Key Features

- **Modular Python test framework** following clean architecture principles  
- **Reusable HttpClient** with:
  - centralized configuration  
  - automatic request/response logging  
  - Allure attachments  
- **Custom retry decorator** with:
  - exponential backoff  
  - jitter  
  - retry on specific HTTP statuses and exceptions  
- **Randomized test data** generation using **Faker**  
- **Environment-based configuration** (`config.yaml` + `.env`)  
- **Allure reporting**: requests, responses, metadata  
- Clear and scalable **project structure**

---

## Installation

Clone the repository:

```bash
git clone https://github.com/MelnichenkoOksana/belitsoft-home-assignment.git
cd belitsoft-home-assignment
```

Create and activate a virtual environment:

### Windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### macOS / Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

### Configure environment files

Copy example configuration files and adjust them if needed:

```bash
cp config/config.example.yaml config/config.yaml
cp config/.env.example config/.env
```

`config.yaml` contains framework-level settings (base URL, retry policy, headers).  
`.env` allows overriding YAML values using environment variables.

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Running Tests

Basic test execution:
```bash
pytest -q
```

Run tests with Allure result generation:
```bash
pytest --alluredir=reports/allure-results
```

---

##  Viewing Allure Reports

```bash
allure serve reports/allure-results
```

The command will:
- build an HTML report  
- open it in your browser automatically  

---

## Project Structure

```
project-root/
│
├── src/
│   ├── api/               # HTTP client implementation
│   ├── core/              # logger, retry logic, config loader, helpers
│   └── ...
│
├── tests/
│   ├── api/               # API test suites
│   ├── conftest.py        # fixtures
│   └── ...
│
├── config/
│   ├── config.yaml            # main local config (ignored in git)
│   ├── config.example.yaml    # template config (committed)
│   ├── .env                   # local environment variables (ignored in git)
│   └── .env.example           # example environment file (committed)
│
├── reports/               # Allure output (ignored in git)
│
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.12+
- pip
- Allure CLI (for report generation)

Install Allure CLI (if not installed):

### macOS
```bash
brew install allure
```

### Windows
Download from:  
https://github.com/allure-framework/allure2/releases

---

##  Notes

- `config.yaml` and `.env` are intentionally excluded from the repository  
- Use `config.example.yaml` and `.env.example` to configure your environment  
- Allure report folders are ignored by Git but generated locally  

## About This Project

This framework was developed as part of a technical assignment to demonstrate professional skills in Python-based API test automation, including:

- Pytest test design  
- HTTP client implementation  
- custom retry logic and backoff strategies  
- configuration management (YAML + environment variables)  
- dynamic test data generation  
- Allure reporting integration  
- clean project structure and maintainable architecture  

It is intended to showcase real-world Automation QA engineering practices.