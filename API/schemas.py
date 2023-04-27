from pydantic import BaseModel


class LegalProceeding(BaseModel):
    date: str
    title: str
    content: str


class ProcessDetail(BaseModel):
    process_num: str
    jurisdictional_unit: str
    action: str
    actors: str
    defendant: str
    legal_proceedings: list[LegalProceeding]