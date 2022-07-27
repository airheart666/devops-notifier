import uvicorn  # type: ignore
"""
Este arquivo serve para simplificar a incialização do utilitário, necessitando apenas que execute o arquivo main, ao invés de executar o comando uvicorn
"""


async def app(scope, receive, send):
    ...

if __name__ == "__main__":
    uvicorn.run("listener:listener", port=8000,
                log_level="info", host="*")
