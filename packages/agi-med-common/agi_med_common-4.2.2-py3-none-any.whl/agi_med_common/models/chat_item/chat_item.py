from pydantic import Field
from typing import Any

from . import OuterContextItem, InnerContextItem, ReplicaItemPair
from ..enums import ActionEnum
from .. import _Base


class ChatItem(_Base):
    outer_context: OuterContextItem = Field(alias="OuterContext")
    inner_context: InnerContextItem = Field(alias="InnerContext")

    def create_id(self, short: bool = False, clean: bool = False) -> str:
        return self.outer_context.create_id(short, clean)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    def update(self, replica_pair: ReplicaItemPair) -> None:
        self.inner_context.replicas.append(replica_pair.user_replica)
        self.inner_context.replicas.append(replica_pair.bot_replica)

    def count_questions(self) -> int:
        return len(
            list(
                filter(
                    lambda replica: replica.role and replica.action == ActionEnum.QUESTION,
                    self.inner_context.replicas,
                )
            )
        )

    def zip_history(self, field: str) -> list[Any]:
        return [replica.to_dict().get(field, None) for replica in self.inner_context.replicas]
