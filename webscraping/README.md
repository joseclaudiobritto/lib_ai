# Webscrapping de Dados da Biblioteca

Este módulo realiza a busca de dados de livros do website da biblioteca e armazena os dados em um banco de dados PostgreSQL.

## Funcionalidades

- Acessa o site da biblioteca em modo headless
- Realiza a busca automática para obter todas as listagens de livros
- Extrai informações detalhadas para cada livro, incluindo:
  - Título e subtítulo
  - ISBN
  - Classificação CDD
  - Localização
  - Autor
  - Detalhes de publicação
  - Assuntos
  - Resumo completo de cada livro
- Salva os dados no banco de dados PostgreSQL

## Requisitos

### Para Desenvolvimento Local
- Python 3.8+
- Navegador Firefox instalado
- Pacotes Python necessários (listados em requirements.txt)
- PostgreSQL (opcional para desenvolvimento local)

### Para Implantação com Docker
- Docker
- Docker Compose

## Instalação

### Desenvolvimento Local
1. Clone ou baixe este repositório
2. Instale os pacotes necessários:

```bash
cd webscraping
pip install -r requirements.txt
```

3. Crie um arquivo `.env` baseado no `.env.example` com suas configurações

```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

4. Certifique-se de que o Chrome está instalado em seu sistema

### Implantação com Docker
1. Clone ou baixe este repositório
2. Navegue até a pasta do webscraping e crie um arquivo .env:

```bash
cd webscraping
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

3. Construa e execute usando Docker Compose:

```bash
./run.sh
```

ou

```bash
docker-compose up -d
```

Isso irá:
- Criar um contêiner com banco de dados PostgreSQL
- Construir e executar o contêiner do webscrapping
- Armazenar os dados no banco de dados e em arquivos de saída

## Uso

### Execução Local
Execute o script:

```bash
cd src
python main.py
```

O script continuará obtendo páginas de livros até não encontrar mais resultados, o que garante uma coleta completa do acervo disponível online.

### Execução com Docker
O ambiente Docker executará automaticamente o webscrapping quando iniciado. Para acionar manualmente uma nova execução:

```bash
docker-compose restart webscrapping
```

## Configuração do Banco de Dados

O banco de dados PostgreSQL pode ser acessado com:
- Host: localhost (ou seu host Docker)
- Porta: 5437
- Usuário: biopark
- Senha: biopark123
- Banco de dados: biblioteca_db

Esses valores podem ser alterados no arquivo `.env`.

## Saída

O script gera:
1. Registros no banco de dados na tabela `livros`

## Esquema do Banco de Dados

O banco de dados inclui:
- Tabela `livros` com colunas para todos os atributos dos livros
- Índices para pesquisa otimizada
- Uma view (`vw_livros_basico`) para consultas simplificadas

## Personalização

- Para modificar o tempo de espera entre requisições, ajuste a variável `TEMPO_ESPERA` no arquivo .env
- Para modificar o tempo de espera ao obter resumos, ajuste a variável `TEMPO_ESPERA_RESUMO` no arquivo .env
- Para alterar o número máximo de tentativas ao obter resumos, ajuste a variável `MAX_TENTATIVAS` no arquivo .env
- Para modificar as configurações de conexão do banco de dados, atualize as variáveis correspondentes no arquivo .env
- Para extrair informações adicionais, atualize a função `extrair_info` e adicione novos campos ao dicionário `dados_livro`

## Resolução de Problemas

- Se encontrar problemas com o driver do navegador, certifique-se de que está usando a versão mais recente do Chrome
- Para problemas de conexão com o banco de dados, verifique se o contêiner PostgreSQL está em execução com `docker-compose ps`
- Visualize logs com `docker-compose logs webscrapping` ou `docker-compose logs postgres`
