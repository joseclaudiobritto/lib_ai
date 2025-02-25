#!/usr/bin/env python3
import os
import sys
import psycopg2
from sqlalchemy import create_engine, text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def testar_conexao():
    print("Testando conexão com o banco de dados PostgreSQL...")
    
    print(f"Parâmetros de conexão:")
    print(f"  Host: {DB_HOST}")
    print(f"  Porta: {DB_PORT}")
    print(f"  Usuário: {DB_USER}")
    print(f"  Banco de dados: {DB_NAME}")
    
    try:
        print("\nTestando conexão com psycopg2...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        versao_db = cursor.fetchone()
        print(f"Conectado com sucesso ao PostgreSQL!")
        print(f"Versão do PostgreSQL: {versao_db[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM livros;")
        contagem_livros = cursor.fetchone()[0]
        print(f"Livros no banco de dados: {contagem_livros}")
        
        cursor.close()
        conn.close()
        print("Conexão fechada com sucesso.")
        
    except Exception as e:
        print(f"Erro na conexão psycopg2: {e}")
        
    try:
        print("\nTestando conexão com SQLAlchemy...")
        conn_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(conn_string)
        
        with engine.connect() as connection:
            resultado = connection.execute(text("SELECT version();"))
            versao = resultado.scalar()
            print(f"Conectado com sucesso via SQLAlchemy!")
            print(f"Versão do PostgreSQL: {versao}")
            
            resultado = connection.execute(text("SELECT COUNT(*) FROM livros;"))
            contagem = resultado.scalar()
            print(f"Livros no banco de dados: {contagem}")
            
            if contagem > 0:
                resultado = connection.execute(text("SELECT titulo, autor FROM livros LIMIT 1;"))
                amostra = resultado.fetchone()
                print(f"Livro de exemplo: '{amostra[0]}' por {amostra[1]}")
                
        print("Conexão SQLAlchemy fechada com sucesso.")
        
    except Exception as e:
        print(f"Erro na conexão SQLAlchemy: {e}")

if __name__ == "__main__":
    testar_conexao()
