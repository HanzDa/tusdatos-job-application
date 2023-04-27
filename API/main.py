from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create-process/")
def create_process(process_details: schemas.ProcessDetail, db: Session = Depends(get_db)):
    return crud.create_process_details(db=db, process_details=process_details)


@app.get("/get-processes/", response_model=list[schemas.ProcessDetail])
def get_process(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    process = crud.get_process(db, skip=skip, limit=limit)
    return process
