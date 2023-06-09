from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder


from . import models, schemas


def create_legal_proceedings(db: Session, legal_proceedings: schemas.LegalProceeding) -> list:
    """
    Create legal proceedings in the database.

    :param db: database session
    :param legal_proceedings: list of legal proceedings to create
    :return: list of created legal proceedings
    """
    all_process = []
    for process in legal_proceedings:
        date = process.date
        title = process.title
        content = process.content

        db_process = models.LegalProceeding(date=date,
                                            title=title,
                                            content=content)

        all_process.append(db_process)

    return all_process


def create_process_details(db: Session, process_details: schemas.ProcessDetail):
    """
    Create a process detail and associated legal proceedings in the database.

    :param db: database session
    :param process_details: details of the process to create
    """
    process_num = process_details.process_num
    jurisdictional_unit = process_details.jurisdictional_unit
    action = process_details.action
    actors = process_details.actors
    defendant = process_details.defendant

    db_detail = models.ProcessDetail(process_num=process_num,
                                     jurisdictional_unit=jurisdictional_unit,
                                     action=action,
                                     actors=actors,
                                     defendant=defendant)

    db.add(db_detail)

    proceedings = create_legal_proceedings(db, process_details.legal_proceedings)
    db_detail.legal_proceedings = proceedings

    db.commit()


def get_process(db: Session, skip: int = 0, limit: int = 100) -> list:
    """
    Retrieve a list of process details from the database.

    :param db: database session
    :param skip: number of process details to skip
    :param limit: maximum number of process details to return
    :return: list of process details
    """
    all_processes = db.query(models.ProcessDetail).offset(skip).limit(limit).all()

    json_processes = []
    for process in all_processes:
        legal_proceedings = jsonable_encoder(process.legal_proceedings)
        json_process = jsonable_encoder(process)
        json_process['legal_proceedings'] = legal_proceedings

        json_processes.append(json_process)

    return json_processes
