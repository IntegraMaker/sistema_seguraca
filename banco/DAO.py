from .acesso import Session, db
from .model import *
from sqlalchemy.exc import IntegrityError
from datetime import *
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()

def criar_banco():
    Base.metadata.create_all(bind=db)

criar_banco()

def criarPessoa(nome, cpf, cargo, matricula, foto, curso=None):
    with get_session() as session:
        try:
            nova_pessoa = Pessoa(nome=nome, cpf=cpf, cargo=cargo, matricula=matricula, foto=foto, curso=curso)
            session.add(nova_pessoa)
            session.commit()
            return True
        except IntegrityError:
            print("Error: Ao criar Pessoa!")
            return False

def listarPessoas(paginaAtual=1, totalPagina=10):
    offset = (paginaAtual - 1) * totalPagina
    with get_session() as session:
        pessoas = session.query(Pessoa).offset(offset).limit(totalPagina).all()
        total = session.query(Pessoa).count()
        session.expunge_all()
        
        return {
            'pessoas': pessoas,
            'total': total,
            'paginaAtual': paginaAtual,
            'totalPagina': totalPagina,
            'paginas': (total + totalPagina - 1) // totalPagina
        }

def listarPessoasNome(nome, paginaAtual=1, totalPagina=10):
    offset = (paginaAtual - 1) * totalPagina
    with get_session() as session:
        pessoas = session.query(Pessoa).filter(Pessoa.nome.ilike(f"%{nome}%")).offset(offset).limit(totalPagina).all()
        total = session.query(Pessoa).filter(Pessoa.nome.ilike(f"%{nome}%")).count()
        session.expunge_all()

        return {
            'pessoas': pessoas,
            'total': total,
            'paginaAtual': paginaAtual,
            'totalPagina': totalPagina,
            'paginas': (total + totalPagina - 1) // totalPagina
        }

def buscaPessoa(cpf):
    with get_session() as session:
        saida = session.query(Pessoa).filter(Pessoa.cpf == cpf).first()
        if saida:
            session.expunge(saida)
        return saida

def buscarPessoaPorToken(token_uuid):
    with get_session() as session:
        try:
            pessoa = session.query(Pessoa).filter(Pessoa.token_acesso == token_uuid).first()
            if pessoa:
                session.expunge(pessoa)
                return pessoa
        except Exception as e:
            print(f"Erro ao buscar token: {e}")
        return None

def cadastrarQRCodePessoa(cpf, caminhoQRCode, token_acesso, validade):
    with get_session() as session:
        try:
            session.query(Pessoa).filter(Pessoa.cpf == cpf).update({
                Pessoa.qrcode: caminhoQRCode,
                Pessoa.token_acesso: token_acesso,
                Pessoa.validade_qrcode: validade
            })
            session.commit()
            return True
        except IntegrityError:
            print("Error: Ao Registrar QRCode!")
            return False

def renovarValidadeQRCode(cpf, nova_data_validade):
    with get_session() as session:
        try:
            session.query(Pessoa).filter(Pessoa.cpf == cpf).update({
                Pessoa.validade_qrcode: nova_data_validade
            })
            session.commit()
            return True
        except Exception as e:
            print(f"Error: Ao renovar QRCode: {e}")
            return False

def buscarAdministrador(id):
    with get_session() as session:
        saida = session.query(Administrador).filter(Administrador.id == id).first()
        if saida:
            return {
                "nome": saida.nome,
                "id": saida.id,
                "cargo": saida.cargo,
                "senha": saida.senha
            }
        return None

def criarVeiculo(cpf, nome, cor, placa):
    with get_session() as session:
        try:
            novo_veiculo = Veiculo(dono=cpf, nome=nome, cor=cor, placa=placa)
            session.add(novo_veiculo)
            session.commit()
            return True
        except IntegrityError:
            print("Error: Ao criar Veiculo!")
            return False

def cadastrarVisita(cpf, motivo):
    data = datetime.now()
    print(data)
    with get_session() as session:
        try:
            nova_visita = Visita(cpf=cpf, motivo=motivo, data=data)
            session.add(nova_visita)
            session.commit()
            return True
        except IntegrityError:
            print("Error: Ao inserir visita!")
            return False

def listarVisitas(paginaAtual=1, visitasPagina=10):
    offset = (paginaAtual - 1) * visitasPagina
    with get_session() as session:
        visitas = session.query(Visita).order_by(Visita.data.desc()).offset(offset).limit(visitasPagina).all()
        total = session.query(Visita).count()
        session.expunge_all()

        return {
            'visitas': visitas,
            'total': total,
            'paginaAtual': paginaAtual,
            'visitaPagina': visitasPagina,
            'paginas': (total + visitasPagina - 1) // visitasPagina
        }

def contarTotalPessoas():
    with get_session() as session:
        return session.query(Pessoa).count()

def contarVisitasHoje():
    inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    fim = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    with get_session() as session:
        return session.query(Visita).filter(Visita.data >= inicio, Visita.data <= fim).count()

def renovarValidadeLista(lista_cpfs, nova_data):
    with get_session() as session:
        try:
            session.query(Pessoa).filter(Pessoa.cpf.in_(lista_cpfs)).update(
                {Pessoa.validade_qrcode: nova_data}, 
                synchronize_session=False
            )
            session.commit()
            return True
        except Exception as e:
            print(f"Erro na renovação em massa: {e}")
            return False