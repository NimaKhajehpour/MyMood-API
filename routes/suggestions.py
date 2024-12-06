from fastapi import APIRouter, Path, Body, HTTPException
from starlette import status

from di.injection import db_dependency
from di.user_dependency import user_dependency
from models.suggestions import Suggestion, SuggestionRequest

router = APIRouter(
    prefix="/suggestions",
    tags=["Suggestions"]
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_suggestions(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    suggestions = db.query(Suggestion).filter(Suggestion.user_id == user.get('id')).all()
    return suggestions


@router.get("/{suggestion_id", status_code=status.HTTP_200_OK)
async def get_suggestion_by_id(db: db_dependency, user: user_dependency, suggestion_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    suggestion = db.query(Suggestion).filter(Suggestion.user_id == user.get('id')).filter(Suggestion.id == suggestion_id).first()
    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Suggestion not found")
    return suggestion


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_suggestion(db: db_dependency, user: user_dependency, created_suggestion: SuggestionRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    suggestion = Suggestion(**created_suggestion.model_dump(), username=user.get('sub'), user_id=user.get('id'))
    db.add(suggestion)
    db.commit()