from pymongo import MongoClient

def get_mongo_collection():
    client = MongoClient('mongodb://localhost:27017')
    db = client['biblioteca_mongo']
    return db['utilizadores_utilizador']

def inserir_utilizador(nome, contacto, numero_socio, user_id):
    colecao = get_mongo_collection()
    doc = {
        'nome': nome,
        'contacto': contacto,
        'numero_socio': numero_socio,
        'user_id': user_id
    }
    colecao.insert_one(doc)

def listar_utilizadores():
    colecao = get_mongo_collection()
    return list(colecao.find())