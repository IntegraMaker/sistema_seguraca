from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .acesso import Base

class Administrador(Base):
    __tablename__ = "administradores"

    nome = Column("nome", String(255), nullable=False)
    id = Column("id", String(20), primary_key=True)
    cargo = Column("cargo", String(40), nullable=False)
    senha = Column("senha", String(255), nullable=False)

class Pessoa(Base):
    __tablename__ = "pessoas"

    nome = Column("nome", String(255), nullable=False)
    cpf = Column("cpf", String(11), primary_key=True)
    cargo = Column("cargo", String(20), nullable=False)
    matricula = Column("matricula", String(30), nullable=True)
    curso = Column("curso", String(100), nullable=True)
    foto = Column("foto", String(100), nullable=False)
    token_acesso = Column("token_acesso", String(36), nullable=True)
    qrcode = Column("qrcode", String(100), nullable=True)
    validade_qrcode = Column("validade_qrcode", DateTime, nullable=True)

    veiculos = relationship("Veiculo", backref="proprietario")
    visitas = relationship("Visita", backref="visitante")

class Veiculo(Base):
    __tablename__ = "veiculos"

    dono = Column("dono", ForeignKey("pessoas.cpf"), nullable=False)
    nome = Column("nome", String(40), nullable=False)
    cor = Column("cor", String(40), nullable=False)
    placa = Column("placa", String(7), primary_key=True)

class Visita(Base):
    __tablename__ = "visitas"

    cpf = Column("cpf", String(11), ForeignKey("pessoas.cpf"))
    motivo = Column("motivo", String(500), nullable=False)
    data = Column("data", DateTime(), nullable=False, primary_key=True)