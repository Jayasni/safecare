
from app.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole


def promote_user_to_admin():
    email = input("Enter the registered user's email: ").strip()

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            print("User not found. Please register first.")
            return

        user.role = UserRole.ADMIN

        db.commit()
        db.refresh(user)

        print("\nAdmin role assigned successfully!")
        print("Name:", user.full_name)
        print("Email:", user.email)
        print("Role:", user.role.value)

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    promote_user_to_admin()
