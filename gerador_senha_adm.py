from werkzeug.security import generate_password_hash

senha = "adm1"
hash = generate_password_hash(senha)

print(f"Copie este código para o banco de dados:\n{hash}")