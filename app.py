import os
from datetime import *
from flask import *
from blueprints.pessoa_bp import pessoa_bp
from werkzeug.utils import secure_filename
from banco.DAO import *
from dotenv import load_dotenv
import qrcode
import hashlib

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'img_pessoas'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.register_blueprint(pessoa_bp)

if not os.path.exists(f"static/{app.config['UPLOAD_FOLDER']}"):
    os.makedirs(f"static/{app.config['UPLOAD_FOLDER']}")

if not os.path.exists(f"static/qrcode_pessoas"):
    os.makedirs(f"static/qrcode_pessoas")

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

@app.route('/cadastro_qrcode', methods=['post', 'get'])
def cadastro_qrcode():
    if "id" in session:
        if request.method == "POST":
            cpf = request.form.get("cpf")
            registro = buscaPessoa(cpf)

            if registro:
                try:
                    with open(registro.foto, "rb") as img_file:
                        image_bytes = img_file.read()
                        image_hash = hashlib.sha256(image_bytes).hexdigest()
                    

                    print(image_hash)

                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=20,
                        border=2
                    )
                    qr.add_data(image_hash)
                    qr.make(fit=True)
                    imagem = qr.make_image(fill_color='black', back_color='white')

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    nome_seguro = f"{timestamp}_{registro.nome}.png"
                    caminho_completo = os.path.join(f"static/qrcode_pessoas", nome_seguro)

                    imagem.save(caminho_completo)
                    resultado = cadastrarQRCodePessoa(cpf, caminho_completo)
                    print(resultado)

                    return render_template("cadastro_qrcode.html", mensagem="✅QRCode cadastrado com Sucesso!")
                except:
                    print("Error: Ao criar o QRCode!")

            return render_template("cadastro_qrcode.html", mensagem="❌Erro ao cadastrar QRCode!")

        return render_template("cadastro_qrcode.html", mensagem="")

    return render_template("login.html")


@app.route('/cadastro_pessoa', methods=['post', 'get'])
def cadastro_pessoa():
    if "id" in session:
        if request.method == 'POST':
            nome = request.form.get("nome")
            cpf = request.form.get("cpf")
            cargo = request.form.get("cargo")
            matricula = request.form.get("matricula")
            curso = request.form.get("curso")
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

                    # cadastrar QRCode
                    try:
                        with open(caminho_completo, "rb") as img_file:
                            image_bytes = img_file.read()
                            image_hash = hashlib.sha256(image_bytes).hexdigest()
                        

                        print(image_hash)

                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=20,
                            border=2
                        )
                        qr.add_data(image_hash)
                        qr.make(fit=True)
                        imagem = qr.make_image(fill_color='black', back_color='white')

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        nome_seguro = f"{timestamp}_{nome}.png"
                        caminho_QRCode = os.path.join(f"static/qrcode_pessoas", nome_seguro)

                        imagem.save(caminho_QRCode)
                        resultado = cadastrarQRCodePessoa(cpf, caminho_QRCode)
                        print(resultado)
                        
                    except Exception as e:
                        return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500


                    # Cadastrar pessoa, e veiculo
                    resultado = criarPessoa(nome, cpf, cargo, matricula, caminho_completo, curso)
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
