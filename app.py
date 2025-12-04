from flask import Flask, request, jsonify
from database import db, init_db
from models import Paciente

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sghss.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return {"message": "SGHSS API - Online"}

# ------------------------------------------------------------
# CADASTRAR PACIENTE
# ------------------------------------------------------------
@app.route("/pacientes", methods=["POST"])
def cadastrar_paciente():
    data = request.json

    if not data.get("cpf"):
        return {"erro": "CPF é obrigatório"}, 400

    existente = Paciente.query.filter_by(cpf=data["cpf"]).first()
    if existente:
        return {"erro": "CPF já está cadastrado"}, 400

    paciente = Paciente(
        nome=data.get("nome"),
        cpf=data.get("cpf"),
        data_nascimento=data.get("data_nascimento"),
        telefone=data.get("telefone"),
        email=data.get("email")
    )

    db.session.add(paciente)
    db.session.commit()

    return {"mensagem": "Paciente cadastrado com sucesso", "id": paciente.id}, 201


# ------------------------------------------------------------
# LISTAR PACIENTES
# ------------------------------------------------------------
@app.route("/pacientes", methods=["GET"])
def listar_pacientes():
    pacientes = Paciente.query.all()
    lista = [
        {
            "id": p.id,
            "nome": p.nome,
            "cpf": p.cpf,
            "email": p.email,
            "telefone": p.telefone
        }
        for p in pacientes
    ]
    return jsonify(lista)


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
