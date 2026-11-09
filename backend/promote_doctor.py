
from app.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole


def promote_user_to_doctor():
    email = input("Enter the registered doctor's email: ").strip()

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == email
        ).first()

        if user is None:
            print("User not found. Register first.")
            return

        if user.doctor_profile:
            print("This user already has a doctor profile.")
            return

        user.role = UserRole.DOCTOR

        db.commit()
        db.refresh(user)

        print("\nDoctor role assigned successfully!")
        print("Name:", user.full_name)
        print("Email:", user.email)
        print("User ID:", user.id)
        print("Role:", user.role.value)

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    promote_user_to_doctor()
