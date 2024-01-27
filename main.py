from contextlib import asynccontextmanager
from typing import AsyncIterator
from graphene import Schema
from app.db.database import prepare_db
from app.gql.queries import Query
from fastapi import FastAPI
from starlette_graphene import GraphQLApp
import uvicorn

schema = Schema(query=Query)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    prepare_db()
    try:
        yield
    finally:
        pass


app = FastAPI(lifespan=lifespan)
app.mount("/graphql", GraphQLApp(schema=schema))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
