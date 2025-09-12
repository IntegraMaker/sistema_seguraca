from flask import *
from banco.DAO import *

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def paginaLogin():
    if request.method == "POST":
        id = request.values.get("id")
        senha = request.values.get("senha")
        try:
            dados = buscarAdministrador(id)

            if (str(id) == dados["id"]) and (senha == dados["senha"]):
                return pagina_inicial()
        except Exception as e:
            print(f"An error occurred: {e} \n\n\n\n\n ")

            # return paginaLogin()
    return render_template('login.html')


@app.route('/pagina_inicial')
def pagina_inicial():
    lista = listarPessoas()
    print(lista)
    return render_template('index.html')


@app.route('/cadastro_visita', methods=['post', 'get'])
def cadastro_visita():
    if request.method == "post":
        cpf = request.values.get("cpf")
        motivo = request.values.get("motivo")
        resultado = cadastrarVisita(cpf, motivo)
        print(resultado)
        return pagina_inicial()

    return render_template('cadastro_visita.html')


@app.route('/cadastro_pessoa', methods=['post', 'get'])
def cadastro_pessoa():
    if request.method == 'post':
        nome = request.values.get("nome")
        cpf = request.values.get("cpf")
        cargo = request.values.get("cargo")
        matricula = request.values.get("matricula")
        temVeiculo = request.values.get("confirmacao")
        print(temVeiculo)
        resultado = criarPessoa(nome, cpf, cargo, matricula)
        print(resultado)
        if temVeiculo.lower() == "sim":
            nome_veiculo = request.values.get("veiculo")
            cor = request.values.get("cor")
            placa = request.values.get("placa")
            resultado = criarVeiculo(cpf, nome_veiculo, cor, placa)
            print(resultado)
            # fazer ligação carro - pessoa no banco
    return render_template('cadastro_pessoa.html')


@app.route('/cadastro_veiculo', methods=['post', 'get'])
def cadastro_veiculo():
    if request.method == "post":
        dono = request.values.get("cpf")
        nome = request.values.get("nome")
        cor = request.values.get("cor")
        placa = request.values.get("placa")
        resultado = criarVeiculo(dono, nome, cor, placa)
        print(resultado)
        # necessario fazer ligação carro - pessoa no banco
    return render_template('cadastro_veiculo.html')


if __name__ == '__main__':
    # app.run(host= "0.0.0.0", debug = True , port = 80)
    app.run()
