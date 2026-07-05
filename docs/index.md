# Async Snowflake Connector for Python

An async Python connector for Snowflake using JWT authentication.

## Installation

```bash
pip install async-snowflake
```

## Quick Usage

```python
import asyncio
from async_snowflake import SnowflakeClient, SnowflakeJWTAuthClient

async def main():
    auth = SnowflakeJWTAuthClient(
        account="YOUR_ACCOUNT",
        user="YOUR_USER",
        private_key_path="/path/to/private_key.pem",
    )
    
    async with SnowflakeClient.create(
        base_url="https://your-account.snowflakecomputing.com",
        auth_client=auth,
    ) as client:
        # Execute queries
        result = await client.query.execute("SELECT * FROM users LIMIT 10")
        print(f"Rows: {result.rows}")
        print(f"Columns: {result.columns}")
        
        # List databases
        databases = await client.database.list()
        for db in databases:
            print(db.name)

asyncio.run(main())
```

## Async Queries

For long-running queries, submit the statement asynchronously and poll for
completion instead of blocking on a single request:

```python
import asyncio

# Submit the query; returns a statement handle immediately
handle = await client.query.execute_async("SELECT * FROM big_table")

# Poll until the statement finishes
status = await client.query.get_status(handle)
while status.state == "running":
    await asyncio.sleep(1)
    status = await client.query.get_status(handle)

# Fetch the full result set (all partitions are reassembled for you)
result = await client.query.get_results(handle)
print(f"Rows: {result.row_count}")
print(f"Columns: {result.columns}")
```

### Streaming large result sets

`get_results()` loads every partition into memory. For large results, stream
them one partition (a batch of rows) at a time with `generate_results()`, which
keeps memory bounded:

```python
async for partition in client.query.generate_results(handle):
    for row in partition:
        process(row)
```

Each partition fetch is retried automatically on transient connection drops.

> **Account names with underscores:** if your account name contains
> underscores, the client normalizes the URL host (`_` → `-`) so TLS
> verification against Snowflake's wildcard certificate succeeds. Pass your
> account/base URL as-is — the JWT issuer keeps the real account name intact.

## Fluent Interface

```python
# Account operations
await client.account.get_current_account()
await client.account.list_accounts()

# Database operations
await client.database.list()
await client.database.describe("my_db")

# Schema operations
await client.schema.list(database="my_db")
await client.schema.describe("my_db", "my_schema")

# Table operations
await client.table.list(database="my_db", schema="my_schema")

# Warehouse operations
await client.warehouse.list()
await client.warehouse.resume("warehouse_name")

# Query execution
result = await client.query.execute("SELECT * FROM table")
```

## Using with FastAPI

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from async_snowflake import SnowflakeClient, SnowflakeJWTAuthClient

# Global client instance
snowflake_client: SnowflakeClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global snowflake_client
    
    auth = SnowflakeJWTAuthClient(
        account="YOUR_ACCOUNT",
        user="YOUR_USER",
        private_key_path="/path/to/private_key.pem",
    )
    
    snowflake_client = await SnowflakeClient.create(
        base_url="https://your-account.snowflakecomputing.com",
        auth_client=auth,
    )
    
    yield
    
    await snowflake_client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/users")
async def get_users():
    result = await snowflake_client.query.execute(
        "SELECT * FROM users LIMIT 100"
    )
    return {"columns": result.columns, "rows": result.rows}

@app.get("/databases")
async def get_databases():
    databases = await snowflake_client.database.list()
    return {"databases": [db.model_dump() for db in databases]}
```

## Configuration with Credentials File

Create a `credentials.toml` file:

```toml
[default]
account = "YOUR_ACCOUNT"
user = "YOUR_USER"
private_key_path = "/path/to/private_key.pem"
region = "us-east-1"

[production]
account = "PROD_ACCOUNT"
user = "admin"
private_key_path = "/path/to/prod_key.pem"
```

Then load with `CredentialsManager`:

```python
from async_snowflake import CredentialsManager

creds = CredentialsManager(profile="default").credentials
# Use creds.account, creds.user, etc.
```

Or use environment variables:

```bash
export SNOWFLAKE_ACCOUNT="your_account"
export SNOWFLAKE_USER="your_user"
export SNOWFLAKE_PRIVATE_KEY_PATH="/path/to/key.pem"
```
