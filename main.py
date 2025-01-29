from fastapi import Depends, FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Expense model
class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    amount = Column(Float)

# FastAPI app
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_expenses/")
def create_expenses(db: Session = Depends(get_db)):
    expenses = [
        Expense(description="Food", amount=10.5),
        Expense(description="Transport", amount=5.0),
        Expense(description="Utilities", amount=100.0),
        Expense(description="Entertainment", amount=50.0),
        Expense(description="Rent", amount=500.0),
        Expense(description="Insurance", amount=200.0),
        Expense(description="Clothing", amount=30.0),
        Expense(description="Medical", amount=15.0),
        Expense(description="Miscellaneous", amount=25.0),
        Expense(description="Savings", amount=100.0)
    ]
    db.add_all(expenses)
    db.commit()
    return {"message": "Expenses created"}

@app.get("/expenses/")
def get_expenses(db: Session = Depends(get_db)):
    expenses = db.query(Expense).all()
    return {"expenses": expenses}
