from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email , Length, ValidationError, EqualTo
from fakepin.models import Usuario

class FormLogin(FlaskForm):
  email = StringField("E-mail", validators=[DataRequired(),Email()])
  senha =PasswordField("Senha", validators=[DataRequired()])
  botao_confirmacao = SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
  username = StringField("Nome de usuário", validators=[DataRequired()])
  email = StringField("E-mail", validators=[DataRequired(), Email()])
  senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
  confirmacao_senha = PasswordField("Confirmação de senha", validators=[DataRequired(), EqualTo("senha")])
  botao_confirmacao = SubmitField("Criar conta")

  def validate_email(self, email):
    usuario = Usuario.query.filter_by(email=email.data).first()
    if usuario:
      return ValidationError("E-mail já cadastrado, faça login para continuar")


class FormFoto(FlaskForm):
  foto =  FileField("Foto", validators=[DataRequired()])
  botao_confirmacao = SubmitField("Enviar foto")