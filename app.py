import os
from flask import *
from dotenv import load_dotenv
from banco.DAO import *
from blueprints.pessoa_bp import pessoa_bp
from blueprints.cadastro_bp import cadastro_bp
from blueprints.registro_bp import registro_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'img_pessoas'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.register_blueprint(pessoa_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(registro_bp)

if not os.path.exists(f"static/{app.config['UPLOAD_FOLDER']}"):
    os.makedirs(f"static/{app.config['UPLOAD_FOLDER']}")

if not os.path.exists(f"static/qrcode_pessoas"):
    os.makedirs(f"static/qrcode_pessoas")


@app.route('/', methods=["GET", "POST"])
def pagina_login():
    if request.method == "POST":
        id = str(request.form.get("id"))
        senha = request.form.get("senha")
        try:
            dados = buscarAdministrador(id)
            if (id == dados["id"]) and (senha == dados["senha"]):
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


@app.route('/home')
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


if __name__ == '__main__':
    # app.run(host= "0.0.0.0", debug = True , port = 80)
    app.run()
