# `hexfrost-toolbox` - batteries for FastAPI projects

Open source library with useful utils for fast development


## Installation

```bash
pip install hexfrost-toolbox
```

## Usage

### Test Client

```python
from toolbox.testing import debug_client

app = FastAPI()

async with debug_client(app) as client:
    response = await client.get('/')
    assert response.status_code == 200
```
You can use app with this client for debug code like as `django.testclient`


### Test Database

The function will create a new database with a prefix next to the one specified in the settings.


* The original settings file will be overwritten so that in all tests queries will go to the new database.

```python
POSTGRES_DB = "postgres" # will overwrite -> "test_postgres"
```

You can use one database settings file for all tests, without worrying that the original database will be overwritten

```python
from toolbox.testing import temporary_database
from toolbox.sqlalchemy.connection import DatabaseConnectionSettings

from your_project.alchemy_models import BaseModel


@pytest.fixture(autouse=True)
def db_settings():
    data = DatabaseConnectionSettings(
        POSTGRES_USER="postgres", # Required
        POSTGRES_PASSWORD = "postgres", # Required
        POSTGRES_HOST = "0.0.0.0", # Required
        POSTGRES_PORT = "5432", # Required
        POSTGRES_DB = "postgres" # Required
    )

    return data

@pytest.fixture(autouse=True)
async def temp_db(db_settings):
    async with temporary_database(
            settings=db_settings,
            base_model=BaseModel,
            # db_prefix = "test" # optional
    ):
        yield
        pass
```

### Database Connect

```python
from fastapi import Depends, FastAPI
from toolbox.sqlalchemy.connection import DatabaseConnectionManager, DatabaseConnectionSettings


settings = DatabaseConnectionSettings(
        POSTGRES_USER="postgres", # Required
        POSTGRES_PASSWORD = "postgres", # Required
        POSTGRES_HOST = "0.0.0.0", # Required
        POSTGRES_PORT = "5432", # Required
        POSTGRES_DB = "postgres" # Required
    )

get_db_conn = DatabaseConnectionManager(settings=settings)

app = FastAPI()

@app.get("/")
async def index(database_conn = Depends(get_db_conn)):
    ...
```

### Auth Middleware
#### FastAPI

```python

from toolbox.auth.middlewares.fastapi_ import BearerTokenMiddleware, BearerTokenMiddlewareSettings

class TokenStorage:

    async def __call__(self, token: str) -> bool:
        ...

token_validator = TokenStorage()
settings = BearerTokenMiddlewareSettings(
    token_validator=token_validator, # Required
    exclude_paths=["/docs"] # Required
)

BearerTokenMiddleware.set_settings(settings)

app = FastAPI()
app.add_middleware(BearerTokenMiddleware)

```
### Sensetive Fields in Pydantic Models

```python
import os
from toolbox.schemes import SensitiveDataScheme
from toolbox.cipher import CipherSuiteManager, CipherSuiteSettings


settings = CipherSuiteSettings(
    MASTER_KEY=os.getenv("MASTER_KEY") # Required
)


cipher_suite = CipherSuiteManager.set_settings(settings)


SensitiveDataScheme.set_cipher_suite_manager(cipher_suite)


class OpenAPIToken(SensitiveDataScheme):
    _sensitive_attributes = ["token"]

    default_model: str
    token: str | bytes


new_token = OpenAPIToken(
        default_model = "o3-mini",
        token = "sk-12fefx33k34h1v4h1cl14c"
    ).encrypt_fields()

unsafe_data = new_token.decrypt_fields()
```

### Tools



That's it! Enjoy! 🚀
