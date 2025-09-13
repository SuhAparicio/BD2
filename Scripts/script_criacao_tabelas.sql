-- Tabela Categorias: Armazena as categorias dos livros.
CREATE TABLE Categorias (
    id_categoria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- Tabela Autores: Armazena informações sobre os autores.
CREATE TABLE Autores (
    id_autor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    nacionalidade VARCHAR(50)
);

-- Tabela Editoras: Armazena informações sobre as editoras.
CREATE TABLE Editoras (
    id_editora SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    localizacao VARCHAR(100)
);

-- Tabela Livros: Armazena os livros, com referências a categorias, autores e editoras.
CREATE TABLE Livros (
    id_livro SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    stock INTEGER DEFAULT 1,
    ano_publicacao INTEGER NOT NULL,
    id_categoria INTEGER REFERENCES Categorias(id_categoria) ON DELETE SET NULL,
    id_autor INTEGER REFERENCES Autores(id_autor) ON DELETE SET NULL,
    id_editora INTEGER REFERENCES Editoras(id_editora) ON DELETE SET NULL
);

-- Tabela Requisicoes: Regista requisicoes, referenciando Livros e Utilizadores (ID como string do Mongo).
CREATE TABLE Requisicoes (
    id_requisicao SERIAL PRIMARY KEY,
    id_livro INTEGER REFERENCES Livros(id_livro) ON DELETE CASCADE,
    id_utilizador VARCHAR(24) NOT NULL,  -- Referência ao _id do Mongo como string
    data_requisicao DATE NOT NULL DEFAULT CURRENT_DATE,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao_real DATE,
    estado VARCHAR(50) DEFAULT 'Requisitado'  -- ex: 'Requisitado', 'Devolvido', 'Atrasado'
);

/*******************/
/*     INDICES     */
/*******************/

-- Índices para otimizar a função livro_mais_requisitado
CREATE INDEX idx_requisicoes_data_requisicao ON Requisicoes(data_requisicao);
CREATE INDEX idx_requisicoes_id_livro ON Requisicoes(id_livro);

-- Índice para otimizar verificações de requisições ativas em triggers e procedimentos
CREATE INDEX idx_requisicoes_id_livro_estado_devolucao ON Requisicoes(id_livro, estado, data_devolucao_real);

-- Índices para otimizar verificações de chaves estrangeiras em Livros
CREATE INDEX idx_livros_id_categoria ON Livros(id_categoria);
CREATE INDEX idx_livros_id_autor ON Livros(id_autor);
CREATE INDEX idx_livros_id_editora ON Livros(id_editora);
