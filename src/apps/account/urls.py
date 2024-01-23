from django.urls import path

from .views import AccountDetail, AccountList

urlpatterns = [
    path("", AccountList.as_view(), name="todo-list"),
    path("<uuid:pk>", AccountDetail.as_view(), name="todo-details"),
]
