from rest_framework.permissions import BasePermission

class IsGerenteGroup(BasePermission):
    """
    Permissão que concede acesso apenas se o usuário estiver
    autenticado e pertencer ao grupo 'Gerentes' (ou for Admin).
    """
    message = "Acesso negado: Requer privilégios do grupo Gerentes ou Admin."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True

        return request.user.groups.filter(name='Gerentes').exists()