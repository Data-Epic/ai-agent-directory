import os

from auth.auth import hashed_password
from core.database import SessionLocal
from core.models.user import User
from dotenv import load_dotenv

load_dotenv()

ADMIN_FNAME = os.getenv("ADMIN_FNAME")
ADMIN_LNAME = os.getenv("ADMIN_LNAME")
ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def create_initial_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.is_admin == 1).first()
    if admin:
        print("Admin user already exists.")
        return
    new_admin = User(
        first_name=ADMIN_FNAME,
        last_name=ADMIN_LNAME,
        username=ADMIN_USER,
        email=ADMIN_EMAIL,
        hashed_password=hashed_password(ADMIN_PASSWORD),
        is_admin=1,
    )
    db.add(new_admin)
    db.commit()
    print("Admin user created successfully.")


if __name__ == "__main__":
    create_initial_admin()
