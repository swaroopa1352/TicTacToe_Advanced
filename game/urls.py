# game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("g/<uuid:game_id>/", views.game_page, name="game_page"),

    # JSON API
    path("api/g/<uuid:game_id>/state/", views.game_state, name="state"),
    path("api/g/<uuid:game_id>/move/", views.move, name="move"),
    path("api/g/<uuid:game_id>/restart/", views.restart, name="restart"),
    # (optional) remove this if you don't need it anymore:
    # path("api/g/<uuid:game_id>/ai-move/", views.ai_move, name="ai_move"),
]
