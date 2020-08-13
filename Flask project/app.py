from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
#setando a conexao com o banco sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.sqlite3'

#instanciando o banco de dados e passando minha aplicacao como parametro
db = SQLAlchemy(app)
#criando a classe usuario e seus atributos
class Usuario(db.Model):
    id = db.Column('id',db.Integer, primary_key = True, autoincrement=True)
    nome = db.Column(db.String(150))
    sobrenome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    senha = db.Column(db.String(150))
    #construtor da classe
    def __init__(self, nome, sobrenome, email, senha):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha





#definindo as rotas
#mostra a pagina inicial e se tiver usuarios ja cadastrados, ira mostra-los
@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

#metodo de adicionar
#instancia um novo usuario de acordo com o input nos campos 
#adiciona no banco e commita o resultado
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        usuario = Usuario(request.form['nome'],request.form['sobrenome'],request.form['email'],request.form['senha'])
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

#metodo de remover usuario pelo id
#instancia um usuario pelo id, deleta ele e commita
@app.route('/delete/<int:id>')
def delete(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))

#metodo de editar usuario
#instancia o usuario pelo id recebido e faz as alteracoes de acordo
#com os inputs dos campos
@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.sobrenome = request.form['sobrenome']
        usuario.email = request.form['email']
        usuario.senha = request.form['senha']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', usuario=usuario)

#inicializa a aplicacao no moodo debug
#e cria o banco de dados
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,port=80)