import time
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

def configurar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def obter_conexao_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        return None

def criar_engine_sqlalchemy():
    conn_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_string)

def obter_livros():
    driver = configurar_driver()
    try:
        print("Acessando o site da biblioteca...")
        driver.get(BIBLIOTECA_URL)
        time.sleep(TEMPO_ESPERA)
        
        print("Realizando busca...")
        botao_busca = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")
        botao_busca.click()
        time.sleep(TEMPO_ESPERA)
        
        todos_livros = []
        pagina = 1
        sem_livros = False
        
        while not sem_livros:
            print(f"Obtendo página {pagina}...")
            
            url_pagina = f"{BIBLIOTECA_URL.rstrip('/')}/../acervo/{pagina}"
            driver.get(url_pagina)
            time.sleep(TEMPO_ESPERA)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            elementos_livro = soup.find_all("div", class_="media")
            
            if not elementos_livro:
                print(f"Nenhum livro encontrado na página {pagina}. Finalizando a busca.")
                sem_livros = True
                break
                
            mensagem_erro = soup.find("div", class_="alert-danger")
            if mensagem_erro or "Não foi possível localizar" in driver.page_source:
                print(f"Página {pagina} indica fim dos resultados. Finalizando a busca.")
                sem_livros = True
                break
            
            for livro in elementos_livro:
                try:
                    elemento_titulo = livro.find("h4", class_="media-heading")
                    link_titulo = elemento_titulo.find("a")
                    titulo = link_titulo.text.strip() if link_titulo else "N/A"
                    
                    url_livro = link_titulo.get("href") if link_titulo else "N/A"
                    if url_livro and not url_livro.startswith("http"):
                        base_url = "/".join(BIBLIOTECA_URL.split("/")[:-2])
                        url_livro = f"{base_url}{url_livro}"
                    
                    elemento_subtitulo = elemento_titulo.find("small")
                    subtitulo = elemento_subtitulo.text.strip() if elemento_subtitulo else ""
                    
                    elemento_info = livro.find("p")
                    texto_info = elemento_info.get_text("\n") if elemento_info else ""
                    
                    isbn = extrair_info(texto_info, "ISBN:")
                    cdd = extrair_info(texto_info, "CDD:")
                    localizacao = extrair_info(texto_info, "Localização:")
                    autor = extrair_info(texto_info, "Autor:")
                    local_publicacao = extrair_info(texto_info, "Local de Publicação:")
                    editora = extrair_info(texto_info, "Editora:")
                    ano = extrair_info(texto_info, "Ano do Material:")
                    descricao = extrair_info(texto_info, "Descrição física:")
                    assuntos = extrair_info(texto_info, "Assuntos:")
                    
                    resumo = ""
                    if url_livro and url_livro != "N/A":
                        resumo = extrair_resumo(driver, url_livro)
                        
                    dados_livro = {
                        "titulo": titulo,
                        "subtitulo": subtitulo,
                        "isbn": isbn,
                        "cdd": cdd,
                        "localizacao": localizacao,
                        "autor": autor,
                        "local_publicacao": local_publicacao,
                        "editora": editora,
                        "ano": ano,
                        "descricao": descricao,
                        "assuntos": assuntos,
                        "url": url_livro,
                        "resumo": resumo
                    }
                    
                    todos_livros.append(dados_livro)
                except Exception as e:
                    print(f"Erro ao extrair informações do livro: {e}")
            
            print(f"Obtido {len(elementos_livro)} livros da página {pagina}")
            pagina += 1
                
        return todos_livros
    
    finally:
        driver.quit()

def extrair_info(texto, etiqueta):
    if etiqueta in texto:
        indice_inicio = texto.find(etiqueta) + len(etiqueta)
        indice_proxima_etiqueta = encontrar_indice_proxima_etiqueta(texto, indice_inicio)
        if indice_proxima_etiqueta > 0:
            return texto[indice_inicio:indice_proxima_etiqueta].strip()
        else:
            return texto[indice_inicio:].strip()
    return ""

def extrair_resumo(driver, url_livro):
    for tentativa in range(MAX_TENTATIVAS):
        try:
            print(f"Acessando URL do livro para extrair resumo: {url_livro} (tentativa {tentativa+1}/{MAX_TENTATIVAS})")
            
            tempo_espera_variavel = TEMPO_ESPERA_RESUMO + random.uniform(0, 1)
            driver.get(url_livro)
            time.sleep(tempo_espera_variavel)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            paragrafos = soup.find_all("p")
            for p in paragrafos:
                if p.find("strong") and "Resumo:" in p.text:
                    texto_completo = p.get_text().strip()
                    resumo = texto_completo.replace("Resumo:", "").strip()
                    print(f"Resumo encontrado (método 1): {resumo[:50]}...")
                    return resumo
                    
            divs = soup.find_all("div", class_="col-xs-12")
            for div in divs:
                if div.find("strong") and "Resumo:" in div.text:
                    texto_completo = div.get_text().strip()
                    resumo = texto_completo.replace("Resumo:", "").strip()
                    print(f"Resumo encontrado (método 2): {resumo[:50]}...")
                    return resumo
                    
            for elemento in soup.find_all(string=lambda text: text and "Resumo:" in text):
                parent = elemento.parent
                if parent:
                    texto_completo = parent.get_text().strip()
                    resumo = texto_completo.replace("Resumo:", "").strip()
                    print(f"Resumo encontrado (método 3): {resumo[:50]}...")
                    return resumo
                    
            if tentativa < MAX_TENTATIVAS - 1:
                print(f"Resumo não encontrado na tentativa {tentativa+1}, aguardando para tentar novamente...")
                time.sleep(TEMPO_ESPERA * 2)
            
        except (TimeoutException, WebDriverException) as e:
            print(f"Erro ao acessar URL para resumo (tentativa {tentativa+1}): {e}")
            if tentativa < MAX_TENTATIVAS - 1:
                print("Aguardando para tentar novamente...")
                time.sleep(TEMPO_ESPERA * 3)
        except Exception as e:
            print(f"Erro inesperado ao extrair resumo: {e}")
            break
            
    print(f"Não foi possível obter o resumo para: {url_livro} após {MAX_TENTATIVAS} tentativas")
    return ""

def encontrar_indice_proxima_etiqueta(texto, indice_inicio):
    etiquetas = ["ISBN:", "CDD:", "Localização:", "Autor:", "Título:", 
              "Local de Publicação:", "Editora:", "Ano do Material:", 
              "Descrição física:", "Assuntos:", "Referência Bibliográfica:"]
    
    proximo_indice = float('inf')
    for etiqueta in etiquetas:
        indice = texto.find(etiqueta, indice_inicio)
        if indice > 0 and indice < proximo_indice:
            proximo_indice = indice
    
    return proximo_indice if proximo_indice != float('inf') else -1

def salvar_no_banco(livros):
    if not livros:
        print("Sem livros para salvar no banco de dados")
        return
        
    try:
        df = pd.DataFrame(livros)
        
        engine = criar_engine_sqlalchemy()
        
        df.to_sql('livros', engine, if_exists='append', index=False)
        
        print(f"Salvos {len(livros)} livros no banco de dados")
        
        with engine.connect() as conn:
            resultado = conn.execute(text("SELECT COUNT(*) FROM livros"))
            contagem = resultado.scalar()
            print(f"Total de livros no banco de dados: {contagem}")
            
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")

if __name__ == "__main__":
    print("Obtendo dados web da biblioteca...")
    
    os.makedirs("output", exist_ok=True)
    
    livros = obter_livros()
    
    if livros:
        print(f"Obtidos com sucesso {len(livros)} livros")
        salvar_no_banco(livros)
    else:
        print("Nenhum livro foi obtido.")
