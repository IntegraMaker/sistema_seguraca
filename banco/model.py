from sqlalchemy import Column, String, ForeignKey, DateTime
from .acesso import Base

class Administrador(Base):
    __tablename__ = "administradores"

    nome = Column("nome", String(255), nullable=False)
    id = Column("id", String(20), primary_key=True)
    cargo = Column("cargo", String(40), nullable=False)
    senha = Column("senha", String(18), nullable=False)

    def __init__(self, nome, id, cargo, senha):
        self.nome = nome
        self.id = id
        self.cargo = cargo
        self.senha = senha

    # def __repr__(self):
    #     return self.nome, self.id, self.cargo, self.senha

class Pessoa(Base):
    __tablename__ = "pessoas"

    nome = Column("nome", String(255), nullable=False)
    cpf = Column("cpf", String(11), primary_key=True)
    cargo = Column("cargo", String(20), nullable=False)
    matricula = Column("matricula", String(30), nullable=True)

    def __init__(self, nome, cpf, cargo, matricula):
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.matricula = matricula

    # def __repr__(self):
    #     return f"Pessoa(nome={self.nome!r}, cpf={self.cpf!r}, cargo={self.cargo!r}, veiculo={self.veiculo!r})"
    
class Veiculo(Base):
    __tablename__ = "veiculos"

    dono = Column("dono", ForeignKey("pessoas.cpf"), nullable=False)
    nome = Column("nome", String(40), nullable=False)
    cor = Column("cor", String(40), nullable=False)
    placa = Column("placa", String(7), primary_key=True)

    def __init__(self, dono, nome, cor, placa):
        self.dono = dono
        self.nome = nome
        self.cor = cor
        self.placa = placa


class Visita(Base):
    __tablename__ = "visitas"

    cpf = Column("cpf", String(11), ForeignKey("pessoas.cpf"))
    motivo = Column("motivo", String(500), nullable=False)
    data = Column("data", DateTime(), nullable=False, primary_key=True)

    def __init__(self, cpf, motivo, data):
        self.cpf = cpf
        self.motivo = motivo
        self.data = data

    # def __repr__(self):
    #     return f"Visita(cpf={self.cpf!r}, motivo={self.motivo!r}, data={self.data})"