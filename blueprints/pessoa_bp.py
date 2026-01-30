from flask import *
from banco.DAO import *
from datetime import datetime, timedelta

pessoa_bp = Blueprint("pessoa", __name__, url_prefix="/pessoa")

@pessoa_bp.route("/carteira", methods=["get", "post"])
def carteiraPessoa():
    if "id" in session:
        cpf = request.values.get("cpf")
        registro = buscaPessoa(cpf)
        estadoQrcode = "Gere o QRCode!"
        validade_formatada = None

        if registro and registro.qrcode:
            estadoQrcode = "Válido"
            
            if registro.validade_qrcode:
                validade_formatada = registro.validade_qrcode.strftime("%d/%m/%Y")
                if registro.validade_qrcode < datetime.now():
                    estadoQrcode = "Inválido"

        return render_template("pessoa/carteira.html", dadosPessoa=registro, estadoQrcode=estadoQrcode, validade=validade_formatada)
    return render_template("login.html")

@pessoa_bp.route("/renovar_qrcode", methods=["POST"])
def renovar_qrcode():
    if "id" in session:
        cpf = request.form.get("cpf")
        if cpf:
            nova_validade = datetime.now() + timedelta(days=365)
            renovarValidadeQRCode(cpf, nova_validade)
            return redirect(url_for("pessoa.carteiraPessoa", cpf=cpf))
    return render_template("login.html")