# cashier-server-python
Cashier synchronization server, in Python

Ledger-cli REST server for [Cashier](https://github.com/alensiljak/cashier) PWA, implemented in Python with FastAPI.

Cashier Server acts as a mediator between Cashier PWA and Ledger CLI, forwarding queries to Ledger and the results to Cashier. Used for synchronizing the ledger data in Cashier.

This is a Python implementation of the Cashier Server using FastAPI.

## Installation

1. Install `uv`
2. Install `uv tool install cashier-server`

## Configure Backend

To use Beancount as a back-end, set the BEAN_BOOK environment variable.
The easiest way is by creating an `.env` file containing this variable, 
which should point to your Beancount book.
Otherwise, Cashier Server will use Ledger as the backend.

## Run

Execute `cashier-server-py` script provided by the `cashier-server` package.

The server runs on 0.0.0.0:3000, matching the Rust implementation.

## API Endpoints

- `/` - Execute a ledger command
- `/hello` - Return a base64-encoded image
- `/ping` - Simple health check
- `/shutdown` - Request server shutdown

CORS is enabled for all origins, similar to the Rust implementation.

## Development

VSCode recommended.
Run the `run.cmd` script to start the server.
Or run from VSCode to debug.

## Debug

Make sure that Ledger CLI is configured and can be called from the current directory.
Then run:

```sh
run.cmd
# or
uv run python app.py
# Or uvicorn directly:
uvicorn app:app --host 0.0.0.0 --port 3000
```

## Notes on the Implementation

3. Logging is configured to output to the console.

5. For the `/hello` endpoint, you would need to provide an actual image file named "hello.png" in the same directory as the app.py file.
