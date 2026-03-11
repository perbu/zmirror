# zmirror

Syncs Zendesk tickets to PostgreSQL using [dlt](https://dlthub.com/). Runs as a Kubernetes CronJob.

## Setup

1. Fill in credentials in `k8s.yaml`
2. Build and push the image:
   ```
   docker build -t your-registry/zmirror:latest .
   docker push your-registry/zmirror:latest
   ```
3. Update the `image` field in `k8s.yaml`
4. `kubectl apply -f k8s.yaml`

## Configuration

All config via environment variables (see `k8s.yaml` Secret):

| Variable | Description |
|---|---|
| `SOURCES__ZENDESK__CREDENTIALS__SUBDOMAIN` | Zendesk subdomain |
| `SOURCES__ZENDESK__CREDENTIALS__EMAIL` | Zendesk agent email |
| `SOURCES__ZENDESK__CREDENTIALS__TOKEN` | Zendesk API token |
| `DESTINATION__POSTGRES__CREDENTIALS` | Postgres connection string |

## License

BSD-2-Clause. See [LICENSE](LICENSE).
