import uuid
from datetime import datetime, timezone
from typing import Optional

from scripts.project_example_1.database.session_division import SessionDivision


cache_db = {"session": []}

class SessionDivisionCache(SessionDivision):

    def get_last_session_user(self, user_identifier: int) -> Optional[dict]:

        user_sessions = [session for session in cache_db["session"]
                         if session["user"] == user_identifier]
        if not user_sessions:
            return None
        return user_sessions[-1]


    def save_new_session_user(self, user_identifier: int) -> None:
        cache_db["session"].append({"user": user_identifier, "id": uuid.uuid4().hex,
                                    "created_at": datetime.now(timezone.utc)})

session_division_cache = SessionDivisionCache()
