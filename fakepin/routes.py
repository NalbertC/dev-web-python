# criar as rotas do site
from flask import Flask, render_template, url_for, redirect
from fakepin import app, database, bcrypt
from flask_login import login_required, login_user,logout_user, current_user
from fakepin.forms import FormLogin,FormCriarConta
from fakepin.models import Usuario, Foto


@app.route("/",methods=["GET","POST"])
def homepage():
  formLogin = FormLogin()
  if formLogin.validate_on_submit():
    usuario = Usuario.query.filter_by(email=formLogin.email.data).first()
    if usuario and  bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
      login_user(usuario)
      return redirect(url_for("perfil", usuario=usuario.username))

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
    return redirect(url_for("perfil", usuario=usuario.username))

  return render_template("criarconta.html", form=formCriarConta)


@app.route("/perfil/<usuario>")
@login_required
def perfil(usuario):
  return render_template("perfil.html", usuario=usuario)


@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("homepage"))


