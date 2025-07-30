# generatecv

[![CI](https://github.com/yantology/generatecv/workflows/Python%20CI/badge.svg)](https://github.com/yantology/generatecv/actions/workflows/python-ci.yml)
[![Security](https://github.com/yantology/generatecv/workflows/Security%20Scan/badge.svg)](https://github.com/yantology/generatecv/actions/workflows/security.yml)
[![Documentation](https://github.com/yantology/generatecv/workflows/Documentation/badge.svg)](https://github.com/yantology/generatecv/actions/workflows/docs.yml)
[![codecov](https://codecov.io/gh/yantology/generatecv/branch/main/graph/badge.svg)](https://codecov.io/gh/yantology/generatecv)
[![PyPI version](https://badge.fury.io/py/generatecv.svg)](https://badge.fury.io/py/generatecv)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for generating professional CVs from structured data.

## Installation

```bash
pip install generatecv
```

Or using `uv`:

```bash
uv add generatecv
```

For development:

```bash
# Clone the repository
git clone https://github.com/yantology/generatecv.git
cd generatecv

# Create and activate a virtual environment
uv venv

# Install the package and development dependencies
uv pip install -e ".[dev]"
```

## Quick Start

### 1. Get the Example Template

After installation, use the built-in command to get a starter template:

```bash
# Download example YAML to current directory
generatecv-example

# Or specify a custom output path
generatecv-example --output my_cv_data.yaml
```

This creates an `example.yaml` file with sample CV data that you can customize.

### 2. Customize Your Data

Edit the generated YAML file with your information:

```yaml
personal_info:
  name: "Your Name"
  email: "your.email@example.com"
  phone: "+1234567890"
  location: "Your City, Country"
  # ... customize other fields
```

### 3. Generate Your CV

```python
from generatecv.pdf_generator import yamltocv, generatepdf

# Load your CV data from YAML
cv_data = yamltocv("example.yaml")  # or your custom filename

# Generate PDF
output_path = generatepdf(
    cv_data=cv_data,
    output_path="my_cv.pdf",
    style="classic",
    page_size="A4"
)

print(f"CV generated: {output_path}")
```

### Alternative: Pure Python Usage

You can also define your CV data directly in Python:

```python
from generatecv.pdf_generator import generatepdf
from generatecv.models import CV, PersonalInfo, Education, CompanyExperience, Role

cv_data = CV(
    personal_info=PersonalInfo(
        name="Your Name",
        email="your.email@example.com",
        phone="+1234567890",
        location="Your City, Country",
        summary="Your professional summary",
        title="Your Job Title"
    ),
    education=[
        Education(
            institution="University Name",
            degree="Your Degree",
            start_date="2019",
            end_date="2023"
        )
    ],
    experience=[
        CompanyExperience(
            company="Company Name",
            location="Company Location",
            roles=[
                Role(
                    title="Your Role",
                    start_date="2023-01",
                    end_date="Present",
                    description="Your role description"
                )
            ]
        )
    ]
)

# Generate PDF
generatepdf(cv_data, "my_cv.pdf")
```

## Development

### Type Checking

This project uses `pyrefly` for static type checking:

```bash
# Run type checking
pyrefly check

# Suppress errors temporarily during migration
pyrefly check --suppress-errors
```

### Testing

Tests are written using `pytest`:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=generatecv

# Generate coverage report
pytest --cov=generatecv --cov-report=html
```

### Linting

This project uses `ruff` for linting:

```bash
# Run linter
ruff check .

# Automatically fix issues
ruff check --fix .
```

### Code Formatting

Code formatting is done with `black`:

```bash
# Format code
black .

# Format code with line length of 80 characters
black --line-length 80 .
```

## Project Structure

```
generatecv/
├── src/
│   ├── generatecv/        # Main package
│   │   ├── __init__.py
│   │   └── cv_generator.py
│   ├── tool/              # CLI tools
│   │   ├── __init__.py
│   │   └── main.py
│   └── py.typed           # PEP 561 marker
├── tests/                 # Test directory
│   ├── test_cv_generator.py
│   └── test_example.py
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
