from flask import *
from banco.DAO import *

pessoa_bp = Blueprint("pessoa", __name__, url_prefix="/pessoa")

@pessoa_bp.route("/carteira", methods=["get", "post"])
def carteiraPessoa():
    if "id" in session:
        cpf = request.values.get("cpf")
        registro = buscaPessoa(cpf)
        return render_template("pessoa/carteira.html", dadosPessoa=registro)
    return render_template("login.html")