from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.sql import func
from database.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    complete_name = Column(String(255), nullable=False)
    
    # apenas email vw ou sesé
    email = Column(String(255), nullable=False)

    # criptografada
    password

    # ativo ou inativo
    status

    # permissões
    roles 

    created_at
    updated_at
