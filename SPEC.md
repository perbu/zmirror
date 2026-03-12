Gemini said
-----------

Since you're running this in Kubernetes, the ideal architecture is a **Kubernetes CronJob**.

A CronJob is perfect for 10k tickets because it starts, syncs the new data (incremental), and then shuts down, consuming zero resources between runs.

### Technical Spec: Zendesk-to-Postgres Sync (K8s Edition)

#### 1\. Implementation Detail

-   **Logic:** A Python script using the `dlt` library and its verified [Zendesk source](https://dlthub.com/docs/dlt-ecosystem/verified-sources/zendesk).

-   **Sync Mode:** Incremental with `write_disposition="merge"`. This ensures existing tickets in Postgres are updated and new ones are appended.

-   **State Management:** `dlt` stores the "last sync timestamp" in the destination database itself (in a table called `_dlt_pipeline_state`). This means the K8s pod can be ephemeral; it will always know where it left off by querying Postgres.

#### 2\. Environment Variables

The pod requires the following secrets mapped to env vars:

-   `SOURCES__ZENDESK__CREDENTIALS__SUBDOMAIN`

-   `SOURCES__ZENDESK__CREDENTIALS__EMAIL`

-   `SOURCES__ZENDESK__CREDENTIALS__PASSWORD` (or API Token)

-   `DESTINATION__POSTGRES__CREDENTIALS` (Format: `postgresql://user:pass@host:port/db`)

#### 3\. Kubernetes Manifest Specs

-   **Kind:** `CronJob`

-   **Schedule:** `"0 2 * * *"` (Runs daily at 2 AM).

-   **ConcurrencyPolicy:** `Forbid` (Prevents a second job from starting if the first one is still running).

-   **RestartPolicy:** `OnFailure`.

-   **Resources:** 10k tickets are lightweight; 256Mi RAM and 500m CPU is more than enough.

* * * * *

### Copy/Paste this Prompt for Claude Code

> **Prompt for Claude:** "I need a Python script and a Kubernetes manifest to sync Zendesk tickets to a PostgreSQL database using the `dlt` library.
>
> **Requirements:**
>
> 1.  **Script (`sync.py`):** Use `dlt.pipeline` with the `zendesk_support` source. Target only the `tickets` resource. Use `write_disposition='merge'` to ensure incremental updates.
>
>
> 2.  **Config:** Credentials must be pulled from environment variables following `dlt` naming conventions (e.g., `SOURCES__ZENDESK__...`).
>
>
> 3.  **K8s Manifest:** Create a `CronJob` (api version `batch/v1`).
>
>
>     -   Set `concurrencyPolicy: Forbid`.
>
>
>     -   Include a `Secret` template for the Zendesk and Postgres credentials.
>
>
>     -   Ensure the CronJob runs daily.
>
>
> 4.  **Dockerfile:** Provide a simple multi-stage Dockerfile to package the script and `dlt[postgres]` dependency.
>
>
>
> **Note:** Do not use local file storage for state; rely on `dlt`'s built-in Postgres state backend."

* * * * *

### One important tip for 2026:

When Claude generates the Zendesk source, ensure it uses the **Zendesk Incremental Export API** rather than the standard `/tickets` endpoint. `dlt` usually handles this automatically if `load_all=False` is passed to the source, but it's worth double-checking the logs on the first run to ensure you aren't hitting the 100-per-page limit unnecessarily.

