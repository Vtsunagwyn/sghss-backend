from database import db

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))
