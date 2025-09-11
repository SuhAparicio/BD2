-- Inserções para a tabela Categorias
INSERT INTO Categorias (nome, descricao) VALUES
('Ficção', 'Livros de narrativa fictícia'),
('Ciência', 'Livros sobre temas científicos'),
('História', 'Livros históricos'),
('Fantasia', 'Livros de fantasia épica'),
('Biografia', 'Biografias e memórias'),
('Tecnologia', 'Livros sobre tecnologia e informática'),
('Romance', 'Livros românticos'),
('Mistério', 'Livros de suspense e mistério'),
('Poesia', 'Coletâneas de poemas'),
('Autoajuda', 'Livros de desenvolvimento pessoal');

-- Inserções para a tabela Autores
INSERT INTO Autores (nome, data_nascimento, nacionalidade) VALUES
('J.K. Rowling', '1965-07-31', 'Britânica'),
('Isaac Asimov', '1920-01-02', 'Americana'),
('Yuval Noah Harari', '1976-02-24', 'Israelense'),
('J.R.R. Tolkien', '1892-01-03', 'Britânica'),
('Agatha Christie', '1890-09-15', 'Britânica'),
('Steve Jobs', '1955-02-24', 'Americana'),
('Jane Austen', '1775-12-16', 'Britânica'),
('Gabriel García Márquez', '1927-03-06', 'Colombiana'),
('Emily Dickinson', '1830-12-10', 'Americana'),
('Dale Carnegie', '1888-11-24', 'Americana');

-- Inserções para a tabela Editoras
INSERT INTO Editoras (nome, localizacao) VALUES
('Penguin Books', 'Londres, Reino Unido'),
('Companhia das Letras', 'São Paulo, Brasil'),
('Random House', 'Nova Iorque, EUA'),
('Bloomsbury', 'Londres, Reino Unido'),
('Editora Rocco', 'Rio de Janeiro, Brasil'),
('Wiley', 'Hoboken, EUA'),
('Record', 'Rio de Janeiro, Brasil'),
('HarperCollins', 'Nova Iorque, EUA'),
('Leya', 'Lisboa, Portugal'),
('Intrínseca', 'Rio de Janeiro, Brasil');

-- Inserções para a tabela Livros
INSERT INTO Livros (titulo, isbn, stock, ano_publicacao, id_categoria, id_autor, id_editora) VALUES
('Harry Potter e a Pedra Filosofal', '9780747532699', 5, 1997, 4, 1, 4),
('Fundação', '9780553293357',5,  1951, 2, 2, 3),
('Sapiens: Uma Breve História da Humanidade', '9780062316097',5,  2011, 3, 3, 8),
('O Senhor dos Anéis', '9780261103573',5,  1954, 4, 4, 4),
('Assassinato no Expresso do Oriente', '9780062693662',5 , 1934, 8, 5, 8),
('Steve Jobs', '9781451648539',5,  2011, 5, 6, 3),
('Orgulho e Preconceito', '9780141439518',5,  1813, 7, 7, 1),
('Cem Anos de Solidão', '9780060883287',5,  1967, 7, 8, 8),
('Poemas Completos de Emily Dickinson', '9780316184137',5,  1955, 9, 9, 3),
('Como Fazer Amigos e Influenciar Pessoas', '9780671027032',5,  1936, 10, 10, 3),
('O Hobbit', '9780547928227',5,  1937, 4, 4, 4),
('Mistborn: O Império Final', '9780765311788',5,  2006, 4, 4, 3);

-- Inserções para a tabela Requisicoes
-- IDs fictícios de usuários do MongoDB
INSERT INTO Requisicoes (id_livro, id_utilizador, data_requisicao, data_devolucao_prevista, data_devolucao_real, estado) VALUES
(1, '66d8f123abc1234567890def', '2025-08-01', '2025-08-15', NULL, 'Requisitado'),
(2, '66d8f123abc1234567890df0', '2025-08-05', '2025-08-19', '2025-08-10', 'Devolvido'),
(3, '66d8f123abc1234567890df1', '2025-08-10', '2025-08-24', NULL, 'Requisitado'),
(4, '66d8f123abc1234567890df2', '2025-08-12', '2025-08-26', NULL, 'Requisitado'),
(5, '66d8f123abc1234567890df3', '2025-08-15', '2025-08-29', '2025-08-20', 'Devolvido'),
(6, '66d8f123abc1234567890df4', '2025-08-20', '2025-09-03', NULL, 'Requisitado'),
(7, '66d8f123abc1234567890df5', '2025-08-22', '2025-09-05', NULL, 'Requisitado'),
(8, '66d8f123abc1234567890df6', '2025-08-25', '2025-09-08', NULL, 'Requisitado'),
(9, '66d8f123abc1234567890df7', '2025-08-28', '2025-09-11', NULL, 'Requisitado'),
(10, '66d8f123abc1234567890df8', '2025-08-30', '2025-09-13', NULL, 'Requisitado'),
(11, '66d8f123abc1234567890df9', '2025-09-01', '2025-09-15', NULL, 'Requisitado'),
(12, '66d8f123abc1234567890dfa', '2025-09-03', '2025-09-17', NULL, 'Requisitado');