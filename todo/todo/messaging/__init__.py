from todo import settings
from todo.services.todo_service import (
    TodoService,
)

TOPICS = {
    f'{settings.token_validation_response_topic}': TodoService,
}
