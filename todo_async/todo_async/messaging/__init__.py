from todo_async import settings
from todo_async.services.todo_service import (
    TodoService,
)

TOPICS = {
    f'{settings.token_validation_response_topic}': TodoService,
}
