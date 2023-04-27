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
    """
    Create a new process in the database.

    Args:
    - process_details (schemas.ProcessDetail): Details of the process to be created.
    - db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
    - None
    """
    return crud.create_process_details(db=db, process_details=process_details)



@app.get("/get-processes/", response_model=list[schemas.ProcessDetail])
def get_process(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get a list of processes from the database.

    Args:
    - skip (int, optional): Number of processes to skip. Defaults to 0.
    - limit (int, optional): Maximum number of processes to retrieve. Defaults to 50.
    - db (Session, optional): Database session object. Defaults to Depends(get_db).

    Returns:
    - list[schemas.ProcessDetail]: List of process details.
    """
    process = crud.get_process(db, skip=skip, limit=limit)
    return process
