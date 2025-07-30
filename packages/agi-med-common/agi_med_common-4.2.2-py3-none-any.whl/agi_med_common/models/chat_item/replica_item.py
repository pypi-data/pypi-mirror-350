from datetime import datetime
from typing import Any, Optional

from pydantic import Field, ConfigDict

from .. import _Base
from ..enums import StateEnum, ActionEnum, ModerationLabelEnum


_DATETIME_FORMAT: str = "%Y-%m-%d-%H-%M-%S"
_EXAMPLE_DATETIME: str = datetime(1970, 1, 1, 0, 0, 0).strftime(_DATETIME_FORMAT)


class ReplicaItem(_Base):
    body: str = Field("", alias="Body", examples=["Привет"])
    resource_id: Optional[str] = Field(None, alias="ResourceId", examples=["<link-id>"])
    role: bool = Field(False, alias="Role", description="True = ai, False = client", examples=[False])
    date_time: str = Field(
        _EXAMPLE_DATETIME,
        alias="DateTime",
        examples=[_EXAMPLE_DATETIME],
        description=f"Format: {_DATETIME_FORMAT}",
    )
    state: StateEnum = Field("EMPTY", alias="State", description="chat manager fsm state", examples=["COLLECTION"])
    action: ActionEnum = Field("START", alias="Action", description="chat manager fsm action", examples=["DIAGNOSIS"])
    moderation: ModerationLabelEnum = Field(
        ModerationLabelEnum.OK,
        alias="Moderation",
        description="chat manager moderated outcome type",
        examples=[ModerationLabelEnum.NON_MED],
    )

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    @staticmethod
    def DATETIME_FORMAT() -> str:
        return _DATETIME_FORMAT


class ReplicaItemPair(_Base):
    # remove annoying warning for protected `model_` namespace
    model_config = ConfigDict(protected_namespaces=())

    user_replica: ReplicaItem = Field(alias="UserReplica")
    bot_replica: ReplicaItem = Field(alias="BotReplica")
