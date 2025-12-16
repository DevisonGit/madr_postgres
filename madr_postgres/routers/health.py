from fastapi import APIRouter

from madr_postgres.schemas.message import Message

router = APIRouter(prefix='/health', tags=['health'])


@router.get('/', response_model=Message)
async def health_check():
    return {'message': 'ok'}
