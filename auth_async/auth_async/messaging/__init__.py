from auth_async import settings
from auth_async.services.auth_service import (
    AuthService,
)

TOPICS = {
    f'{settings.token_validation_request_topic}': AuthService,
}
