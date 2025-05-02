# seed.py
from faker import Faker
from src import db, app
from src.models.user_model import User

fake = Faker()
with app.app_context():
    print("Starting seed...")
    User.query.delete()
    new_users = []
    for _ in range(20):
        username = fake.user_name()
        email = fake.email()
        new_user = User(name=username, email=email)
        new_users.append(new_user)
    db.session.add_all(new_users)
    db.session.commit()
    print("Successfully seeded")