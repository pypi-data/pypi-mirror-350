# Business logic core for python (bisslog-core-py)

[![PyPI](https://img.shields.io/pypi/v/bisslog)](https://pypi.org/project/bisslog/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**bisslog-core** is a lightweight and dependency-free Python library that implements the **Hexagonal Architecture (Ports and Adapters)**.  
It enforces a strict separation between **domain logic, application, and infrastructure**, allowing easy integration with different frameworks and external services without modifying core business logic.

This library serves as an **auxiliary layer for business logic or service domain**, providing a **common language** for operations when interacting with external components.  
In other words, the **business rules remain unchanged** even if the infrastructure changes (e.g., switching the messaging system).  
The key principle is:  
> **"The domain should not change because some adapter changed."**

It is designed for **backend functionality**, **framework-agnostic development**, and to **minimize migration costs**.


![Explanation Diagram](https://raw.githubusercontent.com/darwinhc/bisslog-core-py/master/docs/explanation.jpg)


---

## 🚀 Installation
You can install `bisslog-core` using **pip**:

```bash
pip install bisslog
```

## Usage Example


Here is an example of what the implementation of a use case looks like without importing any additional dependencies.


Note: if the adapter is not implemented it will give execution attempt messages.

~~~python
from random import random

from bisslog.database.bisslog_db import bisslog_db as db
from bisslog.use_cases.use_case_full import FullUseCase
from bisslog import use_case
from scripts.project_example_1.usecases.my_second_use_case import my_second_use_case


class SumarUseCase(FullUseCase):

    @use_case  # or simply def use()
    def something(self, a: int, b: int, user_id: int, transaction_id: str, *args, **kwargs) -> dict:
        component = self._transaction_manager.get_component()
        self.log.info("Receive a:%d b:%d %s", a, b, component, checkpoint_id="reception",
                      transaction_id=transaction_id)

        # Retrieve last session
        last_session = db.session.get_last_session_user(user_id)
        if last_session is not None:
            self.log.info(f"Last session of user {user_id} fue {last_session}", 
                          checkpoint_id="last_session")

        db.session.save_new_session_user(user_id)

        db.event_type.loadWebhookEventType(5)
        rand = random()
        new_value = my_second_use_case(value=rand*10, product_type="string2", transaction_id=transaction_id)

        # Calculate result
        res = a + b
        if res > 10:
            self.log.warning("Es mayor que 10", checkpoint_id="check-response")

        # Publish event
        self.publish("queue_suma", {"suma": res + new_value, "operation": "a + b"})
        return {"suma": res}


sumar_use_case = SumarUseCase("sumar")
~~~

~~~python
from bisslog import use_case, domain_context, transaction_manager, bisslog_upload_file


log = domain_context.tracer

@use_case
def my_second_use_case(value: float, product_type: str, *args, **kwargs) -> float:

        log.info(
            "Received %d %s", value, transaction_manager.get_component(),
            checkpoint_id="second-reception")

        if product_type == "string1":
            new_value = value * .2
        elif product_type == "string2":
            new_value = value * .3
        elif product_type == "string3":
            new_value = value * .5
        else:
            new_value = value * .05

        uploaded = bisslog_upload_file.main.upload_file_from_local("./test.txt", "/app/casa/20")

        if uploaded:

            log.info("Uploaded file component: %s", transaction_manager.get_component(),
                     checkpoint_id="uploaded-file")

        return new_value
~~~



For the configuration of the entry-points or primary libraries, they will only have to call the corresponding use case and map the fields. Here is an example with FastAPI. [More examples](scripts/project_example_1/)


~~~python
from typing import Annotated

from fastapi import FastAPI, Header, HTTPException

from scripts.project_example_1.usecases.my_first_use_case import sumar_use_case

app = FastAPI()

@app.get("/fast-api-example/first-use-case/{a}/{b}")
async def get_user(a: str, b: str,
                   user_id: Annotated[str | None, Header()]):
    print(a, b, user_id)
    if user_id is None:
        raise HTTPException(status_code=400, detail="user_id is required")
    res = sumar_use_case(int(a), int(b), int(user_id))
    res["identifier"] = "fast-api"
    return res

~~~


Definition of possible interfaces of divisions needed by the database, if not, it does not matter.

~~~python
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

~~~

The following is a dummie implementation of the above division to give an example

~~~python
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

~~~


## 🧪 Running library tests

To Run test with coverage
~~~cmd
coverage run --source=bisslog -m pytest tests/
~~~


To generate report
~~~cmd
coverage html && open htmlcov/index.html
~~~


## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

