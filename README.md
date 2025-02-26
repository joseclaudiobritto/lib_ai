# Sistema de Recomendação de Livros com IA

Este projeto implementa um sistema de recomendação de livros baseado em IA, utilizando dados extraídos da biblioteca Biopark.

## Visão Geral do Projeto

O projeto é dividido em duas partes principais:

1. **Módulo de Webscraping** - Responsável pela coleta de dados dos livros da biblioteca
2. **Módulo de IA/Web** - Implementa um modelo de IA para recomendar livros com base nos dados coletados

## Estrutura do Projeto

```
lib_ai/
├── webscraping/        # Módulo de webscrapping de dados
│   ├── src/           # Código-fonte do webscrapping
│   ├── sql/           # Scripts SQL para o banco de dados
│   ├── README.md      # Documentação específica do módulo
│   └── ...
├── modelo/            # Módulo do modelo de IA (a ser implementado)
├── web/               # Interface web (a ser implementada)
└── README.md          # Esta documentação principal
```

## Módulo de Webscraping

O módulo de webscraping é responsável por:

- Coletar informações de livros do site da biblioteca Biopark
- Processar e limpar os dados coletados
- Armazenar os dados em um banco de dados PostgreSQL

Para mais detalhes sobre o funcionamento e uso deste módulo, consulte o [README do módulo de webscraping](webscraping/README.md).

## Módulo de IA/Web (Próximas Etapas)

Este módulo (a ser implementado) será responsável por:

- Realizar o fine-tuning de um modelo de IA usando os dados coletados
- Implementar algoritmos de recomendação personalizados
- Fornecer uma interface web para interação com o sistema

## Requisitos Gerais

- Python 3.8+
- Docker e Docker Compose (para implantação)
- PostgreSQL (para armazenamento de dados)
- Firefox (para o módulo de webscraping)

## Início Rápido

1. Clone o repositório
2. Para executar o webscrapping dos dados:
   ```bash
   cd webscraping
   ./run.sh
   ```
3. Consulte o README específico de cada módulo para instruções detalhadas

## Segurança e Configuração

Dados sensíveis (credenciais, URLs, etc.) são mantidos em:
- Variáveis de ambiente
- Arquivos de configuração locais (`.env`)
- Estes arquivos não são versionados (incluídos no `.gitignore`)

Para configurar o ambiente, crie um arquivo `.env` baseado nos arquivos `.env.example` fornecidos.

## Contribuição

Este projeto está em desenvolvimento ativo. Para contribuir:
1. Crie um fork do repositório
2. Implemente suas alterações
3. Envie um pull request

## Licença

[MIT](LICENSE)
