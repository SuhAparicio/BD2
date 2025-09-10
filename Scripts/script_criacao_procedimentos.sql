/******************************/
/*         CATEGORIAS         */
/******************************/

-- Procedimento para inserir uma nova categoria
CREATE OR REPLACE PROCEDURE inserir_categoria(
    nome_param VARCHAR,
    descricao_param TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o nome não é nulo ou vazio
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da categoria não pode ser nulo ou vazio.';
    END IF;

    -- Inserir a categoria na tabela
    INSERT INTO Categorias (nome, descricao)
    VALUES (nome_param, descricao_param);
END;
$$;

-- Procedimento para atualizar uma categoria existente
CREATE OR REPLACE PROCEDURE atualizar_categoria(
    id_param INT,
    nome_param VARCHAR,
    descricao_param TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a categoria existe
    IF NOT EXISTS (SELECT 1 FROM Categorias WHERE id_categoria = id_param) THEN
        RAISE EXCEPTION 'Categoria com ID % não encontrada.', id_param;
    END IF;

    -- Validação: Verificar se o nome não é nulo ou vazio
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da categoria não pode ser nulo ou vazio.';
    END IF;

    -- Atualizar os dados da categoria
    UPDATE Categorias
    SET nome = nome_param,
        descricao = descricao_param
    WHERE id_categoria = id_param;
END;
$$;

-- Procedimento para eliminar uma categoria
CREATE OR REPLACE PROCEDURE eliminar_categoria(id_param INT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a categoria existe
    IF NOT EXISTS (SELECT 1 FROM Categorias WHERE id_categoria = id_param) THEN
        RAISE EXCEPTION 'Categoria com ID % não encontrada.', id_param;
    END IF;

    -- Verificar se a categoria está associada a livros
    IF EXISTS (SELECT 1 FROM Livros WHERE id_categoria = id_param) THEN
        RAISE EXCEPTION 'Não é possível eliminar a categoria com ID % porque ela está associada a livros.', id_param;
    END IF;

    -- Excluir a categoria
    DELETE FROM Categorias WHERE id_categoria = id_param;
END;
$$;

/******************************/
/*          EDITORAS          */
/******************************/

-- Procedimento para inserir uma nova editora
CREATE OR REPLACE PROCEDURE inserir_editora(
    nome_param VARCHAR,
    localizacao_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o nome não é nulo ou vazio
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da editora não pode ser nulo ou vazio.';
    END IF;

    -- Inserir a editora na tabela
    INSERT INTO Editoras (nome, localizacao)
    VALUES (nome_param, localizacao_param);
END;
$$;

-- Procedimento para atualizar uma editora existente
CREATE OR REPLACE PROCEDURE atualizar_editora(
    id_param INT,
    nome_param VARCHAR,
    localizacao_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a editora existe
    IF NOT EXISTS (SELECT 1 FROM Editoras WHERE id_editora = id_param) THEN
        RAISE EXCEPTION 'Editora com ID % não encontrada.', id_param;
    END IF;

    -- Validação: Verificar se o nome não é nulo ou vazio
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da editora não pode ser nulo ou vazio.';
    END IF;

    -- Atualizar os dados da editora
    UPDATE Editoras
    SET nome = nome_param,
        localizacao = localizacao_param
    WHERE id_editora = id_param;
END;
$$;

-- Procedimento para eliminar uma editora
CREATE OR REPLACE PROCEDURE eliminar_editora(id_param INT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a editora existe
    IF NOT EXISTS (SELECT 1 FROM Editoras WHERE id_editora = id_param) THEN
        RAISE EXCEPTION 'Editora com ID % não encontrada.', id_param;
    END IF;

    -- Verificar se a editora está associada a livros
    IF EXISTS (SELECT 1 FROM Livros WHERE id_editora = id_param) THEN
        RAISE EXCEPTION 'Não é possível eliminar a editora com ID % porque ela está associada a livros.', id_param;
    END IF;

    -- Excluir a editora
    DELETE FROM Editoras WHERE id_editora = id_param;
END;
$$;

/*****************************/
/*          AUTORES          */
/*****************************/

-- Procedimento para inserir um novo autor
CREATE OR REPLACE PROCEDURE inserir_autor(
    nome_param VARCHAR,
    data_nascimento_param DATE,
    nacionalidade_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o nome não é nulo ou vazio
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome do autor não pode ser nulo ou vazio.';
    END IF;

    -- Inserir o autor na tabela
    INSERT INTO Autores (nome, data_nascimento, nacionalidade)
    VALUES (nome_param, data_nascimento_param, nacionalidade_param);
END;
$$;

-- Procedimento para atualizar um autor existente
CREATE OR REPLACE PROCEDURE atualizar_autor(
    id_param INT,
    nome_param VARCHAR,
    data_nascimento_param DATE,
    nacionalidade_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o autor existe
    IF NOT EXISTS (SELECT 1 FROM Autores WHERE id_autor = id_param) THEN
        RAISE EXCEPTION 'Autor com ID % não encontrado.', id_param;
    END IF;

    -- Validação: Verificar se o nome não é nulo ou vazio
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome do autor não pode ser nulo ou vazio.';
    END IF;

    -- Atualizar os dados do autor
    UPDATE Autores
    SET nome = nome_param,
        data_nascimento = data_nascimento_param,
        nacionalidade = nacionalidade_param
    WHERE id_autor = id_param;
END;
$$;

-- Procedimento para eliminar um autor
CREATE OR REPLACE PROCEDURE eliminar_autor(id_param INT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o autor existe
    IF NOT EXISTS (SELECT 1 FROM Autores WHERE id_autor = id_param) THEN
        RAISE EXCEPTION 'Autor com ID % não encontrado.', id_param;
    END IF;

    -- Verificar se o autor está associado a livros
    IF EXISTS (SELECT 1 FROM Livros WHERE id_autor = id_param) THEN
        RAISE EXCEPTION 'Não é possível eliminar o autor com ID % porque ele está associado a livros.', id_param;
    END IF;

    -- Excluir o autor
    DELETE FROM Autores WHERE id_autor = id_param;
END;
$$;

/*****************************/
/*           LIVROS          */
/*****************************/

-- Função para o trigger que verifica empréstimos e reservas antes de excluir um livro
CREATE OR REPLACE FUNCTION verificar_exclusao_livro()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o livro está associado a empréstimos ativos
    IF EXISTS (
        SELECT 1 
        FROM Emprestimos 
        WHERE id_livro = OLD.id_livro 
        AND estado IN ('Emprestado', 'Atrasado')
        AND data_devolucao_real IS NULL
    ) THEN
        RAISE EXCEPTION 'Não é possível eliminar o livro com ID % porque ele está associado a empréstimos ativos.', OLD.id_livro;
    END IF;

    -- Validação: Verificar se o livro está associado a reservas ativas ou pendentes não expiradas
    IF EXISTS (
        SELECT 1 
        FROM Reservas 
        WHERE id_livro = OLD.id_livro 
        AND estado IN ('Pendente', 'Ativa')
    ) THEN
        RAISE EXCEPTION 'Não é possível eliminar o livro com ID % porque ele está associado a reservas ativas ou pendentes.', OLD.id_livro;
    END IF;

    RETURN OLD;
END;
$$;

-- Trigger que executa a função antes de excluir um livro
CREATE OR REPLACE TRIGGER trigger_verificar_exclusao_livro
BEFORE DELETE ON Livros
FOR EACH ROW
EXECUTE FUNCTION verificar_exclusao_livro();

-- Procedimento para inserir um novo livro
CREATE OR REPLACE PROCEDURE inserir_livro(
    titulo_param VARCHAR,
    isbn_param VARCHAR,
    ano_publicacao_param INTEGER,
    id_categoria_param INTEGER,
    id_autor_param INTEGER,
    id_editora_param INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o título não é nulo ou vazio
    IF titulo_param IS NULL OR TRIM(titulo_param) = '' THEN
        RAISE EXCEPTION 'O título do livro não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se o ISBN não é nulo ou vazio
    IF isbn_param IS NULL OR TRIM(isbn_param) = '' THEN
        RAISE EXCEPTION 'O ISBN do livro não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se o ISBN é único
    IF EXISTS (SELECT 1 FROM Livros WHERE isbn = isbn_param) THEN
        RAISE EXCEPTION 'O ISBN % já está registrado.', isbn_param;
    END IF;

    -- Validação: Verificar se a categoria existe (se fornecida)
    IF id_categoria_param IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Categorias WHERE id_categoria = id_categoria_param) THEN
        RAISE EXCEPTION 'Categoria com ID % não encontrada.', id_categoria_param;
    END IF;

    -- Validação: Verificar se o autor existe (se fornecido)
    IF id_autor_param IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Autores WHERE id_autor = id_autor_param) THEN
        RAISE EXCEPTION 'Autor com ID % não encontrado.', id_autor_param;
    END IF;

    -- Validação: Verificar se a editora existe (se fornecida)
    IF id_editora_param IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Editoras WHERE id_editora = id_editora_param) THEN
        RAISE EXCEPTION 'Editora com ID % não encontrada.', id_editora_param;
    END IF;

    -- Validação: Verificar se o ano de publicação é razoável (ex.: entre 0 e o ano atual)
    IF ano_publicacao_param IS NOT NULL AND (ano_publicacao_param < 0 OR ano_publicacao_param > EXTRACT(YEAR FROM CURRENT_DATE)) THEN
        RAISE EXCEPTION 'Ano de publicação % inválido.', ano_publicacao_param;
    END IF;

    -- Inserir o livro na tabela
    INSERT INTO Livros (titulo, isbn, ano_publicacao, id_categoria, id_autor, id_editora)
    VALUES (titulo_param, isbn_param, ano_publicacao_param, id_categoria_param, id_autor_param, id_editora_param);
END;
$$;

-- Procedimento para atualizar um livro existente
CREATE OR REPLACE PROCEDURE atualizar_livro(
    id_param INT,
    titulo_param VARCHAR,
    isbn_param VARCHAR,
    ano_publicacao_param INTEGER,
    id_categoria_param INTEGER,
    id_autor_param INTEGER,
    id_editora_param INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_param;
    END IF;

    -- Validação: Verificar se o título não é nulo ou vazio
    IF titulo_param IS NULL OR TRIM(titulo_param) = '' THEN
        RAISE EXCEPTION 'O título do livro não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se o ISBN não é nulo ou vazio
    IF isbn_param IS NULL OR TRIM(isbn_param) = '' THEN
        RAISE EXCEPTION 'O ISBN do livro não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se o ISBN é único (ignorando o próprio livro)
    IF EXISTS (SELECT 1 FROM Livros WHERE isbn = isbn_param AND id_livro != id_param) THEN
        RAISE EXCEPTION 'O ISBN % já está registrado para outro livro.', isbn_param;
    END IF;

    -- Validação: Verificar se a categoria existe (se fornecida)
    IF id_categoria_param IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Categorias WHERE id_categoria = id_categoria_param) THEN
        RAISE EXCEPTION 'Categoria com ID % não encontrada.', id_categoria_param;
    END IF;

    -- Validação: Verificar se o autor existe (se fornecido)
    IF id_autor_param IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Autores WHERE id_autor = id_autor_param) THEN
        RAISE EXCEPTION 'Autor com ID % não encontrado.', id_autor_param;
    END IF;

    -- Validação: Verificar se a editora existe (se fornecida)
    IF id_editora_param IS NOT NULL AND NOT EXISTS (SELECT 1 FROM Editoras WHERE id_editora = id_editora_param) THEN
        RAISE EXCEPTION 'Editora com ID % não encontrada.', id_editora_param;
    END IF;

    -- Validação: Verificar se o ano de publicação é razoável (se fornecido)
    IF ano_publicacao_param IS NOT NULL AND (ano_publicacao_param < 0 OR ano_publicacao_param > EXTRACT(YEAR FROM CURRENT_DATE)) THEN
        RAISE EXCEPTION 'Ano de publicação % inválido.', ano_publicacao_param;
    END IF;

    -- Atualizar os dados do livro
    UPDATE Livros
    SET titulo = titulo_param,
        isbn = isbn_param,
        ano_publicacao = ano_publicacao_param,
        id_categoria = id_categoria_param,
        id_autor = id_autor_param,
        id_editora = id_editora_param
    WHERE id_livro = id_param;
END;
$$;

-- Procedimento simplificado para eliminar um livro
CREATE OR REPLACE PROCEDURE eliminar_livro(id_param INT)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_param;
    END IF;

    -- Excluir o livro (o trigger verificará empréstimos e reservas)
    DELETE FROM Livros WHERE id_livro = id_param;
END;
$$;