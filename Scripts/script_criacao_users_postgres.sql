/***********************************/
/* CRIAÇÃO DE ROLES E UTILIZADORES */
/***********************************/

-- Criar roles no PostgreSQL
CREATE ROLE admin_role;
CREATE ROLE bibliotecario_role;
CREATE ROLE membro_role;

-- Conceder privilégios básicos para as roles
GRANT ALL PRIVILEGES ON SCHEMA public TO admin_role;
GRANT USAGE ON SCHEMA public TO bibliotecario_role;
GRANT USAGE ON SCHEMA public TO membro_role;

-- Conceder privilégios para a role admin_role (todas as operações em todas as tabelas do schema public)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_role;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin_role;

-- Conceder privilégios para a role bibliotecario_role (todas as operações nas tabelas especificadas)
GRANT ALL PRIVILEGES ON Categorias, Autores, Editoras, Livros, Requisicoes TO bibliotecario_role;
GRANT ALL PRIVILEGES ON SEQUENCE categorias_id_categoria_seq, autores_id_autor_seq, editoras_id_editora_seq, livros_id_livro_seq, requisicoes_id_requisicao_seq TO bibliotecario_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO bibliotecario_role;

-- Conceder privilégios para a role membro_role (apenas leitura nas tabelas especificadas)
GRANT SELECT ON Categorias, Autores, Editoras, Livros, Requisicoes TO membro_role;

-- Conceder permissões específicas para as funções permitidas
GRANT EXECUTE ON FUNCTION filtrar_livros(VARCHAR, BOOLEAN, BOOLEAN) TO membro_role;
GRANT EXECUTE ON FUNCTION filtrar_requisicoes(VARCHAR, VARCHAR, BOOLEAN, BOOLEAN) TO membro_role;
GRANT EXECUTE ON FUNCTION livro_mais_requisitado() TO membro_role;
GRANT EXECUTE ON FUNCTION livros_disponiveis_por_livro(INTEGER) TO membro_role;
GRANT EXECUTE ON FUNCTION livros_disponiveis_requisicao() TO membro_role;

-- Criar utilizadores e associar às roles
CREATE USER admin_user WITH PASSWORD 'password';
GRANT admin_role TO admin_user;

CREATE USER bibliotecario_user WITH PASSWORD 'password';
GRANT bibliotecario_role TO bibliotecario_user;

CREATE USER membro_user WITH PASSWORD 'password';
GRANT membro_role TO membro_user;

-- Garantir que as roles tenham privilégios futuros (para tabelas e sequências criadas posteriormente)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO bibliotecario_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO bibliotecario_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO membro_role;