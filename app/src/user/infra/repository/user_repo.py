from utils.database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO
from user.infra.db_models.user import User
from fastapi import HTTPException
from utils.helpers import row_to_dict


class UserRepository(IUserRepository):
    async def save(self, user:UserVO):
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        async with SessionLocal() as db:
            db.add(new_user)
            await db.commit()

    def find_by_email(self, email:str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=422)
        
        return UserVO(**row_to_dict(user))
