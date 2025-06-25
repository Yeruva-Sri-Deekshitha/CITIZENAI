from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def save(self, db):
        user_data = {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
        return db.users.insert_one(user_data)

    @staticmethod
    def find_by_email(db, email):
        return db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(db, user_id):
        return db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)