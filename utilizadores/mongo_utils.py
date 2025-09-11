from pymongo import MongoClient
from bson import ObjectId

def get_mongo_collection():
    client = MongoClient('mongodb://localhost:27017')
    db = client['biblioteca_mongo']
    return db['utilizadores']

def get_user_by_django_id(django_user_id):
    colecao = get_mongo_collection()
    return colecao.find_one({'django_user_id': django_user_id})

def inserir_utilizador(nome, contacto, django_user_id, role):
    colecao = get_mongo_collection()
    doc = {
        'nome': nome,
        'contacto': contacto,
        'django_user_id': django_user_id,  # ID do utilizador Django
        'role': role                       # 'admin', 'bibliotecario' ou 'membro'
    }
    colecao.insert_one(doc)

def listar_utilizadores():
    colecao = get_mongo_collection()
    return list(colecao.find())

def obter_utilizador_por_id(pk):
    colecao = get_mongo_collection()
    return colecao.find_one({'_id': ObjectId(pk)})

def atualizar_utilizador(pk, dados):
    colecao = get_mongo_collection()
    colecao.update_one({'_id': ObjectId(pk)}, {'$set': dados})

def get_role_by_django_id(django_user_id):
    user = get_user_by_django_id(django_user_id)
    return user['role'] if user and 'role' in user else None

def is_admin(django_user_id):
    return get_role_by_django_id(django_user_id) == 'admin'

def is_bibliotecario(django_user_id):
    return get_role_by_django_id(django_user_id) == 'bibliotecario'

def is_membro(django_user_id):
    return get_role_by_django_id(django_user_id) == 'membro'
