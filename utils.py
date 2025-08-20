# ✅ utils.py
from datetime import datetime, timedelta
from tabulate import tabulate

def get_date_ranges():
    end = datetime.today()
    start = end - timedelta(days=13)
    end_prev = start
    start_prev = end_prev - timedelta(days=13)
    return (
        start.strftime('%Y-%m-%d 00:00:00'),
        end.strftime('%Y-%m-%d 23:59:59'),
        start_prev.strftime('%Y-%m-%d 00:00:00'),
        end_prev.strftime('%Y-%m-%d 23:59:59')
    )

def format_comparative_table(rows):
    if not rows or len(rows) < 2:
        return "⚠️ Not enough data for comparison"
    current = rows[0]
    previous = rows[1]
    headers = ["Metric", "Current", "Previous"]
    table = []
    for key in current:
        if key == "period":
            continue
        label = key.replace("_", " ").capitalize()
        table.append([label, current[key], previous[key]])
    return tabulate(table, headers=headers, tablefmt="github")

def create_notion_blocks(title: str, rows: list[dict]) -> list:
    if not rows or len(rows) < 2:
        return []

    current = rows[0]
    previous = rows[1]

    header_row = ["Metric", "Current", "Previous"]
    data_rows = []

    for key in current:
        if key == "period":
            continue
        label = key.replace("_", " ").capitalize()
        data_rows.append([label, str(current[key]), str(previous[key])])

    return [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": title}}]
            }
        },
        {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 3,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    _build_table_row(header_row)
                ] + [_build_table_row(row) for row in data_rows]
            }
        }
    ]

def _build_table_row(cells: list[str]) -> dict:
    return {
        "object": "block",
        "type": "table_row",
        "table_row": {
            "cells": [[{"type": "text", "text": {"content": cell}}] for cell in cells]
        }
    }
