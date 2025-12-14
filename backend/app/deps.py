from typing import Annotated, AsyncGenerator, TypeAlias
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from app.model_db import QuestionDB, AnswerDB
from app.db import async_engine


async def create_session() -> AsyncGenerator[AsyncSession]:
    # WARN: async expects no expiration
    # Ref: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session


SessionDep: TypeAlias = Annotated[AsyncSession, Depends(create_session)]


# NOTE: crud operation
async def get_user_db(session: SessionDep, answer_id: int) -> UserDB:
    statement = select().where(UserDB.id == answer_id)
    session_user = await session.scalar(statement)
    if session_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User wasn't found"
        )
    return session_user


CurrentAnswerDep: TypeAlias = Annotated[AnswerDB, Depends(get_answer_db)]


# NOTE: crud operation
async def get_question_db(session: SessionDep, question_id: int) -> QuestionDB:
    statement = select(QuestionDB).where(QuestionDB.id == question_id)
    session_question = await session.scalar(statement)
    if session_question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question wasn't found"
        )
    return session_question


CurrentQuestionDep: TypeAlias = Annotated[QuestionDB, Depends(get_question_db)]
