from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

EXPIRE_TIME = 30
REFRESH_DAYS = 7
ALGORITHM = 'HS256'
SECRET_KEY = 'Test!123'


class JWTUtil:
    @staticmethod
    def token(entity_id: str) -> str:
        payload = {
            'sub': str(entity_id),
            'exp': datetime.utcnow() + timedelta(minutes=EXPIRE_TIME),
        }

        return jwt.encode(payload, SECRET_KEY, ALGORITHM)

    @staticmethod
    def refresh(entity_id: str) -> str:
        payload = {
            'sub': str(entity_id),
            'exp': datetime.utcnow() + timedelta(days=REFRESH_DAYS),
        }

        return jwt.encode(payload, SECRET_KEY, ALGORITHM)

    @staticmethod
    def verify(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            return payload.get('sub')
        except JWTError:
            return None
