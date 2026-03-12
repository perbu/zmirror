"""Zendesk tickets to PostgreSQL sync using dlt."""

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

import logging

import dlt
from zendesk import zendesk_support

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def strip_null_bytes(record):
    """Strip null bytes from string fields — PostgreSQL can't store them."""
    for key, value in record.items():
        if isinstance(value, str):
            record[key] = value.replace("\x00", "")
    return record


def main():
    pipeline = dlt.pipeline(
        pipeline_name="zendesk_to_postgres",
        destination="postgres",
        dataset_name="zendesk",
    )

    source = zendesk_support(load_all=False)
    data = source.with_resources("tickets", "ticket_comments")
    data.resources["tickets"].add_map(strip_null_bytes)
    data.resources["ticket_comments"].add_map(strip_null_bytes)
    # Force complex columns to text to avoid ADBC jsonb binary format issues
    data.resources["tickets"].apply_hints(
        columns={"tags": {"data_type": "text"}}
    )

    info = pipeline.run(data, write_disposition="merge", loader_file_format="parquet")
    print(info)


if __name__ == "__main__":
    main()
