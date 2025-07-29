from abc import ABC, abstractmethod
from typing import Optional

from bisslog.adapters.division import Division


class SessionDivision(Division, ABC):

    @abstractmethod
    def save_new_session_user(self, user_identifier: int) -> None:
        raise NotImplementedError("save_new_session_user not implemented")

    @abstractmethod
    def get_last_session_user(self, user_identifier: int) -> Optional[dict]:
        raise NotImplementedError("get_last_session_user not implemented")
