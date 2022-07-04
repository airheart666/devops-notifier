import uvicorn  # type: ignore


async def app(scope, receive, send):
    ...

if __name__ == "__main__":
    uvicorn.run("listener:listener", port=8000, log_level="info")
