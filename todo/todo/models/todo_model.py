from datetime import datetime
from enum import Enum

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class Todo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_uuid: Mapped[str]
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TodoState]
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
