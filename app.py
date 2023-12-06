from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://<andreysilva>:<root>@<SQLATIVIDADE2023>/TestDB?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db = SQLAlchemy(app)

# Modelo de dados
class CalculoIMC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    altura = db.Column(db.Float)
    peso = db.Column(db.Float)
    imc = db.Column(db.Float)

# Rota principal
@app.route('/')
def index():
    dados_imc = CalculoIMC.query.all()
    return render_template('index.html', dados_imc=dados_imc)

# Rota para calcular IMC
@app.route('/calcular_imc', methods=['POST'])
def calcular_imc():
    nome = request.form['nome']
    altura = float(request.form['altura'])
    peso = float(request.form['peso'])

    imc = peso / (altura ** 2)

    novo_calculo = CalculoIMC(nome=nome, altura=altura, peso=peso, imc=imc)
    db.session.add(novo_calculo)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
