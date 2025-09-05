# game/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Game

def _normalize_diff(raw: str):
    raw = (raw or "").strip().lower()
    if raw == "easy": return Game.DIFF_EASY
    if raw in ("med", "medium"): return Game.DIFF_MED
    return Game.DIFF_HARD

def home(request):
    """
    New game:
      /                         → 2-player
      /?vs=ai&ai=O&diff=medium → vs AI (AI plays O), medium difficulty
      /?vs=ai&ai=X&diff=hard   → vs AI (AI plays X), hard difficulty
    """
    vs = request.GET.get("vs")
    ai_mark = (request.GET.get("ai") or "O").upper()
    diff = _normalize_diff(request.GET.get("diff"))

    g = Game.objects.create(
        ai_enabled=(vs == "ai"),
        ai_player=("X" if ai_mark == "X" else "O"),
        ai_difficulty=diff,
    )

    # If AI starts (X), make its first move right away.
    if g.ai_enabled and g.ai_player == "X" and g.current_player == "X":
        g.ai_move()

    return redirect("game_page", game_id=g.id)

@ensure_csrf_cookie
def game_page(request, game_id):
    g = get_object_or_404(Game, pk=game_id)
    return render(request, "game/index.html", {"game": g})

def game_state(request, game_id):
    g = get_object_or_404(Game, pk=game_id)
    return JsonResponse(g.as_dict())

def move(request, game_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    g = get_object_or_404(Game, pk=game_id)
    try:
        pos = int(request.POST.get("pos"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "invalid pos"}, status=400)

    # Human move
    g.make_move(pos)

    # If AI should move now, do it immediately (single round-trip)
    if g.ai_enabled and g.status == Game.IN_PROGRESS and g.current_player == g.ai_player:
        g.ai_move()

    return JsonResponse(g.as_dict())

def restart(request, game_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    g = get_object_or_404(Game, pk=game_id)
    g.restart()

    # If AI starts after restart, move immediately
    if g.ai_enabled and g.current_player == g.ai_player:
        g.ai_move()

    return JsonResponse(g.as_dict())
