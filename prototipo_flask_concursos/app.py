
from flask import Flask, render_template, request, redirect, url_for, flash
import json, os

app = Flask(__name__)
app.secret_key = 'segredo123'

# Funções utilitárias
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            return json.load(f)
    return []

def salvar_dados(arquivo, dados):
    with open(arquivo, 'w') as f:
        json.dump(dados, f, indent=4)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    login = request.form['login']
    senha = request.form['senha']
    usuarios = carregar_dados('data/usuarios.json')
    for u in usuarios:
        if u['login'] == login and u['senha'] == senha:
            return redirect(url_for('home'))
    flash('Usuário ou senha inválidos.')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cadastro_concurso', methods=['GET', 'POST'])
def cadastro_concurso():
    if request.method == 'POST':
        concursos = carregar_dados('data/concursos.json')
        novo = {
            'edital': request.form['edital'],
            'orgao': request.form['orgao'],
            'cargos': request.form['cargos'],
            'localidades': request.form['localidades'],
            'datas': request.form['datas'],
            'criterios': request.form['criterios']
        }
        concursos.append(novo)
        salvar_dados('data/concursos.json', concursos)
        flash('Concurso cadastrado com sucesso!')
        return redirect(url_for('cadastro_concurso'))
    return render_template('cadastro_concurso.html')

@app.route('/inscricao', methods=['GET', 'POST'])
def inscricao():
    concursos = carregar_dados('data/concursos.json')
    if request.method == 'POST':
        inscricoes = carregar_dados('data/inscricoes.json')
        nova = {
            'nome': request.form['nome'],
            'cpf': request.form['cpf'],
            'concurso': request.form['concurso'],
            'cargo': request.form['cargo'],
            'localidade': request.form['localidade']
        }
        inscricoes.append(nova)
        salvar_dados('data/inscricoes.json', inscricoes)
        flash('Inscrição realizada com sucesso!')
        return redirect(url_for('inscricao'))
    return render_template('inscricao.html', concursos=concursos)

@app.route('/alocacao')
def alocacao():
    return render_template('alocacao.html')

@app.route('/correcao')
def correcao():
    return render_template('correcao.html')

if __name__ == '__main__':
    app.run(debug=True)
    