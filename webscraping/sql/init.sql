CREATE TABLE IF NOT EXISTS livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    subtitulo TEXT,
    isbn VARCHAR(50),
    cdd VARCHAR(50),
    localizacao VARCHAR(100),
    autor VARCHAR(255),
    local_publicacao VARCHAR(100),
    editora VARCHAR(255),
    ano VARCHAR(50),
    descricao TEXT,
    assuntos TEXT,
    resumo TEXT,
    url VARCHAR(255),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_livros_titulo ON livros(titulo);
CREATE INDEX IF NOT EXISTS idx_livros_autor ON livros(autor);
CREATE INDEX IF NOT EXISTS idx_livros_isbn ON livros(isbn);

CREATE OR REPLACE VIEW vw_livros_basico AS
SELECT id, titulo, autor, editora, ano, resumo, assuntos 
FROM livros;
