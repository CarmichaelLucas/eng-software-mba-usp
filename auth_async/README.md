### .env Example

```
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

DATABASE_URL= "postgresql+asyncpg://docker:password@postgres:5432/auth_async_api"

KAFKA_BOOTSTRAP_SERVERS="kafka:29092"
TOKEN_VALIDATION_REQUEST_TOPIC="token_validation_request"
TOKEN_VALIDATION_RESPONSE_TOPIC="token_validation_response"
```
