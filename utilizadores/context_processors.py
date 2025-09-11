from utilizadores.mongo_utils import is_admin, is_bibliotecario, is_membro

def user_roles(request):
    if request.user.is_authenticated:
        django_user_id = request.user.id
        return {
            'is_admin': is_admin(django_user_id),
            'is_bibliotecario': is_bibliotecario(django_user_id),
            'is_membro': is_membro(django_user_id),
        }
    return {
        'is_admin': False,
        'is_bibliotecario': False,
        'is_membro': False,
    }