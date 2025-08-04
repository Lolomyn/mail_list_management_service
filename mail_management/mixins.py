# mail_management/mixins.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(LoginRequiredMixin):
    """Проверяет, что пользователь является владельцем объекта"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.created_by != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого объекта")
        return super().dispatch(request, *args, **kwargs)


class ManagerMixin(LoginRequiredMixin):
    """Проверяет, что пользователь входит в группу 'Менеджеры'"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Менеджеры').exists():
            raise PermissionDenied("Требуются права менеджера")
        return super().dispatch(request, *args, **kwargs)


class OrdinaryUserMixin(LoginRequiredMixin):
    """Проверяет, что пользователь не является менеджером"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Менеджеры').exists():
            raise PermissionDenied("Менеджеры не могут выполнять это действие")
        return super().dispatch(request, *args, **kwargs)
