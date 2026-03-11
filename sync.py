"""Zendesk tickets to PostgreSQL sync using dlt."""

import dlt
from dlt.sources.zendesk import zendesk_support


def main():
    pipeline = dlt.pipeline(
        pipeline_name="zendesk_to_postgres",
        destination="postgres",
        dataset_name="zendesk",
    )

    source = zendesk_support(load_all=False)
    tickets = source.with_resources("tickets")

    info = pipeline.run(tickets, write_disposition="merge")
    print(info)


if __name__ == "__main__":
    main()
