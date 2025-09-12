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
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da categoria não pode ser vazio.';
    END IF;

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
DECLARE
    nome_atual VARCHAR;
BEGIN
    SELECT nome INTO nome_atual FROM Categorias WHERE id_categoria = id_param;

    IF nome_atual IS NULL THEN
        RAISE EXCEPTION 'A categoria "%" não foi encontrada.', nome_param;
    END IF;

    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da categoria não pode ser vazio.';
    END IF;

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
DECLARE
    nome_categoria VARCHAR;
BEGIN
    SELECT nome INTO nome_categoria FROM Categorias WHERE id_categoria = id_param;

    IF nome_categoria IS NULL THEN
        RAISE EXCEPTION 'A categoria "%" não foi encontrada.', nome_categoria;
    END IF;

    IF EXISTS (SELECT 1 FROM Livros WHERE id_categoria = id_param) THEN
        RAISE EXCEPTION 'Não é possível eliminar a categoria "%" porque ela está associada a livros.', nome_categoria;
    END IF;

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
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da editora não pode ser vazio.';
    END IF;

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
DECLARE
    nome_atual VARCHAR;
BEGIN
    SELECT nome INTO nome_atual FROM Editoras WHERE id_editora = id_param;

    IF nome_atual IS NULL THEN
        RAISE EXCEPTION 'A editora "%" não foi encontrada.', nome_param;
    END IF;

    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome da editora não pode ser vazio.';
    END IF;

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
DECLARE
    nome_editora VARCHAR;
BEGIN
    SELECT nome INTO nome_editora FROM Editoras WHERE id_editora = id_param;

    IF nome_editora IS NULL THEN
        RAISE EXCEPTION 'A editora "%" não foi encontrada.', nome_editora;
    END IF;

    IF EXISTS (SELECT 1 FROM Livros WHERE id_editora = id_param) THEN
        RAISE EXCEPTION 'Não é possível eliminar a editora "%" porque ela está associada a livros.', nome_editora;
    END IF;

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
    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome do autor não pode ser vazio.';
    END IF;

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
DECLARE
    nome_atual VARCHAR;
BEGIN
    SELECT nome INTO nome_atual FROM Autores WHERE id_autor = id_param;

    IF nome_atual IS NULL THEN
        RAISE EXCEPTION 'O autor "%" não foi encontrado.', nome_param;
    END IF;

    IF nome_param IS NULL OR TRIM(nome_param) = '' THEN
        RAISE EXCEPTION 'O nome do autor não pode ser vazio.';
    END IF;

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
DECLARE
    nome_autor VARCHAR;
BEGIN
    SELECT nome INTO nome_autor FROM Autores WHERE id_autor = id_param;

    IF nome_autor IS NULL THEN
        RAISE EXCEPTION 'O autor "%" não foi encontrado.', nome_autor;
    END IF;

    IF EXISTS (SELECT 1 FROM Livros WHERE id_autor = id_param) THEN
        RAISE EXCEPTION 'Não é possível eliminar o autor "%" porque ele está associado a livros.', nome_autor;
    END IF;

    DELETE FROM Autores WHERE id_autor = id_param;
END;
$$;

/*****************************/
/*           LIVROS          */
/*****************************/

-- Função para o trigger que verifica requisições antes de excluir um livro
CREATE OR REPLACE FUNCTION verificar_exclusao_livro()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM Requisicoes 
        WHERE id_livro = OLD.id_livro 
        AND estado IN ('Requisitado', 'Atrasado')
        AND data_devolucao_real IS NULL
    ) THEN
        RAISE EXCEPTION 'Não é possível eliminar o livro "%" porque ele está emprestado.', OLD.titulo;
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
    stock_param INTEGER,
    ano_publicacao_param INTEGER,
    id_categoria_param INTEGER,
    id_autor_param INTEGER,
    id_editora_param INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    nome_categoria VARCHAR;
    nome_autor VARCHAR;
    nome_editora VARCHAR;
BEGIN
    IF titulo_param IS NULL OR TRIM(titulo_param) = '' THEN
        RAISE EXCEPTION 'O título do livro não pode ser vazio.';
    END IF;

    IF isbn_param IS NULL OR TRIM(isbn_param) = '' THEN
        RAISE EXCEPTION 'O ISBN do livro não pode ser vazio.';
    END IF;

    IF EXISTS (SELECT 1 FROM Livros WHERE isbn = isbn_param) THEN
        RAISE EXCEPTION 'O ISBN "%" já está registrado para outro livro.', isbn_param;
    END IF;
    
    IF stock_param IS NULL OR stock_param < 0 THEN
        RAISE EXCEPTION 'O stock do livro "%" é inválido. Deve ser maior ou igual a 0.', titulo_param;
    END IF;
    
    IF ano_publicacao_param IS NULL OR ano_publicacao_param < 0 OR ano_publicacao_param > EXTRACT(YEAR FROM CURRENT_DATE) THEN
        RAISE EXCEPTION 'O ano de publicação do livro "%" é inválido.', titulo_param;
    END IF;

    IF id_categoria_param IS NOT NULL THEN
        SELECT nome INTO nome_categoria FROM Categorias WHERE id_categoria = id_categoria_param;
        IF nome_categoria IS NULL THEN
            RAISE EXCEPTION 'A categoria "%" não foi encontrada.', nome_categoria;
        END IF;
    END IF;

    IF id_autor_param IS NOT NULL THEN
        SELECT nome INTO nome_autor FROM Autores WHERE id_autor = id_autor_param;
        IF nome_autor IS NULL THEN
            RAISE EXCEPTION 'O autor "%" não foi encontrado.', nome_autor;
        END IF;
    END IF;

    IF id_editora_param IS NOT NULL THEN
        SELECT nome INTO nome_editora FROM Editoras WHERE id_editora = id_editora_param;
        IF nome_editora IS NULL THEN
            RAISE EXCEPTION 'A editora "%" não foi encontrada.', nome_editora;
        END IF;
    END IF;

    INSERT INTO Livros (titulo, isbn, ano_publicacao, id_categoria, id_autor, id_editora, stock)
    VALUES (titulo_param, isbn_param, ano_publicacao_param, id_categoria_param, id_autor_param, id_editora_param, stock_param);
END;
$$;

-- Procedimento para atualizar um livro existente
CREATE OR REPLACE PROCEDURE atualizar_livro(
    id_param INT,
    titulo_param VARCHAR,
    isbn_param VARCHAR,
    stock_param INTEGER,
    ano_publicacao_param INTEGER,
    id_categoria_param INTEGER,
    id_autor_param INTEGER,
    id_editora_param INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    titulo_atual VARCHAR;
    nome_categoria VARCHAR;
    nome_autor VARCHAR;
    nome_editora VARCHAR;
BEGIN
    SELECT titulo INTO titulo_atual FROM Livros WHERE id_livro = id_param;

    IF titulo_atual IS NULL THEN
        RAISE EXCEPTION 'O livro "%" não foi encontrado.', titulo_param;
    END IF;

    IF titulo_param IS NULL OR TRIM(titulo_param) = '' THEN
        RAISE EXCEPTION 'O título do livro não pode ser vazio.';
    END IF;

    IF isbn_param IS NULL OR TRIM(isbn_param) = '' THEN
        RAISE EXCEPTION 'O ISBN do livro não pode ser vazio.';
    END IF;

    IF EXISTS (SELECT 1 FROM Livros WHERE isbn = isbn_param AND id_livro != id_param) THEN
        RAISE EXCEPTION 'O ISBN "%" já está registrado para outro livro.', isbn_param;
    END IF;
    
    IF stock_param IS NULL OR stock_param < 0 THEN
        RAISE EXCEPTION 'O stock do livro "%" é inválido. Deve ser maior ou igual a 0.', titulo_param;
    END IF;

    IF ano_publicacao_param IS NULL OR ano_publicacao_param < 0 OR ano_publicacao_param > EXTRACT(YEAR FROM CURRENT_DATE) THEN
        RAISE EXCEPTION 'O ano de publicação do livro "%" é inválido.', titulo_param;
    END IF;

    IF id_categoria_param IS NOT NULL THEN
        SELECT nome INTO nome_categoria FROM Categorias WHERE id_categoria = id_categoria_param;
        IF nome_categoria IS NULL THEN
            RAISE EXCEPTION 'A categoria "%" não foi encontrada.', nome_categoria;
        END IF;
    END IF;

    IF id_autor_param IS NOT NULL THEN
        SELECT nome INTO nome_autor FROM Autores WHERE id_autor = id_autor_param;
        IF nome_autor IS NULL THEN
            RAISE EXCEPTION 'O autor "%" não foi encontrado.', nome_autor;
        END IF;
    END IF;

    IF id_editora_param IS NOT NULL THEN
        SELECT nome INTO nome_editora FROM Editoras WHERE id_editora = id_editora_param;
        IF nome_editora IS NULL THEN
            RAISE EXCEPTION 'A editora "%" não foi encontrada.', nome_editora;
        END IF;
    END IF;

    UPDATE Livros
    SET titulo = titulo_param,
        isbn = isbn_param,
        ano_publicacao = ano_publicacao_param,
        id_categoria = id_categoria_param,
        id_autor = id_autor_param,
        id_editora = id_editora_param,
        stock = stock_param
    WHERE id_livro = id_param;
END;
$$;

-- Procedimento para eliminar um livro
CREATE OR REPLACE PROCEDURE eliminar_livro(id_param INT)
LANGUAGE plpgsql
AS $$
DECLARE
    titulo_livro VARCHAR;
BEGIN
    SELECT titulo INTO titulo_livro FROM Livros WHERE id_livro = id_param;

    IF titulo_livro IS NULL THEN
        RAISE EXCEPTION 'O livro "%" não foi encontrado.', titulo_livro;
    END IF;

    DELETE FROM Livros WHERE id_livro = id_param;
END;
$$;

/******************************/
/*        REQUISIÇÕES         */
/******************************/

CREATE OR REPLACE FUNCTION filtrar_requisicoes(
    titulo_livro_param VARCHAR,
    id_utilizador_param VARCHAR,
    ativa_param BOOLEAN
)
RETURNS TABLE (
    id_requisicao INTEGER,
    titulo_livro VARCHAR,
    id_utilizador VARCHAR,
    data_requisicao DATE,
    data_devolucao_prevista DATE,
    data_devolucao_real DATE,
    estado VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id_requisicao,
        l.titulo AS titulo_livro,
        r.id_utilizador,
        r.data_requisicao,
        r.data_devolucao_prevista,
        r.data_devolucao_real,
        r.estado
    FROM Requisicoes r
    JOIN Livros l ON r.id_livro = l.id_livro
    WHERE 
        (titulo_livro_param IS NULL OR l.titulo ILIKE '%' || titulo_livro_param || '%')
        AND (id_utilizador_param IS NULL OR r.id_utilizador ILIKE '%' || id_utilizador_param || '%')
        AND (ativa_param IS NULL OR (
            (ativa_param = TRUE AND r.estado IN ('Requisitado', 'Atrasado') AND r.data_devolucao_real IS NULL)
            OR (ativa_param = FALSE AND r.estado = 'Devolvido')
        ))
    ORDER BY r.id_requisicao;
END;
$$;


-- Função para o trigger que verifica exclusão de requisições
CREATE OR REPLACE FUNCTION verificar_exclusao_requisicao()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF OLD.estado IN ('Requisitado', 'Atrasado') 
       AND OLD.data_devolucao_real IS NULL THEN
        RAISE EXCEPTION 'Não é possível eliminar esta requisição porque ela está ativa ou atrasada.';
    END IF;

    RETURN OLD;
END;
$$;

-- Trigger que executa a função antes de excluir uma requisição
CREATE OR REPLACE TRIGGER trigger_verificar_exclusao_requisicao
BEFORE DELETE ON Requisicoes
FOR EACH ROW
EXECUTE FUNCTION verificar_exclusao_requisicao();

-- Procedimento para inserir uma nova requisição (apenas id_livro, id_utilizador, data_devolucao_prevista)
CREATE OR REPLACE PROCEDURE inserir_requisicao(
    id_livro_param INTEGER,
    id_utilizador_param VARCHAR,
    data_devolucao_prevista_param DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    titulo_livro VARCHAR;
BEGIN
    SELECT titulo INTO titulo_livro FROM Livros WHERE id_livro = id_livro_param;

    IF titulo_livro IS NULL THEN
        RAISE EXCEPTION 'O livro "%" não foi encontrado.', titulo_livro;
    END IF;

    IF id_utilizador_param IS NULL OR TRIM(id_utilizador_param) = '' THEN
        RAISE EXCEPTION 'O ID do utilizador não pode ser vazio.';
    END IF;

    IF data_devolucao_prevista_param <= CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de devolução prevista do livro "%" deve ser futura.', titulo_livro;
    END IF;

    INSERT INTO Requisicoes (id_livro, id_utilizador, data_requisicao, data_devolucao_prevista, data_devolucao_real, estado)
    VALUES (
        id_livro_param,
        id_utilizador_param,
        CURRENT_DATE,
        data_devolucao_prevista_param,
        NULL,
        'Requisitado'
    );
END;
$$;

-- Procedimento para atualizar uma requisição existente (apenas id_livro, id_utilizador, data_devolucao_prevista)
CREATE OR REPLACE PROCEDURE atualizar_requisicao(
    id_param INTEGER,
    id_livro_param INTEGER,
    id_utilizador_param VARCHAR,
    data_devolucao_prevista_param DATE
)
LANGUAGE plpgsql
AS $$
DECLARE
    titulo_livro VARCHAR;
    estado_atual VARCHAR;
BEGIN
    -- Verificar se a requisição existe e obter o estado atual
    SELECT r.estado, l.titulo 
    INTO estado_atual, titulo_livro 
    FROM Requisicoes r
    JOIN Livros l ON r.id_livro = l.id_livro
    WHERE r.id_requisicao = id_param;

    IF estado_atual IS NULL THEN
        RAISE EXCEPTION 'Esta requisição não foi encontrada.';
    END IF;

    -- Impedir atualização se a requisição já foi devolvida
    IF estado_atual = 'Devolvido' THEN
        RAISE EXCEPTION 'Não é possível editar a requisição do livro "%" porque ela já foi devolvida.', titulo_livro;
    END IF;

    -- Verificar se o livro existe
    SELECT titulo INTO titulo_livro FROM Livros WHERE id_livro = id_livro_param;

    IF titulo_livro IS NULL THEN
        RAISE EXCEPTION 'O livro "%" não foi encontrado.', titulo_livro;
    END IF;

    IF id_utilizador_param IS NULL OR TRIM(id_utilizador_param) = '' THEN
        RAISE EXCEPTION 'O ID do utilizador não pode ser vazio.';
    END IF;

    IF data_devolucao_prevista_param <= CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de devolução prevista do livro "%" deve ser futura.', titulo_livro;
    END IF;

    UPDATE Requisicoes
    SET id_livro = id_livro_param,
        id_utilizador = id_utilizador_param,
        data_devolucao_prevista = data_devolucao_prevista_param
    WHERE id_requisicao = id_param;
END;
$$;

-- Procedimento para eliminar uma requisição
CREATE OR REPLACE PROCEDURE eliminar_requisicao(id_param INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Requisicoes WHERE id_requisicao = id_param) THEN
        RAISE EXCEPTION 'Esta requisição não foi encontrada.';
    END IF;

    DELETE FROM Requisicoes WHERE id_requisicao = id_param;
END;
$$;

-- Procedimento para marcar uma requisição como devolvida
CREATE OR REPLACE PROCEDURE marcar_requisicao_devolvida(id_param INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    titulo_livro VARCHAR;
    estado_atual VARCHAR;
BEGIN
    SELECT r.estado, l.titulo 
    INTO estado_atual, titulo_livro 
    FROM Requisicoes r
    JOIN Livros l ON r.id_livro = l.id_livro
    WHERE r.id_requisicao = id_param;

    IF estado_atual IS NULL THEN
        RAISE EXCEPTION 'Esta requisição não foi encontrada.';
    END IF;

    IF estado_atual = 'Devolvido' THEN
        RAISE EXCEPTION 'A requisição do livro "%" já foi devolvida.', titulo_livro;
    END IF;

    UPDATE Requisicoes
    SET data_devolucao_real = CURRENT_DATE,
        estado = 'Devolvido'
    WHERE id_requisicao = id_param;
END;
$$;

/******************************/
/*      STOCK REQUISIÇÃO      */
/******************************/

-- Função para o trigger que verifica o stock antes de inserir uma requisição
CREATE OR REPLACE FUNCTION verificar_stock_requisicao()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    stock_livro INTEGER;
    total_requisicoes_ativas INTEGER;
    titulo_livro VARCHAR;
BEGIN
    SELECT stock, titulo INTO stock_livro, titulo_livro
    FROM Livros
    WHERE id_livro = NEW.id_livro;

    IF stock_livro IS NULL THEN
        RAISE EXCEPTION 'O livro "%" não foi encontrado.', titulo_livro;
    END IF;

    SELECT COUNT(*) INTO total_requisicoes_ativas
    FROM Requisicoes
    WHERE id_livro = NEW.id_livro
      AND estado IN ('Requisitado', 'Atrasado')
      AND data_devolucao_real IS NULL;

    IF (total_requisicoes_ativas + 1) > stock_livro THEN
        RAISE EXCEPTION 'Não é possível requisitar o livro "%" porque não há exemplares disponíveis.', titulo_livro;
    END IF;

    RETURN NEW;
END;
$$;

-- Trigger que executa a função antes de inserir uma requisição
CREATE OR REPLACE TRIGGER trigger_verificar_stock_requisicao
BEFORE INSERT ON Requisicoes
FOR EACH ROW
EXECUTE FUNCTION verificar_stock_requisicao();

/******************************/
/*        ESTATÍSTICAS        */
/******************************/

CREATE OR REPLACE FUNCTION livro_mais_requisitado()
RETURNS TABLE (
    id_livro INTEGER,
    titulo VARCHAR,
    total_requisicoes BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id_livro,
        l.titulo,
        COUNT(*) AS total_requisicoes
    FROM Requisicoes r
    INNER JOIN Livros l ON r.id_livro = l.id_livro
    WHERE r.data_requisicao >= CURRENT_DATE - INTERVAL '30 days'
      AND r.data_requisicao <= CURRENT_DATE
    GROUP BY r.id_livro, l.titulo
    ORDER BY total_requisicoes DESC, r.id_livro ASC
    LIMIT 1;
END;
$$;

/******************************/
/*   LIVROS DISPONÍVEIS       */
/******************************/

CREATE OR REPLACE FUNCTION livros_disponiveis_requisicao()
RETURNS TABLE (
    id_livro INTEGER,
    titulo VARCHAR,
    stock INTEGER,
    exemplares_disponiveis BIGINT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        l.id_livro,
        l.titulo,
        l.stock,
        (l.stock - COALESCE((
            SELECT COUNT(*) 
            FROM Requisicoes r 
            WHERE r.id_livro = l.id_livro 
            AND r.estado IN ('Requisitado', 'Atrasado')
            AND r.data_devolucao_real IS NULL
        ), 0)) AS exemplares_disponiveis
    FROM Livros l
    WHERE l.stock > COALESCE((
        SELECT COUNT(*) 
        FROM Requisicoes r 
        WHERE r.id_livro = l.id_livro 
        AND r.estado IN ('Requisitado', 'Atrasado')
        AND r.data_devolucao_real IS NULL
    ), 0)
    ORDER BY l.id_livro;
END;
$$;

