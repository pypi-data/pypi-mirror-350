from fastapi import APIRouter

router = APIRouter()


@router.get("/books")
async def get_books():
    return {"books": ["foo", "bar"]}
