## Installation

- **pip:** (soon will be on pypi)
  ```bash
   pip install git+https://github.com/BobTheBuidler/yearn-treasury`
  ```

- **From Source:**  
  ```bash
  git clone https://github.com/BobTheBuidler/yearn-treasury
  cd yearn-treasury
  poetry install
  ```

## Usage

Run the treasury export tool:

```bash
# For pip installations:
yearn-treasury run --network mainnet --interval 12h
```

For local development (from source installation), use:
```bash
poetry run yearn-treasury run --network mainnet --interval 12h
```

**CLI Options:**
- `--network`: The id of the brownie network the exporter will connect to (default: mainnet)
- `--interval`: The time interval between each data snapshot (default: 12h)
- `--daemon`: Run the export process in the background (default: False) (NOTE: currently unsupported)
- `--grafana-port`: Set the port for the Grafana dashboard where you can view data (default: 3003)
- `--renderer-port`: Set the port for the report rendering service (default: 8080)
- `--victoria-port`: Set the port for the Victoria metrics reporting endpoint (default: 8430)

After running the command, the export script will run continuously until you close your terminal.
To access the dashboard, open your browser and navigate to http://localhost:3003

Enjoy!
