from raycraft import RayCraftAPI

simple_service = RayCraftAPI()


@simple_service.post("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}
