from fastapi import APIRouter, HTTPException, Body, Path
from starlette import status
from sqlmodel import func
from di.injection import db_dependency
from di.user_dependency import user_dependency
from models.User import User
from models.bugs import Bug
from models.news import NewsRequest, News
from models.suggestions import Suggestion

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


admin_suggestions_router = APIRouter(
    prefix='/admin/suggestions',
    tags=['Admin']
)


@admin_suggestions_router.get("", status_code=status.HTTP_200_OK)
async def get_all_suggestions(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    suggestion = db.query(Suggestion).all()
    return suggestion


@admin_suggestions_router.get("/{suggestion_id}", status_code=status.HTTP_200_OK)
async def get_suggestion_by_id(db: db_dependency, user: user_dependency, suggestion_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion not found")
    return suggestion


@admin_suggestions_router.put("/approve/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def approve_suggestion(db: db_dependency, user: user_dependency, suggestion_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion not found")
    suggestion.approved = True
    db.add(suggestion)
    db.commit()


@admin_suggestions_router.put("/done/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def set_suggestion_done(db: db_dependency, user: user_dependency, suggestion_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion found")
    suggestion.done = True
    db.add(suggestion)
    db.commit()


@admin_suggestions_router.put("/link/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def set_suggestion_issue_link(db: db_dependency, user: user_dependency, suggestion_id: int = Path(gt=0), link: str = Body()):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion not found")
    suggestion.issue_link = link
    db.add(suggestion)
    db.commit()


@admin_suggestions_router.delete("/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suggestion_by_id(db: db_dependency, user: user_dependency, suggestion_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    suggestion = db.query(Suggestion).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion not found")
    db.query(Suggestion).filter(Suggestion.id == suggestion_id).delete()
    db.commit()


admin_users_router = APIRouter(
    prefix='/admin/users',
    tags=['Admin']
)


@admin_users_router.get("", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    users = db.query(User.id, User.username, User.role).all()
    return [{"id": user.id, "username": user.username, 'role': user.role} for user in users]


@admin_users_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(db: db_dependency, user: user_dependency, user_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    user = db.query(User.id, User.username, User.role).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {'id': user.id, 'username': user.username, 'role': user.role}


@admin_users_router.put("/toggle-admin/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def toggle_user_admin(db: db_dependency, user: user_dependency, user_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Admin privileges")
    user = db.query(User).filter(User.id == user_id).first()
    user_role = db.query(User.role).filter(User.id == user_id).first()
    admins_count = db.query(func.count(User.role)).filter(User.role == 'admin').one()
    if user_role.role == 'admin' and admins_count[0] > 1:
        user.role = 'user'
        db.add(user)
        db.commit()
    elif user_role.role == 'admin' and admins_count[0] <= 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="There has to be at least one admin")
    elif user_role.role == 'user':
        user.role = 'admin'
        db.add(user)
        db.commit()