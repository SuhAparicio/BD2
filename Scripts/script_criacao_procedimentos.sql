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

-- Função para o trigger que verifica requisições e reservas antes de excluir um livro
CREATE OR REPLACE FUNCTION verificar_exclusao_livro()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o livro está associado a requisições ativas
    IF EXISTS (
        SELECT 1 
        FROM Requisicoes 
        WHERE id_livro = OLD.id_livro 
        AND estado IN ('Requisitado', 'Atrasado')
        AND data_devolucao_real IS NULL
    ) THEN
        RAISE EXCEPTION 'Não é possível eliminar o livro com ID % porque ele está associado a uma requisição ativa.', OLD.id_livro;
    END IF;

    -- Validação: Verificar se o livro está associado a reservas ativas ou pendentes não expiradas
    IF EXISTS (
        SELECT 1 
        FROM Reservas 
        WHERE id_livro = OLD.id_livro 
        AND estado IN ('Pendente', 'Ativa')
        AND (data_expiracao IS NULL OR data_expiracao >= CURRENT_DATE)
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
    id_editora_param INTEGER,
    stock_param INTEGER
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

    -- Validação: Verificar se o ano de publicação é válido
    IF ano_publicacao_param IS NULL OR ano_publicacao_param < 0 OR ano_publicacao_param > EXTRACT(YEAR FROM CURRENT_DATE) THEN
        RAISE EXCEPTION 'Ano de publicação % inválido.', ano_publicacao_param;
    END IF;

    -- Validação: Verificar se o stock é válido (não negativo)
    IF stock_param IS NULL OR stock_param < 0 THEN
        RAISE EXCEPTION 'O stock % é inválido. Deve ser maior ou igual a 0.', stock_param;
    END IF;

    -- Inserir o livro na tabela
    INSERT INTO Livros (titulo, isbn, ano_publicacao, id_categoria, id_autor, id_editora, stock)
    VALUES (titulo_param, isbn_param, ano_publicacao_param, id_categoria_param, id_autor_param, id_editora_param, stock_param);
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
    id_editora_param INTEGER,
    stock_param INTEGER
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

    -- Validação: Verificar se o ano de publicação é válido (se fornecido)
    IF ano_publicacao_param IS NULL OR ano_publicacao_param < 0 OR ano_publicacao_param > EXTRACT(YEAR FROM CURRENT_DATE) THEN
        RAISE EXCEPTION 'Ano de publicação % inválido.', ano_publicacao_param;
    END IF;

    -- Validação: Verificar se o stock é válido (não negativo)
    IF stock_param IS NULL OR stock_param < 0 THEN
        RAISE EXCEPTION 'O stock % é inválido. Deve ser maior ou igual a 0.', stock_param;
    END IF;

    -- Atualizar os dados do livro
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
BEGIN
    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_param;
    END IF;

    -- Validação: Verificar se o stock é zero
    IF (SELECT stock FROM Livros WHERE id_livro = id_param) > 0 THEN
        RAISE EXCEPTION 'Não é possível eliminar o livro com ID % porque ainda há exemplares em stock.', id_param;
    END IF;

    -- Excluir o livro (o trigger verificará requisições e reservas)
    DELETE FROM Livros WHERE id_livro = id_param;
END;
$$;

/******************************/
/*          RESERVAS          */
/******************************/

-- Função para o trigger que verifica exclusão de reservas
CREATE OR REPLACE FUNCTION verificar_exclusao_reserva()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Impedir exclusão de reservas ativas ou pendentes não expiradas
    IF OLD.estado IN ('Pendente', 'Ativa') 
       THEN RAISE EXCEPTION 'Não é possível eliminar a reserva com ID % porque ela está ativa ou pendente.', OLD.id_reserva;
    END IF;

    RETURN OLD;
END;
$$;

-- Trigger que executa a função antes de excluir uma reserva
CREATE OR REPLACE TRIGGER trigger_verificar_exclusao_reserva
BEFORE DELETE ON Reservas
FOR EACH ROW
EXECUTE FUNCTION verificar_exclusao_reserva();

-- Procedimento para inserir uma nova reserva
CREATE OR REPLACE PROCEDURE inserir_reserva(
    id_livro_param INTEGER,
    id_utilizador_param VARCHAR,
    data_reserva_param DATE,
    data_expiracao_param DATE,
    estado_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_livro_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_livro_param;
    END IF;

    -- Validação: Verificar se id_utilizador não é nulo ou vazio
    IF id_utilizador_param IS NULL OR TRIM(id_utilizador_param) = '' THEN
        RAISE EXCEPTION 'O ID do utilizador não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se data_expiracao é futura (se fornecida)
    IF data_expiracao_param IS NOT NULL AND data_expiracao_param <= CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de expiração deve ser futura.';
    END IF;

    -- Inserir a reserva na tabela
    INSERT INTO Reservas (id_livro, id_utilizador, data_reserva, data_expiracao, estado)
    VALUES (
        id_livro_param,
        id_utilizador_param,
        COALESCE(data_reserva_param, CURRENT_DATE),
        data_expiracao_param,
        COALESCE(estado_param, 'Pendente')
    );
END;
$$;

-- Procedimento para atualizar uma reserva existente
CREATE OR REPLACE PROCEDURE atualizar_reserva(
    id_param INTEGER,
    id_livro_param INTEGER,
    id_utilizador_param VARCHAR,
    data_reserva_param DATE,
    data_expiracao_param DATE,
    estado_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a reserva existe
    IF NOT EXISTS (SELECT 1 FROM Reservas WHERE id_reserva = id_param) THEN
        RAISE EXCEPTION 'Reserva com ID % não encontrada.', id_param;
    END IF;

    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_livro_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_livro_param;
    END IF;

    -- Validação: Verificar se id_utilizador não é nulo ou vazio
    IF id_utilizador_param IS NULL OR TRIM(id_utilizador_param) = '' THEN
        RAISE EXCEPTION 'O ID do utilizador não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se data_expiracao é futura (se fornecida)
    IF data_expiracao_param IS NOT NULL AND data_expiracao_param <= CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de expiração deve ser futura.';
    END IF;

    -- Validação: Verificar se o estado é válido
    IF estado_param IS NOT NULL AND estado_param NOT IN ('Pendente', 'Ativa', 'Cancelada') THEN
        RAISE EXCEPTION 'Estado inválido: %. Deve ser Pendente, Ativa ou Cancelada.', estado_param;
    END IF;

    -- Atualizar os dados da reserva
    UPDATE Reservas
    SET id_livro = id_livro_param,
        id_utilizador = id_utilizador_param,
        data_reserva = COALESCE(data_reserva_param, data_reserva),
        data_expiracao = data_expiracao_param,
        estado = COALESCE(estado_param, estado)
    WHERE id_reserva = id_param;
END;
$$;

-- Procedimento simplificado para eliminar uma reserva
CREATE OR REPLACE PROCEDURE eliminar_reserva(id_param INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a reserva existe
    IF NOT EXISTS (SELECT 1 FROM Reservas WHERE id_reserva = id_param) THEN
        RAISE EXCEPTION 'Reserva com ID % não encontrada.', id_param;
    END IF;

    -- Excluir a reserva (o trigger verificará restrições)
    DELETE FROM Reservas WHERE id_reserva = id_param;
END;
$$;

/******************************/
/*        REQUISIÇOES         */
/******************************/

-- Função para o trigger que verifica exclusão de requisições
CREATE OR REPLACE FUNCTION verificar_exclusao_requisicao()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Impedir exclusão de requisições ativas ou atrasadas não devolvidas
    IF OLD.estado IN ('Requisitado', 'Atrasado') 
       AND OLD.data_devolucao_real IS NULL THEN
        RAISE EXCEPTION 'Não é possível eliminar a requisição com ID % porque ela está ativa ou atrasada.', OLD.id_requisicao;
    END IF;

    RETURN OLD;
END;
$$;

-- Trigger que executa a função antes de excluir uma requisição
CREATE OR REPLACE TRIGGER trigger_verificar_exclusao_requisicao
BEFORE DELETE ON Requisicoes
FOR EACH ROW
EXECUTE FUNCTION verificar_exclusao_requisicao();

-- Procedimento para inserir uma nova requisição
CREATE OR REPLACE PROCEDURE inserir_requisicao(
    id_livro_param INTEGER,
    id_utilizador_param VARCHAR,
    data_requisicao_param DATE,
    data_devolucao_prevista_param DATE,
    data_devolucao_real_param DATE,
    estado_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_livro_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_livro_param;
    END IF;

    -- Validação: Verificar se id_utilizador não é nulo ou vazio
    IF id_utilizador_param IS NULL OR TRIM(id_utilizador_param) = '' THEN
        RAISE EXCEPTION 'O ID do utilizador não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se data_requisicao não é futura
    IF data_requisicao_param IS NOT NULL AND data_requisicao_param > CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de requisição não pode ser futura.';
    END IF;

    -- Validação: Verificar se data_devolucao_prevista é futura
    IF data_devolucao_prevista_param <= CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de devolução prevista deve ser futura.';
    END IF;

    -- Validação: Verificar se data_devolucao_real é válida
    IF data_devolucao_real_param IS NOT NULL AND data_devolucao_real_param < data_requisicao_param THEN
        RAISE EXCEPTION 'A data de devolução real não pode ser anterior à data de requisição.';
    END IF;

    -- Validação: Verificar se o estado é válido
    IF estado_param IS NOT NULL AND estado_param NOT IN ('Requisitado', 'Devolvido', 'Atrasado') THEN
        RAISE EXCEPTION 'Estado inválido: %. Deve ser Requisitado, Devolvido ou Atrasado.', estado_param;
    END IF;

    -- Inserir a requisição na tabela
    INSERT INTO Requisicoes (id_livro, id_utilizador, data_requisicao, data_devolucao_prevista, data_devolucao_real, estado)
    VALUES (
        id_livro_param,
        id_utilizador_param,
        COALESCE(data_requisicao_param, CURRENT_DATE),
        data_devolucao_prevista_param,
        data_devolucao_real_param,
        COALESCE(estado_param, 'Requisitado')
    );
END;
$$;

-- Procedimento para atualizar uma requisição existente
CREATE OR REPLACE PROCEDURE atualizar_requisicao(
    id_param INTEGER,
    id_livro_param INTEGER,
    id_utilizador_param VARCHAR,
    data_requisicao_param DATE,
    data_devolucao_prevista_param DATE,
    data_devolucao_real_param DATE,
    estado_param VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a requisição existe
    IF NOT EXISTS (SELECT 1 FROM Requisicoes WHERE id_requisicao = id_param) THEN
        RAISE EXCEPTION 'Requisição com ID % não encontrada.', id_param;
    END IF;

    -- Validação: Verificar se o livro existe
    IF NOT EXISTS (SELECT 1 FROM Livros WHERE id_livro = id_livro_param) THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', id_livro_param;
    END IF;

    -- Validação: Verificar se id_utilizador não é nulo ou vazio
    IF id_utilizador_param IS NULL OR TRIM(id_utilizador_param) = '' THEN
        RAISE EXCEPTION 'O ID do utilizador não pode ser nulo ou vazio.';
    END IF;

    -- Validação: Verificar se data_requisicao não é futura
    IF data_requisicao_param IS NOT NULL AND data_requisicao_param > CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de requisição não pode ser futura.';
    END IF;

    -- Validação: Verificar se data_devolucao_prevista é futura
    IF data_devolucao_prevista_param <= CURRENT_DATE THEN
        RAISE EXCEPTION 'A data de devolução prevista deve ser futura.';
    END IF;

    -- Validação: Verificar se data_devolucao_real é válida
    IF data_devolucao_real_param IS NOT NULL AND data_devolucao_real_param < data_requisicao_param THEN
        RAISE EXCEPTION 'A data de devolução real não pode ser anterior à data de requisição.';
    END IF;

    -- Validação: Verificar se o estado é válido
    IF estado_param IS NOT NULL AND estado_param NOT IN ('Requisitado', 'Devolvido', 'Atrasado') THEN
        RAISE EXCEPTION 'Estado inválido: %. Deve ser Requisitado, Devolvido ou Atrasado.', estado_param;
    END IF;

    -- Atualizar os dados da requisição
    UPDATE Requisicoes
    SET id_livro = id_livro_param,
        id_utilizador = id_utilizador_param,
        data_requisicao = COALESCE(data_requisicao_param, data_requisicao),
        data_devolucao_prevista = data_devolucao_prevista_param,
        data_devolucao_real = data_devolucao_real_param,
        estado = COALESCE(estado_param, estado)
    WHERE id_requisicao = id_param;
END;
$$;

-- Procedimento para eliminar uma requisição
CREATE OR REPLACE PROCEDURE eliminar_requisicao(id_param INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validação: Verificar se a requisição existe
    IF NOT EXISTS (SELECT 1 FROM Requisicoes WHERE id_requisicao = id_param) THEN
        RAISE EXCEPTION 'Requisição com ID % não encontrada.', id_param;
    END IF;

    -- Excluir a requisição (o trigger verificará restrições)
    DELETE FROM Requisicoes WHERE id_requisicao = id_param;
END;
$$;

/******************************/
/*        STOCK RESERVA       */
/******************************/

-- Função para o trigger que verifica o stock antes de inserir uma reserva
CREATE OR REPLACE FUNCTION verificar_stock_reserva()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    stock_livro INTEGER;
    total_reservas_ativas INTEGER;
    total_requisicoes_ativas INTEGER;
BEGIN
    -- Obter o stock do livro
    SELECT stock INTO stock_livro
    FROM Livros
    WHERE id_livro = NEW.id_livro;

    -- Verificar se o livro existe
    IF stock_livro IS NULL THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', NEW.id_livro;
    END IF;

    -- Contar reservas ativas ou pendentes não expiradas para o mesmo livro no mesmo dia
    SELECT COUNT(*) INTO total_reservas_ativas
    FROM Reservas
    WHERE id_livro = NEW.id_livro
      AND estado IN ('Pendente', 'Ativa')
      AND (data_expiracao IS NULL OR data_expiracao >= CURRENT_DATE)
      AND data_reserva = CURRENT_DATE;

    -- Contar requisições ativas para o mesmo livro no mesmo dia
    SELECT COUNT(*) INTO total_requisicoes_ativas
    FROM Requisicoes
    WHERE id_livro = NEW.id_livro
      AND estado IN ('Requisitado', 'Atrasado')
      AND data_devolucao_real IS NULL
      AND data_requisicao = CURRENT_DATE;

    -- Verificar se o total de reservas e requisições excede o stock
    IF (total_reservas_ativas + total_requisicoes_ativas + 1) > stock_livro THEN
        RAISE EXCEPTION 'Não é possível criar a reserva para o livro com ID %: stock insuficiente (disponível: %, necessário: %).',
            NEW.id_livro, stock_livro, (total_reservas_ativas + total_requisicoes_ativas + 1);
    END IF;

    RETURN NEW;
END;
$$;

-- Trigger que executa a função antes de inserir uma reserva
CREATE OR REPLACE TRIGGER trigger_verificar_stock_reserva
BEFORE INSERT ON Reservas
FOR EACH ROW
EXECUTE FUNCTION verificar_stock_reserva();

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
    total_reservas_ativas INTEGER;
    total_requisicoes_ativas INTEGER;
BEGIN
    -- Obter o stock do livro
    SELECT stock INTO stock_livro
    FROM Livros
    WHERE id_livro = NEW.id_livro;

    -- Verificar se o livro existe
    IF stock_livro IS NULL THEN
        RAISE EXCEPTION 'Livro com ID % não encontrado.', NEW.id_livro;
    END IF;

    -- Contar reservas ativas ou pendentes não expiradas para o mesmo livro no mesmo dia
    SELECT COUNT(*) INTO total_reservas_ativas
    FROM Reservas
    WHERE id_livro = NEW.id_livro
      AND estado IN ('Pendente', 'Ativa')
      AND (data_expiracao IS NULL OR data_expiracao >= CURRENT_DATE)
      AND data_reserva = CURRENT_DATE;

    -- Contar requisições ativas para o mesmo livro no mesmo dia
    SELECT COUNT(*) INTO total_requisicoes_ativas
    FROM Requisicoes
    WHERE id_livro = NEW.id_livro
      AND estado IN ('Requisitado', 'Atrasado')
      AND data_devolucao_real IS NULL
      AND data_requisicao = CURRENT_DATE;

    -- Verificar se o total de reservas e requisições excede o stock
    IF (total_reservas_ativas + total_requisicoes_ativas + 1) > stock_livro THEN
        RAISE EXCEPTION 'Não é possível criar a requisição para o livro com ID %: stock insuficiente (disponível: %, necessário: %).',
            NEW.id_livro, stock_livro, (total_reservas_ativas + total_requisicoes_ativas + 1);
    END IF;

    RETURN NEW;
END;
$$;

-- Trigger que executa a função antes de inserir uma requisição
CREATE OR REPLACE TRIGGER trigger_verificar_stock_requisicao
BEFORE INSERT ON Requisicoes
FOR EACH ROW
EXECUTE FUNCTION verificar_stock_requisicao();