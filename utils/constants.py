from fastapi.security import OAuth2PasswordBearer


database_url = "sqlite:///database.db"

date_regex_pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$"

time_regex_pattern = r"^([01]?[0-9]|2[0-3]):([0-5]?[0-9])$"

SECRET_KEY = "e9b798bdb3bf21efa12d94cf66b2e26a52c6566727992b6be736265e8e9340c4"
ALGORITHM = "HS256"

oauth2bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
