import csv
from importlib import resources
from typing import List

def load_quotes() -> List[str]:
    """Return a list of quotes shipped with the package."""
    with resources.files(__package__).joinpath("quotes.csv").open(
        "r", newline="", encoding="utf-8"
    ) as f:
        reader = csv.DictReader(f)
        return [row["quote"].strip() for row in reader if row.get("quote")]
