from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

    
class ProcessDetail(Base):
    __tablename__ = "process_details"

    id = Column(Integer, primary_key=True, index=True)
    process_num = Column(String, index=True)
    jurisdictional_unit = Column(String, index=True)
    action = Column(String, index=True)
    actors = Column(String, index=True)
    defendant = Column(String, index=True)

    legal_proceedings = relationship("LegalProceeding", backref='process_details')

    def __repr__(self):
        return f'<ProcessDetail {self.id}>'  


class LegalProceeding(Base):
    __tablename__ = "legal_proceedings"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)

    process_detail_id = Column(Integer, ForeignKey("process_details.id"))

    def __repr__(self):
        return f'<LegalProceeding {self.id}>' 
