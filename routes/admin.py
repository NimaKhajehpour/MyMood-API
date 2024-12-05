from fastapi import APIRouter, HTTPException, Body, Path
from starlette import status

from di.injection import db_dependency
from di.user_dependency import user_dependency
from models.news import NewsRequest, News

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/news", status_code=status.HTTP_201_CREATED)
async def add_news(db: db_dependency, user: user_dependency, created_news: NewsRequest = Body()):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    news = News(**created_news.model_dump())
    db.add(news)
    db.commit()


@router.delete("/news", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_news(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    db.query(News).delete(synchronize_session=False)
    db.commit()


@router.delete("/news/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_news_by_id(db: db_dependency, user: user_dependency, news_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News Not Found")
    db.query(News).filter(News.id == news_id).delete()
    db.commit()
