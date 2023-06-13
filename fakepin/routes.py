# criar as rotas do site
from flask import Flask, render_template, url_for
from fakepin import app

@app.route("/")
def homepage():
  return render_template("homepage.html")

@app.route("/perfil/<usuario>")
def perfil(usuario):
  return render_template("perfil.html", usuario=usuario)