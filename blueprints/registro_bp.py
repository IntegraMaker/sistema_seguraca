from flask import *
from banco.DAO import *

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