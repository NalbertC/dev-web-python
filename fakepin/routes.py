# criar as rotas do site
from flask import Flask, render_template, url_for, redirect
from fakepin import app, database, bcrypt
from flask_login import login_required, login_user,logout_user, current_user
from fakepin.forms import FormLogin,FormCriarConta, FormFoto
from fakepin.models import Usuario, Foto
import os
from werkzeug. utils import secure_filename
import uuid


@app.route("/login",methods=["GET","POST"])
def homepage():
  formLogin = FormLogin()
  if formLogin.validate_on_submit():
    usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
    if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
      login_user(usuario)
      return redirect(url_for("perfil", id_usuario=usuario.id))

  return render_template("homepage.html", form=formLogin)


@app.route("/criar-conta",methods=["GET","POST"])
def criarconta():
  formCriarConta = FormCriarConta()
  if formCriarConta.validate_on_submit():
    senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
    usuario = Usuario(username=formCriarConta.username.data, email=formCriarConta.email.data, senha=senha)

    # cria o usuário no banco
    database.session.add(usuario)
    database.session.commit()

    login_user(usuario, remember=True)
    # redirecionamento
    return redirect(url_for("perfil", id_usuario=usuario.id))

  return render_template("criarconta.html", form=formCriarConta)


@app.route("/perfil/<id_usuario>",methods=["GET","POST"])
@login_required
def perfil(id_usuario):
  usuario = Usuario.query.get(int(id_usuario))
  # verifica se é o próprio usuário logado
  if int(id_usuario )== int(current_user.id):
    form_foto = FormFoto()
    if form_foto.validate_on_submit():
      arquivo = form_foto.foto.data

      uuid_obj = uuid.uuid4()
      uuid_str = str(uuid_obj)

      nome_seguro = secure_filename(uuid_str +"-"+ arquivo.filename)

      url = "http://localhost:5000/"+ app.config["UPLOAD_FOLDER"] + "/"+nome_seguro
      caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],nome_seguro)
      # salvar arquivo na pasta desejada
      arquivo.save(caminho)
      foto = Foto(imagem=nome_seguro, id_usuario=int(current_user.id), url=url)
      database.session.add(foto)
      database.session.commit()

    return render_template("perfil.html", usuario=current_user, form=form_foto)
  else:
    # asdas
    usuario = Usuario.query.get(int(id_usuario))
    return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("homepage"))


@app.route("/")
@login_required
def feed():
  fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
  return render_template("feed.html" , fotos=fotos)