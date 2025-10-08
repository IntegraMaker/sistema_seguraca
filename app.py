import os
from flask import *
from banco.DAO import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/', methods=["GET", "POST"])
def paginaLogin():
    if request.method == "POST":
        id = request.form.get("id")
        senha = request.form.get("senha")
        try:
            dados = buscarAdministrador(id)
            if (str(id) == dados["id"]) and (senha == dados["senha"]):
                session["nome"] = dados["nome"]
                session["id"] = dados["id"]
                session["cargo"] = dados["cargo"]
                return pagina_inicial()
        except Exception as e:
            print(f"An error occurred: {e} \n\n\n\n\n ")
            return render_template("login.html", msg = "Erro ao fazer login!")
        
    if "id" in session:
        lista = listarPessoas()
        return render_template("index.html", listaPessoas = lista)
    
    return render_template('login.html')


@app.route('/pagina_inicial')
def pagina_inicial():
    if "id" in session:
        pesquisa = request.values.get("pesquisar")
        if pesquisa:
            lista = listarPessoasNome(pesquisa)
            return render_template("index.html", listaPessoas=lista)

        lista = listarPessoas()
        return render_template("index.html", listaPessoas=lista)
    return render_template("login.html")


@app.route('/cadastro_visita', methods=['post', 'get'])
def cadastro_visita():
    if "id" in session:
        if request.method == "GET":
            lista = listarVisitas()
            cpf = request.values.get("cpf")
            print(cpf)
            if cpf:
                return render_template('cadastro_visita.html', listaVisitas=lista, cpf=cpf)
            return render_template('cadastro_visita.html', listaVisitas=lista)

        if request.method == "POST":
            cpf = request.form.get("cpf")
            motivo = request.form.get("motivo")
            resultado = cadastrarVisita(cpf, motivo)
            print(resultado)
            if resultado:
                lista = listarVisitas()
                return render_template('cadastro_visita.html', listaVisitas=lista, exito="Visita cadastrada com sucesso!")
            return render_template('cadastro_visita.html', listaVisitas=lista, exito="Cadastro mal sucedido!")
        
    return render_template("login.html")


@app.route('/cadastro_pessoa', methods=['post', 'get'])
def cadastro_pessoa():
    if "id" in session:
        if request.method == 'POST':
            nome = request.form.get("nome")
            cpf = request.form.get("cpf")
            cargo = request.form.get("cargo")
            matricula = request.form.get("matricula")
            temVeiculo = request.form.get("confirmacao")
            print(temVeiculo.lower())
            resultado = criarPessoa(nome, cpf, cargo, matricula)
            print(resultado)
            if temVeiculo.lower() == "sim":
                nome_veiculo = request.form.get("veiculo")
                cor = request.form.get("cor")
                placa = request.form.get("placa")
                resultado = criarVeiculo(cpf, nome_veiculo, cor, placa)
                print(resultado)
        return render_template('cadastro_pessoa.html')
    return render_template("login.html")


@app.route('/cadastro_veiculo', methods=['post', 'get'])
def cadastro_veiculo():
    if "id" in session:
        if request.method == "POST":
            dono = request.form.get("cpf")
            nome = request.form.get("nome")
            cor = request.form.get("cor")
            placa = request.form.get("placa")
            resultado = criarVeiculo(dono, nome, cor, placa)
            print(resultado)
        return render_template('cadastro_veiculo.html')
    return render_template("login.html")


if __name__ == '__main__':
    # app.run(host= "0.0.0.0", debug = True , port = 80)
    app.run()
