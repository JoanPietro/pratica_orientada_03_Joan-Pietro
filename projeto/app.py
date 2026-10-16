from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import Base, SessionLocal, engine
from models import Book, User

app = Flask(__name__)
Base.metadata.create_all(engine)


@app.route('/')
def index():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User).order_by(User.nome)).all()
        livros = session.scalars(
            select(Book).options(selectinload(Book.user)).order_by(Book.titulo)
        ).all()
    return render_template('index.html', usuarios=usuarios, livros=livros)


@app.route('/usuarios/novo', methods=['GET'])
def usuarios_novo_form():
    return render_template('user_form.html')


@app.route('/usuarios/novo', methods=['POST'])
def usuarios_novo():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip()

    if not nome or not email:
        return render_template('user_form.html'), 400

    with SessionLocal() as session:
        usuario = User(nome=nome, email=email)
        session.add(usuario)
        session.commit()

    return redirect(url_for('index'))


@app.route('/livros/novo', methods=['GET'])
def livros_novo_form():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User).order_by(User.nome)).all()
    return render_template('book_form.html', usuarios=usuarios)


@app.route('/livros/novo', methods=['POST'])
def livros_novo():
    titulo = request.form.get('titulo', '').strip()
    user_id = request.form.get('usuario_id')

    if not titulo or not user_id:
        with SessionLocal() as session:
            usuarios = session.scalars(select(User).order_by(User.nome)).all()
        return render_template('book_form.html', usuarios=usuarios), 400

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)