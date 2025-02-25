import os

BIBLIOTECA_URL = os.environ.get('BIBLIOTECA_URL', 'https://bioparkedu.jacad.com.br/academico/biblioteca/')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5437')
DB_USER = os.environ.get('DB_USER', 'biopark')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'biopark123')
DB_NAME = os.environ.get('DB_NAME', 'biblioteca_db')
TEMPO_ESPERA = int(os.environ.get('TEMPO_ESPERA', '2'))
TEMPO_ESPERA_RESUMO = int(os.environ.get('TEMPO_ESPERA_RESUMO', '3'))
MAX_TENTATIVAS = int(os.environ.get('MAX_TENTATIVAS', '3'))
