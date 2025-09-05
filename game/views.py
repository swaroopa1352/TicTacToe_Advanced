from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from . import logic

def index(request):
    return render(request, "game/index.html")

def move(request, pos):
    pos = int(pos)
    result = logic.make_move(pos)
    return JsonResponse(result)

def restart(request):
    logic.reset_game()
    return JsonResponse({"board": logic.board, "winner": None, "player": "X"})