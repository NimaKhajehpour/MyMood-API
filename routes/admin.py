from fastapi import APIRouter, HTTPException, Body, Path
from starlette import status

from di.injection import db_dependency
from di.user_dependency import user_dependency
from models.bugs import Bug
from models.news import NewsRequest, News

admin_news_router = APIRouter(
    prefix="/admin/news",
    tags=["Admin"]
)


@admin_news_router.post("", status_code=status.HTTP_201_CREATED)
async def add_news(db: db_dependency, user: user_dependency, created_news: NewsRequest = Body()):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    news = News(**created_news.model_dump())
    db.add(news)
    db.commit()


@admin_news_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_news(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    db.query(News).delete(synchronize_session=False)
    db.commit()


@admin_news_router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT)
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


admin_bugs_router = APIRouter(
    prefix='/admin/bugs',
    tags=['Admin']
)


@admin_bugs_router.get("", status_code=status.HTTP_200_OK)
async def get_all_bugs(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    bugs = db.query(Bug).all()
    return bugs


@admin_bugs_router.get("/{bug_id}", status_code=status.HTTP_200_OK)
async def get_bug_by_id(db: db_dependency, user: user_dependency, bug_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug report not found")
    return bug


@admin_bugs_router.put("/approve/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
async def approve_bug(db: db_dependency, user: user_dependency, bug_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug report not found")
    bug.approved = True
    db.add(bug)
    db.commit()


@admin_bugs_router.put("/done/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
async def set_bug_done(db: db_dependency, user: user_dependency, bug_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug report not found")
    bug.done = True
    db.add(bug)
    db.commit()


@admin_bugs_router.put("/link/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
async def set_bug_issue_link(db: db_dependency, user: user_dependency, bug_id: int = Path(gt=0), link: str = Body()):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug report not found")
    bug.issue_link = link
    db.add(bug)
    db.commit()


@admin_bugs_router.delete("/{bug_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bug_by_id(db: db_dependency, user: user_dependency, bug_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug report not found")
    db.query(Bug).filter(Bug.id == bug_id).delete()
    db.commit()