from flask import *
from banco.DAO import *

pessoa_bp = Blueprint("pessoa", __name__, url_prefix="/pessoa")

@pessoa_bp.route("/carteira", methods=["get", "post"])
def carteiraPessoa():
    if "id" in session:
        cpf = request.values.get("cpf")
        registro = buscaPessoa(cpf)
        estadoQrcode = "Gere o QRCode!"
        if registro.qrcode:
            caminho = (str(registro.qrcode).split("\\"))
            qrCode = caminho[1].split("_")
            print(qrCode[0])
            estadoQrcode = "Válido"
            if (int(datetime.now().strftime("%Y%m%d")) - int(qrCode[0])) > 30000:
                estadoQrcode = "Inválido"
            print(estadoQrcode)

        return render_template("pessoa/carteira.html", dadosPessoa=registro, estadoQrcode=estadoQrcode)
    return render_template("login.html")