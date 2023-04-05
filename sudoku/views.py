from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import SudokuGame, Cell, Time
from .forms import LoginForm, SigninForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as login_user, authenticate
from django.shortcuts import get_object_or_404
from .library import Sudoku, isValidSudoku, isOriginalSudoku, UTC_to_local
from django.contrib import messages
from datetime import datetime
from DSSudoku.settings import TIME_ZONE
import pytz


def index(request):
    signin_form = SigninForm()
    login_form = LoginForm()
    return render(request, 'sudoku/index.html', {'login_form': login_form, 'signin_form': signin_form})


def register(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_user(request, user)
            print("registration successful. loggin in and redirecting to user home")
            return redirect('/user-home')
        else:
            print("invalid form. redirecting to index")
            return redirect('/index')
    else:
        print("get method observed.")
        return redirect('/index')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_user(request, user)
                return redirect('/user-home')
            else:
                print('invalid user credentials')
                return redirect('/index')
        else:
            print('invalid login form submitted. redirecting to index')
            return redirect('/index')
    else:
        print('Get method observed. Redirecting to index')
        return redirect('/index')


@login_required
def user_home(request):
    return render(request, 'sudoku/user-home.html', {"user": request.user})


# todo : when a user submits incomplete board, he should get back his work instead of all none again
@login_required
def results(request, id):
    if request.method == "POST":
        values = request.POST.get("values")
        game = get_object_or_404(SudokuGame, id=id)
        cells = game.cell_set.all()

        # check of original sudoku
        if not isOriginalSudoku(values, cells):
            messages.error(request, "The sudoku is not the original sudoku.")
            return redirect(f'/board/{id}')

        if len(values) < 81:
            messages.error(request, "Complete all the entries first!!")
            return redirect(f'/board/{id}')

        if not isValidSudoku(values):
            messages.error(
                request, "The sudoku does not meet the rules criteria")
            return redirect(f'/board/{id}')

        time_obj = Time.objects.filter(
            user=request.user, sudoku_game=game).first()

        if not time_obj.time_taken:
            started_time = time_obj.start_time
            time_obj.time_taken = datetime.now(
                pytz.timezone(TIME_ZONE)) - started_time
            time_obj.save()

        time_taken = dict()
        for user in game.players.all():
            td = Time.objects.filter(
                user=user, sudoku_game=game).first().time_taken
            hours, remainder = divmod(td.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_taken[user.username] = f"{hours} hours, {minutes} minutes, and {seconds} seconds"
        return render(request, 'sudoku/results.html', {'time_taken': time_taken.items(), 'creation_time': UTC_to_local(time_obj.start_time).strftime("%Y-%m-%d %H:%M:%S")})
    else:
        return redirect(f'/board/{id}')


@login_required
def board(request, id):
    game = get_object_or_404(SudokuGame, id=id)
    time_obj = Time.objects.filter(user=request.user, sudoku_game=game).first()
    users = game.players.all()
    user_details = []
    for user in users:
        time = Time.objects.filter(user=user, sudoku_game=game).first()
        time_taken = time.time_taken
        # user_info = {
        #     'username': user.username,
        #     # 'hour_started': UTC_to_local(time.start_time).hour,
        #     # 'minute_started': UTC_to_local(time.start_time).minute,
        #     # 'second_started': UTC_to_local(time.start_time).second,
        #     'time_taken': str(time_taken),
        # }
        user_info = (user.username, UTC_to_local(time.start_time).strftime(
            "%Y-%m-%d %H:%M:%S"), str(time.time_taken))
        user_details.append(user_info)
    return render(
        request,
        "sudoku/gameboard.html",
        {
            "cells": game.cell_set.all(),
            'id': game.id,
            'start_time': time_obj.start_time.isoformat(),
            'users_info': user_details,
        })


@login_required
def create_game(request):
    game = SudokuGame()
    game.save()
    game.players.add(request.user)
    time_obj = Time(user=request.user, sudoku_game=game)
    time_obj.save()
    K = int(request.GET.get("K"))
    sudoku = Sudoku(9, K)
    sudoku.fillValues()

    for row in range(1, 10):
        for col in range(1, 10):
            cell = Cell(
                value=sudoku.mat[row-1][col-1] or None,
                row=row,
                col=col,
                right_border=(col == 3 or col == 6),
                bottom_border=(row == 3 or row == 6),
                game=game
            )

            cell.save()
    game.save()
    return redirect(f'/board/{game.id}')


@login_required
def join_game(request):
    id = request.GET.get('id')
    game = get_object_or_404(SudokuGame, pk=id)
    game.players.add(request.user)
    game.save()
    time_obj = Time(user=request.user, sudoku_game=game)
    time_obj.save()
    return redirect(f'/board/{game.id}')
