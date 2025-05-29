import random
from faker import Faker
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Agent, Highlight, Review, Rating
from passlib.hash import bcrypt

fake = Faker()

# Drop and recreate all tables (for development only!)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# --- USERS ---
users = []
for _ in range(10):
    user = User(
        username=fake.user_name(),
        email=fake.email(),
        hashed_password=bcrypt.hash("password"),
        is_admin=False
    )
    db.add(user)
    db.flush()  # Ensure ID is available
    users.append(user)

# Add one admin user
admin_user = User(
    username="admin",
    email="admin@example.com",
    hashed_password=bcrypt.hash("adminpass"),
    is_admin=True
)
db.add(admin_user)
db.flush()
users.append(admin_user)

# --- AGENTS ---
categories = ["tech", "finance", "health", "travel"]
agents = []

for _ in range(15):
    agent = Agent(
        name=fake.name(),
        category=random.choice(categories),
        description=fake.paragraph(nb_sentences=3),
        trending=random.choice([True, False])
    )
    db.add(agent)
    db.flush()
    agents.append(agent)

# --- HIGHLIGHTS ---
highlighted_pairs = set()

for user in users:
    for _ in range(random.randint(1, 4)):
        agent = random.choice(agents)
        pair = (user.id, agent.id)
        if pair not in highlighted_pairs:
            db.add(Highlight(user_id=user.id, agent_id=agent.id))
            highlighted_pairs.add(pair)

# --- REVIEWS ---
for user in users:
    for _ in range(random.randint(1, 3)):
        agent = random.choice(agents)
        if user.id and agent.id:
            db.add(Review(user_id=user.id, agent_id=agent.id, content=fake.sentence()))

# --- RATINGS ---
for user in users:
    for _ in range(random.randint(1, 3)):
        agent = random.choice(agents)
        if user.id and agent.id:
            db.add(Rating(user_id=user.id, agent_id=agent.id, value=round(random.uniform(1.0, 5.0), 1)))

# Commit all
db.commit()
db.close()

print("✅ Fake data seeded successfully.")