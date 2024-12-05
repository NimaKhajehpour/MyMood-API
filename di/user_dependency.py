from typing import Annotated
from utils.auth_utils import get_current_user

user_dependency = Annotated[dict, get_current_user]