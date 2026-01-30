from flask import *
from banco.DAO import *
from datetime import datetime

registro_bp = Blueprint("registro", __name__, url_prefix="/registro")

@registro_bp.route('/visita', methods=['post', 'get'])
def registro_visita():
    if "id" in session:
        if request.method == "GET":
            pagina = request.args.get("page", 1, type=int)
            lista = listarVisitas(pagina)
            cpf = request.values.get("cpf")
            if cpf:
                return render_template('registro/visita.html', listaVisitas=lista, cpf=cpf)
            return render_template('registro/visita.html', listaVisitas=lista)

        if request.method == "POST":
            pagina = request.args.get("page", 1, type=int)
            cpf = request.form.get("cpf")
            motivo = request.form.get("motivo")
            resultado = cadastrarVisita(cpf, motivo)
            print(resultado)
            lista = listarVisitas(pagina)
            if resultado:
                return render_template('registro/visita.html', listaVisitas=lista, exito="Visita cadastrada com sucesso!")
            return render_template('registro/visita.html', listaVisitas=lista, exito="Cadastro mal sucedido!")
        
    return render_template("login.html")

@registro_bp.route('/qrcode', methods=['POST', 'GET'])
def registro_qrcode():
    if "id" in session:
        
        if request.method == "POST":
            data = request.json
            token_lido = data.get('conteudo')

            print(f"Token recebido: {token_lido}")

            if not token_lido:
                return jsonify({
                    'sucesso': False, 
                    'mensagem': "Erro: Nenhum código recebido."
                })

            pessoa_encontrada = buscarPessoaPorToken(token_lido)

            if pessoa_encontrada:
                if pessoa_encontrada.validade_qrcode and pessoa_encontrada.validade_qrcode < datetime.now():
                    return jsonify({
                        'sucesso': False,
                        'mensagem': f"ACESSO NEGADO: QR Code Vencido em {pessoa_encontrada.validade_qrcode.strftime('%d/%m/%Y')}."
                    })

                cadastrarVisita(pessoa_encontrada.cpf, "Acesso via QRCode")

                return jsonify({
                    'sucesso': True,
                    'mensagem': f"Acesso Permitido: {pessoa_encontrada.nome}",
                    'dados': {
                        'nome': pessoa_encontrada.nome,
                        'foto': pessoa_encontrada.foto,
                        'cargo': pessoa_encontrada.cargo
                    }
                })
            else:
                return jsonify({
                    'sucesso': False, 
                    'mensagem': "ACESSO NEGADO: QR Code não cadastrado ou inválido."
                })
            
        return render_template('registro/qrcode.html')
    
    return render_template("login.html")