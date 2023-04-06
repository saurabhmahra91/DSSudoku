from django.contrib import admin
from sudoku.models import SudokuGame, Time, Cell
# Register your models here.
admin.site.register(SudokuGame)
admin.site.register(Cell)
admin.site.register(Time)