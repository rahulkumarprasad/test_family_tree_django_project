from django.urls import path
from . import views as vw

urlpatterns = [
    path("", vw.home, name="home"),
    path("create-person", vw.CreatePerson.as_view(), name = "create_person"),
    path("add-relation", vw.add_relation_ship, name = "add_relation"),
    path("get-count", vw.get_count_of_sons_daughter_wives, name = "get_count"),
    path("get-father-name", vw.get_father_name, name = "get_father_name")
]