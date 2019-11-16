# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #instanciando Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db' #define um caminho para o arquivo de db, na pasta do projeto

db = SQLAlchemy(app)

class Cliente(db.Model): #criando a classe cliente
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(50), nullable=False) 
  address = db.Column(db.String(200), nullable=False)
  phone = db.Column(db.Integer, nullable=False)
  email = db.Column(db.String(100), nullable=False)
  datetime = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self): #função que retorna seu id sempre que é instanciada
    return '<Cliente %r>' % self.id

@app.route('/', methods=['POST', 'GET']) #definindo comportamentos da rota raíz: 
def index():
  if request.method == 'POST': 
    #pegando os dados recebidos do formulário
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    email = request.form['email']

    #criando novo cliente a partir dos dados
    novo_cliente = Cliente(name=name, address=address, phone=phone, email=email)

    #adicionando cliente ao banco de dados
    try:
      db.session.add(novo_cliente)
      db.session.commit()
      return redirect('/')

    except:
      return 'Houve um erro ao cadastrar novo cliente.'

  else:
    clientes = Cliente.query.order_by(Cliente.datetime).all()
    return render_template('index.html', clientes=clientes) #retorna a página index.html dentro da pasta de templates

@app.route('/excluir/<int:id>') #definindo comportamento da rota excluir
def delete(id):
  cliente = Cliente.query.get_or_404(id) #pega o objeto cliente do banco de dados com o id ou recebe 404

  #exluindo cliente do banco de dados
  try:
    db.session.delete(cliente)
    db.session.commit()
    return redirect('/')
  
  except:
    return 'Houve um erro ao excluir o cliente.'


@app.route('/atualizar/<int:id>', methods=['POST', 'GET']) #definindo comportamento da rota atualizar
def atualizar(id):
  cliente = Cliente.query.get_or_404(id) #pega o objeto cliente do banco de dados com o id ou recebe 404

  if request.method == 'POST':
    #atualiza dados do cliente no banco de dados com os dados fornecidos no formulário enviado
    cliente.name = request.form['name']
    cliente.address = request.form['address']
    cliente.phone = request.form['phone']
    cliente.email = request.form['email']

    #comita alteração no banco de dados
    try:
      db.session.commit()
      return redirect('/')

    except:
      return 'Houve um erro ao atualizar o cliente.'
  
  else:
    return render_template('atualizar.html', cliente=cliente)

if __name__ == '__main__':
  app.run(debug=True)
