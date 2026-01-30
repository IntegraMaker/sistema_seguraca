import os
from flask import *
from banco.DAO import *
from werkzeug.utils import secure_filename
import uuid
import qrcode
import re
from datetime import datetime, timedelta

cadastro_bp = Blueprint("cadastro", __name__, url_prefix="/cadastro")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False
    
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False
    
    return True

# ROTA ALTERADA DE /qrcode PARA /renovacao
@cadastro_bp.route('/renovacao', methods=['post', 'get'])
def renovacao_massa():
    if "id" in session:
        msg = None
        erro = None

        if request.method == "POST":
            cpfs_selecionados = request.form.getlist("cpfs")
            
            if cpfs_selecionados:
                nova_validade = datetime.now() + timedelta(days=365)
                resultado = renovarValidadeLista(cpfs_selecionados, nova_validade)
                
                if resultado:
                    msg = f"Sucesso! {len(cpfs_selecionados)} carteiras foram renovadas por 1 ano."
                else:
                    erro = "Erro ao renovar as carteiras selecionadas."
            else:
                erro = "Nenhuma pessoa foi selecionada."

        pagina = request.args.get("page", 1, type=int)
        lista = listarPessoas(pagina)
        
        # Mantemos o arquivo fisico como qrcode.html para não dar erro
        return render_template("cadastro/qrcode.html", listaPessoas=lista, msg=msg, erro=erro)

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

            cpf_limpo = re.sub(r'[^0-9]', '', cpf)
            if not validar_cpf(cpf_limpo):
                return jsonify({'erro': 'CPF inválido! Verifique os números digitados.'}), 400
            
            cpf = cpf_limpo

            try:
                if 'foto' not in request.files:
                    return jsonify({'erro': 'Foto é obrigatória'}), 400
                
                file = request.files['foto']

                if file.filename == '':
                    return jsonify({'erro': 'Nenhuma foto enviada'}), 400
                
                if file and allowed_file(file.filename):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    nome_original = secure_filename(file.filename)
                    nome_seguro = f"{timestamp}_{nome_original}"
                    caminho_completo = os.path.join(f"static/{current_app.config['UPLOAD_FOLDER']}", nome_seguro)
                    
                    file.save(caminho_completo)
                    print(f"✅ Foto salva: {caminho_completo}")

                    resultado = criarPessoa(nome, cpf, cargo, matricula, caminho_completo, curso)
                    print("Cadastro pessoa: ", resultado)

                    if temVeiculo and temVeiculo.lower() == "sim":
                        nome_veiculo = request.form.get("veiculo")
                        cor = request.form.get("cor")
                        placa = request.form.get("placa")
                        resultado = criarVeiculo(cpf, nome_veiculo, cor, placa)
                        print("Cadastro veiculo: ", resultado)

                    try:
                        token_acesso = str(uuid.uuid4())
                        
                        validade = datetime.now() + timedelta(days=365)

                        print(f"Token Gerado: {token_acesso}, Validade até: {validade}")

                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=20,
                            border=2
                        )
                        qr.add_data(token_acesso)
                        qr.make(fit=True)
                        imagem = qr.make_image(fill_color='black', back_color='white')

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        nome_seguro = f"{timestamp}_{nome}.png"
                        caminho_QRCode = os.path.join(f"static/qrcode_pessoas", nome_seguro)

                        imagem.save(caminho_QRCode)
                        
                        resultado = cadastrarQRCodePessoa(cpf, caminho_QRCode, token_acesso, validade)
                        print(resultado)
                        
                    except Exception as e:
                        return jsonify({'erro': f'Erro ao gerar QR Code: {str(e)}'}), 500

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