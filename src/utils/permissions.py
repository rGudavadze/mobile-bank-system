from rest_framework.permissions import BasePermission


class IsCardListOwner(BasePermission):
    def has_permission(self, request, view):
        queryset = view.get_queryset()
        return all(card.account.profile.user == request.user for card in queryset)


class IsCardDetailOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.account.profile.user
