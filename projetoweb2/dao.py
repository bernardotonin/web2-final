"""
Dao - Data access object
Implementa a conexao com o
banco de dados.

"""
from database import Database
from entidades import Cliente, Produto, Favorito

class ProdutoDao:

    # CREATE
    def save(self, produto):
        # Conexão com o DB
        conn = Database.get_connection()
        # Execução da query
        conn.execute(
            f"""INSERT INTO produto(nome, preco, marca) VALUES (?, ?, ?)""",
            (produto.nome, produto.preco, produto.marca)
        )
        # Commita alterações
        conn.commit()
        # Fecha conexão com DB
        conn.close()

    # READ
    def find_all(self):
        # 1. Obtem conexão com DB
        conn = Database.get_connection()
        # 2. Executa a Query
        res = conn.execute("""
        SELECT id, nome, preco, marca, added, categoria FROM produto
        """
        )
        # 3. Obtem resultados
        results = res.fetchall()
        # 4. Mapeia resultados
        results = [
            { 
                "id": produto[0], 
                "nome": produto[1],
                "preco": produto[2],
                "marca": produto[3],
                "added": produto[4],
                "categoria": produto[5],
            } for produto in results]
        # 5. Fecha conexão com DB
        conn.close()
        # 6. Retorna resultado da consulta já mapeado
        return results

    # UPDATE
    def update(self, produto):
        # 1. Obtem conexão com DB
        conn = Database.get_connection()
        # 2. Executa a Query
        conn.execute(f"""
        UPDATE produto SET nome = ?, preco = ?, marca = ? WHERE id = ?
        """, (produto.nome, produto.preco, produto.marca, produto.id))
        # 3. Commita alterações
        conn.commit()
        # 4. Fecha conexão com DB
        conn.close()

    # DELETE
    def delete(self, id):
        # 1. Obtem conexão com DB
        conn = Database.get_connection()
        # 2. Executa a Query
        conn.execute(f"""
            DELETE FROM produto WHERE id = {id}
        """)
        # 3. Commita alterações
        conn.commit()
        # 4. Fecha conexão com DB
        conn.close()
    
    # get_produto
    def find_one(self, id):
        # 1. Obtem conexão com DB
        conn = Database.get_connection()
        # 2. Executa a Query armazenando em uma variavel temporiaria
        temp = conn.execute(f"""SELECT id, nome, preco, marca, added FROM produto WHERE id = {id}""")
        # 3. Obtem 1 resultado
        row = temp.fetchone()
        # 4. Mapeia resultado
        produto = Produto( 
            row[1],
            row[2],
            row[3],
            row[0]
        )
        # 5. Fecha conexão
        conn.close()
        # 6. Retorna resultado
        return produto
    def search(self, nome):
        conn = Database.get_connection()
        temp = conn.execute(f"""SELECT id, nome, preco, marca, added  FROM produto WHERE nome LIKE '%{nome}%'""")
        results = temp.fetchall()
        results = [
            { 
                "id": produto[0], 
                "nome": produto[1],
                "preco": produto[2],
                "marca": produto[3],
                "added": produto[4],
            } for produto in results]        
        conn.close()
        return results
    

class ClienteDao:

    def save(self, cliente):
        """
        Realiza o INSERT na tabela cliente
        """
        # obtem uma conexao com o banco:
        conn = Database.get_connection()
        conn.execute(
            f"""
            INSERT INTO cliente (
                nome, cpf, cep, email            
            ) VALUES (?, ?, ?, ?)
            """,
            (
                cliente.nome,  
                cliente.cpf, 
                cliente.cep,
                cliente.email, 
            )
        )
        conn.commit()
        conn.close()


    def update(self, cliente):
        """
        Realiza UPDATE do cliente
        """
        conn = Database.get_connection()
        conn.execute(
            f"""
            UPDATE cliente SET nome = ?, cpf = ?, cep = ?, email = ?
            WHERE id = ?
            """,
            (
                cliente.nome,
                cliente.cpf,
                cliente.cep,
                cliente.email,
                cliente.id
            )
        )
        conn.commit()
        conn.close()

    def delete(self, id):
        """
        Remove um cliente de acordo com o id fornecido
        """
        conn = Database.get_connection()
        conn.execute(
            # Query
            # Hard Delete (cuidado!)
            f"""
            DELETE FROM cliente WHERE id = {id}
            """
        )
        conn.commit()
        conn.close()


    def find_all(self):
        conn = Database.get_connection()
        res = conn.execute("""
        SELECT id, nome, cpf, cep, email, data_cadastro FROM cliente
        """
        )
        # executa o SELECT
        results = res.fetchall()
        # results eh um vetor

        # versao 1
        results = [
            { 
                "id": cliente[0], 
                "nome": cliente[1],
                "cpf": cliente[2],
                "cep": cliente[3],
                "email": cliente[4],
                "data_cadastro": cliente[5],
            } for cliente in results]

        conn.close()
        return results


    def get_cliente(self, id):
        conn = Database.get_connection()
        res = conn.execute(f"""
        SELECT id, nome, email, cpf, cep, data_cadastro  FROM cliente WHERE id = {id}
        """
        )
        row = res.fetchone()
        
        # cria um objeto cliente para armazenar resultado do SELECT:
        cliente = Cliente( 
            row[1],
            row[2],
            id = row[0],
            cpf = row[3],
            cep = row[4],             
            data_cadastro = row[5]
        )
        conn.close()
        return cliente

class FavoritosDao:
    def save(self, favorito):
        conn = Database.get_connection()
        conn.execute(f"""INSERT INTO favoritos (cliente_id, produto_id) VALUES (?, ?)""", (favorito.idcliente,
        favorito.idproduto
        ))
        conn.commit()
        conn.close()
    def find_all(self):
        conn = Database.get_connection()
        res = conn.execute("""SELECT favoritos.id, favoritos.produto_id, produto.nome, produto.preco, produto.marca FROM favoritos 
        INNER JOIN produto WHERE favoritos.produto_id = produto.id""")
        results = res.fetchall()
        results = [
            { 
                "id": favorito[0], 
                "idproduto": favorito[1],
                "nomeproduto": favorito[2],
                "precoproduto": favorito[3],
                "marcaproduto": favorito[4]
            } for favorito in results]
        return results
    def delete(self, id):
        conn = Database.get_connection()
        conn.execute(f"""DELETE FROM favoritos WHERE id = {id}""")
        conn.commit()
        conn.close()

if __name__ == "__main__":
    pass