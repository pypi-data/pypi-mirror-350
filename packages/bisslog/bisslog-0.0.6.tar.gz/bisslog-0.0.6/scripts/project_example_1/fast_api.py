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
