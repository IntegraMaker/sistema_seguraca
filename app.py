import os
from datetime import *
from flask import *
from werkzeug.utils import secure_filename
from banco.DAO import *
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'img_pessoas'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

if not os.path.exists(f"static/{app.config['UPLOAD_FOLDER']}"):
    os.makedirs(f"static/{app.config['UPLOAD_FOLDER']}")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        pagina = request.args.get("page", 1, type=int)
        lista = listarPessoas(pagina)
        return render_template("index.html", listaPessoas=lista, pesquisa=None)
    
    return render_template('login.html')


@app.route('/pagina_inicial')
def pagina_inicial():
    if "id" in session:
        pesquisa = request.values.get("pesquisar")
        pagina = request.args.get("page", 1, type=int)
        if pesquisa:
            lista = listarPessoasNome(pesquisa, pagina)
            return render_template("index.html", listaPessoas=lista, pesquisa=pesquisa)

        lista = listarPessoas(pagina)
        return render_template("index.html", listaPessoas=lista, pesquisa=None)
    return render_template("login.html")


@app.route('/cadastro_visita', methods=['post', 'get'])
def cadastro_visita():
    if "id" in session:
        if request.method == "GET":
            pagina = request.args.get("page", 1, type=int)
            lista = listarVisitas(pagina)
            cpf = request.values.get("cpf")
            if cpf:
                return render_template('cadastro_visita.html', listaVisitas=lista, cpf=cpf)
            return render_template('cadastro_visita.html', listaVisitas=lista)

        if request.method == "POST":
            pagina = request.args.get("page", 1, type=int)
            cpf = request.form.get("cpf")
            motivo = request.form.get("motivo")
            resultado = cadastrarVisita(cpf, motivo)
            print(resultado)
            lista = listarVisitas(pagina)
            if resultado:
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
            try:
                if 'foto' not in request.files:
                    return jsonify({'erro': 'Foto é obrigatória'}), 400
                
                file = request.files['foto']

                if file.filename == '':
                    return jsonify({'erro': 'Nenhuma foto enviada'}), 400
                
                if file and allowed_file(file.filename):
                    # Gerar nome seguro para o arquivo
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    nome_original = secure_filename(file.filename)
                    nome_seguro = f"{timestamp}_{nome_original}"
                    caminho_completo = os.path.join(f"static/{app.config['UPLOAD_FOLDER']}", nome_seguro)
                    
                    # Salvar arquivo
                    file.save(caminho_completo)
                    print(f"✅ Foto salva: {caminho_completo}")

                    # Cadastrar pessoa, e veiculo
                    resultado = criarPessoa(nome, cpf, cargo, matricula, caminho_completo)
                    print("Cadastro pessoa: ", resultado)
                    if temVeiculo.lower() == "sim":
                        nome_veiculo = request.form.get("veiculo")
                        cor = request.form.get("cor")
                        placa = request.form.get("placa")
                        resultado = criarVeiculo(cpf, nome_veiculo, cor, placa)
                        print("Cadastro veiculo: ", resultado)

                    return jsonify({
                        'mensagem': 'Pessoa cadastrada com sucesso!'
                    }), 200
                
                return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400

            except Exception as e:
                return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

            
            
            
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
