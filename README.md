# annotqc

annotqc is a lightweight command-line tool for running quality checks on annotation datasets before they are used for training or delivery.

The goal is to catch common annotation issues early, such as missing fields, empty text, duplicate IDs, or invalid labels.

This project is intentionally minimal and focused on practical data quality checks.

---

## Installation (local development)

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install in editable mode:

```bash
pip install -e .
```

---

## Usage

Run QC checks on an annotation file:

```bash
annotqc check path/to/annotations.json
```

Example annotation format (JSON list):

```json
[
  {
    "id": "a1",
    "text": "The food was amazing",
    "label": "positive"
  },
  {
    "id": "a2",
    "text": "",
    "label": "neutral"
  }
]
```

---

## Checks (current and planned)

- Missing required fields
- Empty text fields
- Duplicate annotation IDs
- Invalid labels outside allowed taxonomy

---

## Development

Run tests:

```bash
pytest
```

Linting and formatting will be added as the project evolves.

---

## Project status

This project is a work in progress and is being developed incrementally with a focus on clarity, testability and real-world usefulness.