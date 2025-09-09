
CREATE OR REPLACE PROCEDURE inserir_categoria(nome_param VARCHAR, descricao_param TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Categorias (nome, descricao) VALUES (nome_param, descricao_param);
END;
$$;

CREATE OR REPLACE PROCEDURE atualizar_categoria(id_param INT, nome_param VARCHAR, descricao_param TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Categorias SET nome = nome_param, descricao = descricao_param WHERE id_categoria = id_param;
END;
$$;

CREATE OR REPLACE PROCEDURE eliminar_categoria(id_param INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Categorias WHERE id_categoria = id_param;
END;
$$;


CREATE OR REPLACE PROCEDURE inserir_editora(nome_param VARCHAR, localizacao_param VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO Editoras (nome, localizacao) VALUES (nome_param, localizacao_param);
END;
$$;

CREATE OR REPLACE PROCEDURE atualizar_editora(id_param INT, nome_param VARCHAR, localizacao_param VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Editoras SET nome = nome_param, localizacao = localizacao_param WHERE id_editora = id_param;
END;
$$;

CREATE OR REPLACE PROCEDURE eliminar_editora(id_param INT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM Editoras WHERE id_editora = id_param;
END;
$$;