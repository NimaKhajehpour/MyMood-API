from fastapi import APIRouter, HTTPException, Path
from starlette import status

from di.injection import db_dependency
from di.user_dependency import user_dependency
from models.bugs import Bug, BugRequest

router = APIRouter(
    prefix="/bugs",
    tags=["Bugs"]
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_bugs(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    bugs = db.query(Bug).filter(Bug.user_id == user.get('id')).all()
    return bugs


@router.get("/{bug_id}", status_code=status.HTTP_200_OK)
async def get_bug_by_id(db: db_dependency, user: user_dependency, bug_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    bug = db.query(Bug).filter(Bug.user_id == user.get('id')).filter(Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bug report not found")
    return bug


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_bug(db: db_dependency, user: user_dependency, created_bug: BugRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    bug = Bug(**created_bug.model_dump(), user_id=user.get('id'), username=user.get('sub'))
    db.add(bug)
    db.commit()