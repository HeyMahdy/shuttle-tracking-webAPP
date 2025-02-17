import typing
import strawberry
from fastapi import FastAPI, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from Dbs.DataBaseSetting.DatabaseConfig import get_async_db
from Dbs.Models.models import practiceDB
from auth.auth_endpoints import router as auth_router

app = FastAPI()

app.include_router(auth_router)

import strawberry

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

async def get_context(
    db: AsyncSession = Depends(get_async_db),
):
    return {
        "custom_value": db,
    }


@strawberry.type
class USU:
    name: str
    work:str

@strawberry.input
class UpdateFruitWeightInput:
    name: str
    work: str


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_fruit_weight(self, input: UpdateFruitWeightInput,info: strawberry.Info) -> USU:
        # Access the fields from the input
        name = input.name
        work = input.work

        session: AsyncSession = info.context['custom_value']
        p1 = practiceDB(name=name, work=work)
        session.add(p1)
        await session.commit()
        await session.refresh(p1)

        return USU(name=p1.name, work=p1.work)


@strawberry.type
class Query:
    @strawberry.field
    async def hello(self)->str:
        return "Hello World!"



schema = strawberry.Schema(query=Query,mutation=Mutation)

graphql_app = GraphQLRouter(
    schema,
    path="/graphql",
    context_getter=get_context,
)

app.include_router(graphql_app)










































































