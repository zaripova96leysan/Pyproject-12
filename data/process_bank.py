import re
from collections import Counter


def search_transactions(transactions: list[dict], search_string: str) -> list[dict]:
    result = []
    for transaction in transactions:
        description = transaction.get('description', '')
        if re.search(search_string, description, flags=re.IGNORECASE):
            result.append(transaction)
    return result


def count_categories(transactions: list[dict], categories: list[str]) -> dict:
    category_counts = Counter()
    for transaction in transactions:
        description = transaction.get('description', '')
        desc_lower = description.lower()
        for category in categories:
            if category.lower() in desc_lower:
                category_counts[category] += 1
    return category_counts
