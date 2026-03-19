from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)


DB_PATH = os.path.join(DB_DIR, "tarefas.db")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DB_PATH
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200), nullable=False)
    feita = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    todas_as_tarefas = Tarefa.query.all()
    return render_template("index.html", lista_de_tarefas=todas_as_tarefas)


@app.route("/criar-tarefa", methods=["POST"])
def criar():
    conteudo = request.form.get("conteudo_tarefa", "").strip()
    if conteudo:
        tarefa = Tarefa(conteudo=conteudo, feita=False)
        db.session.add(tarefa)
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/eliminar-tarefa/<id>")
def eliminar(id):
    Tarefa.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/tarefa-feita/<id>")
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()
    if tarefa:
        tarefa.feita = not tarefa.feita
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
