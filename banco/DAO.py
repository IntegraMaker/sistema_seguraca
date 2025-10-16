from .acesso import Session, db
from .model import *
from sqlalchemy.exc import IntegrityError
from datetime import *


def criar_banco():
    Base.metadata.create_all(bind=db)


criar_banco()


def criarPessoa(nome, cpf, cargo, matricula, foto):
    db = Session()
    nova_pessoa = Pessoa(nome=nome, cpf=cpf, cargo=cargo, matricula=matricula, foto=foto)
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


def listarPessoas(paginaAtual=1, totalPagina=10):
    offset = (paginaAtual - 1) * totalPagina
    db = Session()
    pessoas = db.query(Pessoa).offset(offset).limit(totalPagina).all()
    total = db.query(Pessoa).count()
    db.close()
    return {
        'pessoas': pessoas,
        'total': total,
        'paginaAtual': paginaAtual,
        'totalPagina': totalPagina,
        'paginas': (total + totalPagina - 1) // totalPagina
    }


def listarPessoasNome(nome, paginaAtual=1, totalPagina=10):
    offset = (paginaAtual - 1) * totalPagina
    db = Session()
    pessoas = db.query(Pessoa).filter(Pessoa.nome.ilike(f"%{nome}%")).offset(offset).limit(totalPagina).all()
    total = db.query(Pessoa).filter(Pessoa.nome.ilike(f"%{nome}%")).count()
    db.close()
    return {
        'pessoas': pessoas,
        'total': total,
        'paginaAtual': paginaAtual,
        'totalPagina': totalPagina,
        'paginas': (total + totalPagina - 1) // totalPagina
    }


def buscaPessoa(cpf):
    db = Session()
    saida = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    db.close()
    return saida


def cadastrarQRCodePessoa(cpf, caminhoQRCode):
    db = Session()
    exito = False
    try:
        db.query(Pessoa).filter(Pessoa.cpf == cpf).update({Pessoa.qrcode: caminhoQRCode})
        db.commit()
        exito = True
    except IntegrityError:
        db.rollback()
        print("Error: Ao Registrar QRCode!")
    finally:
        db.close()
    return exito


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