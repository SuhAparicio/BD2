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
    ano_publicacao INTEGER,
    id_categoria INTEGER REFERENCES Categorias(id_categoria) ON DELETE SET NULL,
    id_autor INTEGER REFERENCES Autores(id_autor) ON DELETE SET NULL,
    id_editora INTEGER REFERENCES Editoras(id_editora) ON DELETE SET NULL
);

-- Tabela Empréstimos: Regista empréstimos, referenciando Livros e Utilizadores (ID como string do Mongo).
CREATE TABLE Emprestimos (
    id_emprestimo SERIAL PRIMARY KEY,
    id_livro INTEGER REFERENCES Livros(id_livro) ON DELETE CASCADE,
    id_utilizador VARCHAR(24) NOT NULL,  -- Referência ao _id do Mongo como string
    data_emprestimo DATE NOT NULL DEFAULT CURRENT_DATE,
    data_devolucao_prevista DATE NOT NULL,
    data_devolucao_real DATE,
    estado VARCHAR(50) DEFAULT 'Emprestado'  -- ex: 'Emprestado', 'Devolvido', 'Atrasado'
);

-- Tabela Reservas: Regista reservas, referenciando Livros e Utilizadores (ID como string do Mongo).
CREATE TABLE Reservas (
    id_reserva SERIAL PRIMARY KEY,
    id_livro INTEGER REFERENCES Livros(id_livro) ON DELETE CASCADE,
    id_utilizador VARCHAR(24) NOT NULL,  -- Referência ao _id do Mongo como string
    data_reserva DATE NOT NULL DEFAULT CURRENT_DATE,
    data_expiracao DATE,
    estado VARCHAR(50) DEFAULT 'Pendente'  -- ex: 'Pendente', 'Ativa', 'Cancelada'
);