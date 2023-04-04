from flask import (
    Flask, render_template, request, redirect, url_for, flash
)
from entidades import Cliente, Produto, Favorito
from dao import ClienteDao, ProdutoDao, FavoritosDao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wow1001'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/reset_db", methods=["GET"])
def reset_db():
    from database import Database
    Database.create_db()
    Database.import_csv()
    flash(f'Banco de dados Resetado', 'success')
    return redirect(url_for("cliente_index"))
    

# ==================================
# ROTAS (CLIENTE)
# ==================================

@app.route("/cliente/index", methods=["GET"])
def cliente_index():
    dc = ClienteDao()
    clientes = dc.find_all()
    return render_template("cliente_list.html", clientes=clientes)

@app.route("/cliente/new", methods=["GET"])
def cliente_new():
    return render_template("cliente.html", 
                            action='create', 
                            cliente=None)

@app.route("/cliente/edit/<id>", methods=["GET"])
def cliente_edit(id):
    dao = ClienteDao()
    cliente = dao.get_cliente(id)
    return render_template("cliente.html", 
                            cliente=cliente,
                            action='update'
                            )

# -------
# CRUD
# -------

# CREATE
@app.route("/cliente/create", methods=["POST"])
def cliente_create():
    
    nome = request.form.get("nome")
    cep = request.form.get("cep")
    email = request.form.get("email")
    cpf = request.form.get("cpf")

    cliente = Cliente(nome, email, cep=cep, cpf=cpf)

    dao = ClienteDao()
    dao.save(cliente)

    # retornar feedback para o usuário
    flash(f'Cliente "{nome}" cadastrado!', 'success')

    return redirect(url_for("cliente_index"))


# READ
@app.route("/cliente/<id>", methods=["GET"])
def cliente_id(id):
    # dc = ClienteDao()
    # cliente = dc.get_cliente(id)
    # return cliente.__dict__   
    return "<h1>TODO: implementar</h1>"


# UPDATE
@app.route("/cliente/update", methods=["POST"])
def cliente_update():
    
    dao = ClienteDao()
    # obtem o id que foi setado no form
    id = request.form.get("id")

    # obtem o cliente que esta no banco
    cliente = dao.get_cliente(id)

    # atualiza os campos do cliente (todos os campos)
    cliente.nome = request.form.get("nome")
    cliente.cep = request.form.get("cep")
    cliente.email = request.form.get("email")
    cliente.cpf = request.form.get("cpf")

    dao.update(cliente)

    # retornar feedback para o usuário
    flash(f'Cliente "{cliente.nome}" Atualizado!', 'success')

    return redirect(url_for("cliente_index"))


# DELETE
@app.route("/cliente/delete/<id>", methods=["GET"])
def cliente_delete(id):
    dao = ClienteDao()
    dao.delete(id)
    flash(f'Cliente removido com sucesso!', 'success')
    return redirect(url_for('cliente_index'))

# ==================================
# ROTAS (PRODUTO)
# ==================================

#  Lista produtos 

@app.route("/produto/index", methods=["GET"])
def produto_index():
    # Cria objeto DAO
    dc = ProdutoDao()
    # Obtem todos os dados do DB ja mapeados
    produtos = dc.find_all()
    # Retorna a pagina + dados do DB
    return render_template("produto_list.html", produtos=produtos)

# Form de Cadastro produtos

@app.route("/produto/new", methods=["GET"])
def produto_new():
    return render_template("produto.html", 
                            action='create', 
                            produto=None)

# Rota do forms para salvar produtos no DB

@app.route("/produto/create", methods=["POST"])
def produto_create():
    # Obtem os dados do form
    nome = request.form.get("nome")
    preco = request.form.get("preco")
    marca = request.form.get("marca")
    # Cria o produto
    produto = Produto(nome, preco, marca)
    # Cria objeto DAO
    dc = ProdutoDao()
    # Chama o metodo para salvar
    dc.save(produto)
    # Feedback para o usuario
    flash(f'Produto {nome} salvo com sucesso!', 'success')
    # Redirect para a lista de produtos
    return redirect(url_for("produto_index"))

# Form de Edição de produtos

@app.route("/produto/edit/<id>", methods=["GET"])
def produto_edit(id):
    # Cria objeto DAO
    dao = ProdutoDao()
    # Obtem o produto que deseja editar
    produto = dao.find_one(id)
    # Retorna a pagina de cadastro com produto=produto, caindo no if la no html
    return render_template("produto.html", 
                            produto=produto,
                            action='update',
                            )

# Rota do forms para editar produtos (update)

@app.route("/produto/update", methods=["POST"])
def produto_update():
    dao = ProdutoDao()
    # id fornecido pelo formulario
    id = request.form.get("id")
    # obtem o produto
    produto = dao.find_one(id)
    # atualiza os campos do produto
    produto.nome = request.form.get("nome")
    produto.preco = request.form.get("preco")
    produto.marca = request.form.get("marca")
    # Chama o metodo para atualizar o produto
    dao.update(produto)
    # Feedback para o usuário
    flash(f'Produto "{produto.nome}" Atualizado!', 'success')
    return redirect(url_for("produto_index")) 

# DELETE   

@app.route("/produto/delete/<id>", methods=["GET"])
def produto_delete(id):
    # Cria objeto DAO
    dao = ProdutoDao()
    # Chama o metodo para deletar com ID
    dao.delete(id)
    # Feedback para o usuario
    flash(f'Produto removido com sucesso!', 'success')
    # Redirect para lista de produtos
    return redirect(url_for("produto_index"))

@app.route("/produto/search", methods=["POST"])
def produto_search():
    produto = request.form.get("busca")
    dao = ProdutoDao()
    produtos = dao.search(produto)
    return render_template("produto_list.html", produtos=produtos) 

# ==================================
# ROTAS (FAVORITOS)
# ==================================

# READ

@app.route("/favoritos", methods=["GET"])
def favoritos_index():
    # Cria o objeto da DAO
    dc = FavoritosDao()
    # Chama o método find all que retorna resultados já mapeados
    favoritos = dc.find_all()
    # Retorna a pagina favoritos.html junto com a lista favoritos
    return render_template("favoritos.html", favoritos=favoritos)

# CREATE

@app.route("/favoritos/add/<idp>", methods=["GET"])
def favoritos_add(idp):
    # Cria o objeto da DAO
    dao = FavoritosDao()
    # Cria um objeto da classe favorito com idcliente 1 e idp fornecido pelo request
    favorito = Favorito(1, idp)
    # Chama o metodo save, salvando o objeto da classe favorito
    dao.save(favorito)
    # Retorna um feedback para o usuario
    flash(f'Produto adicionado aos favoritos', 'success')
    # Redirect para produto_list.html
    return redirect(url_for("produto_index")) 

# DELETE

@app.route("/favoritos/del/<id>", methods=["GET"])
def favoritos_del(id):
    # Cria o objeto da DAO
    dao = FavoritosDao()
    # Chama o metodo delete com o id fornecido pelo request
    dao.delete(id)
    # Retorna um feedback para o usuario
    flash(f'Produto excluido dos favoritos', 'success')
    # Redirect para favoritos.html
    return redirect(url_for("favoritos_index"))

if __name__ == "__main__":
    app.run(debug=True)

    
