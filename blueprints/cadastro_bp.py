import os
from flask import *
from banco.DAO import *
from werkzeug.utils import secure_filename
import qrcode
import hashlib

cadastro_bp = Blueprint("cadastro", __name__, url_prefix="/cadastro")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@cadastro_bp.route('/qrcode', methods=['post', 'get'])
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

                    return render_template("cadastro/qrcode.html", mensagem="✅QRCode cadastrado com Sucesso!")
                except:
                    print("Error: Ao criar o QRCode!")

            return render_template("cadastro/qrcode.html", mensagem="❌Erro ao cadastrar QRCode!")

        return render_template("cadastro/qrcode.html", mensagem="")

    return render_template("login.html")


@cadastro_bp.route('/pessoa', methods=['post', 'get'])
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
                    caminho_completo = os.path.join(f"static/{current_app.config['UPLOAD_FOLDER']}", nome_seguro)
                    
                    # Salvar arquivo
                    file.save(caminho_completo)
                    print(f"✅ Foto salva: {caminho_completo}")

                    # Cadastrar pessoa, e veiculo
                    resultado = criarPessoa(nome, cpf, cargo, matricula, caminho_completo, curso)
                    print("Cadastro pessoa: ", resultado)
                    if temVeiculo.lower() == "sim":
                        nome_veiculo = request.form.get("veiculo")
                        cor = request.form.get("cor")
                        placa = request.form.get("placa")
                        resultado = criarVeiculo(cpf, nome_veiculo, cor, placa)
                        print("Cadastro veiculo: ", resultado)

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

                    return jsonify({
                        'mensagem': 'Pessoa cadastrada com sucesso!'
                    }), 200
                
                return jsonify({'erro': 'Tipo de arquivo não permitido'}), 400

            except Exception as e:
                return jsonify({'erro': f'Erro interno do servidor: {str(e)}'}), 500

        return render_template('cadastro/pessoa.html')
    return render_template("login.html")


@cadastro_bp.route('/veiculo', methods=['post', 'get'])
def cadastro_veiculo():
    if "id" in session:
        if request.method == "POST":
            dono = request.form.get("cpf")
            nome = request.form.get("nome")
            cor = request.form.get("cor")
            placa = request.form.get("placa")
            resultado = criarVeiculo(dono, nome, cor, placa)
            print(resultado)
        return render_template('cadastro/veiculo.html')
    return render_template("login.html")