"""Simple command-line expense tracker."""
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

import click
from tabulate import tabulate

DATA_FILE = Path("expenses.json")


def load_expenses():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save_expenses(expenses):
    DATA_FILE.write_text(json.dumps(expenses, indent=2))


@click.group()
def cli():
    """Track your expenses from the command line."""


@cli.command()
@click.argument("amount", type=float)
@click.argument("category")
@click.option("--note", default="", help="Optional note about the expense.")
def add(amount, category, note):
    """Add an expense: add 12.50 food --note "lunch" """
    expenses = load_expenses()
    new_id = max((e["id"] for e in expenses), default=0) + 1
    expenses.append(
        {
            "id": new_id,
            "date": date.today().isoformat(),
            "amount": amount,
            "category": category.lower(),
            "note": note,
        }
    )
    save_expenses(expenses)
    click.echo(f"Added expense #{new_id}: {amount:.2f} ({category})")


@cli.command("list")
@click.option("--category", default=None, help="Filter by category.")
def list_expenses(category):
    """List all expenses."""
    expenses = load_expenses()
    if category:
        expenses = [e for e in expenses if e["category"] == category.lower()]
    if not expenses:
        click.echo("No expenses found.")
        return
    rows = [[e["id"], e["date"], e["category"], f'{e["amount"]:.2f}', e["note"]] for e in expenses]
    click.echo(tabulate(rows, headers=["ID", "Date", "Category", "Amount", "Note"]))


@cli.command()
def summary():
    """Show total spending per category."""
    expenses = load_expenses()
    if not expenses:
        click.echo("No expenses found.")
        return
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    rows = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    rows = [[cat, f"{amt:.2f}"] for cat, amt in rows]
    click.echo(tabulate(rows, headers=["Category", "Total"]))
    click.echo(f"\nGrand total: {sum(totals.values()):.2f}")


@cli.command()
@click.argument("expense_id", type=int)
def delete(expense_id):
    """Delete an expense by its ID."""
    expenses = load_expenses()
    remaining = [e for e in expenses if e["id"] != expense_id]
    if len(remaining) == len(expenses):
        click.echo(f"No expense with ID {expense_id}.")
        return
    save_expenses(remaining)
    click.echo(f"Deleted expense #{expense_id}.")


if __name__ == "__main__":
    cli()
