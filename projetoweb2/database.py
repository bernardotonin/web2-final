"""
Classe utilitária para 
ajudar na inicilização do 
banco de dados
"""
import sqlite3
import csv
class Database:

    @staticmethod
    def create_db():
        """ criar as tabela """
        conn = sqlite3.connect('banco.db')
        print('Criando banco de dados...')
        with open('schema.sql') as f:
            # executa o create table, insert, ...
            conn.executescript(f.read())
        conn.commit()
        conn.close()

    @staticmethod
    def get_connection():
        """ obter uma conexao com o BD """
        conn = sqlite3.connect('banco.db')
        return conn
        
    @staticmethod
    def import_csv():
        conn = sqlite3.connect('banco.db')
        with open('produtos.csv') as file:
            arquivo = csv.reader(file, delimiter=',')
            for linha in arquivo:
                conn.execute(f"""INSERT INTO produto(nome, categoria, preco) VALUES (?, ?, ?)""",
                (linha[1], linha[2], linha[3]))
                conn.commit()
        conn.close()
