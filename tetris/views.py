from django.shortcuts import render, HttpResponse
from .tetris import Game
from django.views.decorators.csrf import csrf_exempt
from threading import Timer
from .models import Score


games = {}
flag = False

def step():
    for name in games:
        if not games[name].is_gameover():
            games[name].next_tick()

    r = Timer(1.0, step)
    r.start()


@csrf_exempt
def index(request):
    global flag
    if request.method == "GET":
        best_scores = ()
        if "name" in request.session:
            name = request.session["name"]
            game = games[name]
            if game.is_gameover():
                best_scores = users_score()
                del games[name]
                del request.session["name"]
            return render(request, 'tetris/index.html', {"game": game, "gamefield": game.get_gamefield_with_shape(), "scores": best_scores})
        else:
            return render(request, 'tetris/index.html', {"game": None, "gamefield": None})
    elif request.method == "POST":
        name = request.POST.get("name", "")
        request.session["name"] = name
        game = Game(20,10)
        games[name] = game
        if flag == False:
            flag = True
            step()
        return render(request, 'tetris/index.html', {"game": game, "gamefield": game.get_gamefield_with_shape()})


def action(request):
    if "name" in request.session:
        name = request.session["name"]
        game = games[name]
        key = request.GET.get("key", "")
        if key == "38":
            game.rotate()
        if key == "37":
            game.move_left()
        if key == "39":
            game.move_right()
        if key == "40":
            game.move_down()
    return HttpResponse(status=200)


def users_score():
    for name in games:
        Score.objects.create(name = name, score = games[name].score)
    for score in Score.objects.all().order_by("-score")[10:]:
        score.delete()
    return Score.objects.all().order_by("-score")[:10]
