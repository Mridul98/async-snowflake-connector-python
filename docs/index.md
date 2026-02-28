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
