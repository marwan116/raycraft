from fastapi import FastAPI

simple_service = FastAPI()


@simple_service.post("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}
