from .acesso import Session, db
from .model import *
from sqlalchemy.exc import IntegrityError
from datetime import *


def criar_banco():
    Base.metadata.create_all(bind=db)


criar_banco()


def criarPessoa(nome, cpf, cargo, matricula):
    db = Session()
    nova_pessoa = Pessoa(nome=nome, cpf=cpf, cargo=cargo, matricula=matricula)
    exito = False
    try:
        db.add(nova_pessoa)
        db.commit()
        exito = True
    except IntegrityError:
        db.rollback()
        print("Error: Ao criar Pessoa!")
    finally:
        db.close()
    return exito


def listarPessoas():
    db = Session()
    saida = db.query(Pessoa).filter().all()
    db.close()
    return saida


def listarPessoasNome(nome):
    db = Session()
    saida = db.query(Pessoa).filter(Pessoa.nome.ilike(f"%{nome}%")).all()
    db.close()
    return saida


def buscaPessoa(cpf):
    db = Session()
    saida = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    db.close()
    return saida


def buscarAdministrador(id):
    db = Session()
    saida = db.query(Administrador).filter(Administrador.id == id).first()
    db.close()
    saida = {
        "nome": saida.nome,
        "id": saida.id,
        "cargo": saida.cargo,
        "senha": saida.senha
    }
    return saida


def criarVeiculo(cpf, nome, cor, placa):
    db = Session()
    novo_veiculo = Veiculo(dono=cpf, nome=nome, cor=cor, placa=placa)
    exito = False
    try:
        db.add(novo_veiculo)
        db.commit()
        exito = True
    except IntegrityError:
        db.rollback()
        print("Error: Ao criar Veiculo!")
    finally:
        db.close()
    return exito


def cadastrarVisita(cpf, motivo):
    data = datetime.now()
    print(data)
    db = Session()
    nova_visita = Visita(cpf=cpf, motivo=motivo, data=data)
    exito = False
    try:
        db.add(nova_visita)
        db.commit()
        exito = True
    except IntegrityError:
        db.rollback()
        print("Error: Ao inserir visita!")
    finally:
        db.close()
    return exito


def listarVisitas(paginaAtual=1, visitasPagina=10):
    offset = (paginaAtual - 1) * visitasPagina
    db = Session()
    visitas = db.query(Visita).order_by(Visita.data.desc()).offset(offset).limit(visitasPagina).all()
    total = db.query(Visita).count()
    db.close()
    return {
        'visitas': visitas,
        'total': total,
        'paginaAtual': paginaAtual,
        'visitaPagina': visitasPagina,
        'paginas': (total + visitasPagina - 1) // visitasPagina
    }