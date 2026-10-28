# Expense Tracker CLI

A simple command-line tool to track your daily expenses. Data is stored locally in a JSON file.

## Features

- Add expenses with a category and optional note
- List all expenses or filter by category
- See total spending per category
- Delete expenses by ID

## Installation

```bash
git clone https://github.com/<your-username>/expense-tracker.git
cd expense-tracker
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python expense_tracker.py add 12.50 food --note "lunch"
python expense_tracker.py add 40 transport
python expense_tracker.py list
python expense_tracker.py list --category food
python expense_tracker.py summary
python expense_tracker.py delete 1
```

## Requirements

- Python 3.8+
- click
- tabulate

## License

MIT
