from fastapi import APIRouter, HTTPException, Path
from starlette import status

from di.injection import db_dependency
from di.user_dependency import user_dependency
from models.news import News

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_news(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    news = db.query(News).all()
    return news


@router.get("/{news_id}", status_code=status.HTTP_200_OK, response_model=News)
async def get_news_by_id(db: db_dependency, user: user_dependency, news_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News Not Found")
    return news
