from django.db import models
from django.contrib.auth.models import User

# class Player(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class SudokuGame(models.Model):
    # id = models.AutoField(primary_key=True)
    players = models.ManyToManyField(User)

    def __repr__(self) -> str:
        return f"Sudoku{self.pk}"
    def __str__(self) -> str:
        return f"Sudoku{self.pk}"


class Cell(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.IntegerField(null=True)
    game = models.ForeignKey(SudokuGame, on_delete=models.CASCADE)
    right_border = models.BooleanField(default=False)
    bottom_border = models.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"({self.row}, {self.col})"

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


class Time(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sudoku_game = models.ForeignKey(SudokuGame, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'sudoku_game']

    def __repr__(self) -> str:
        return f"{self.sudoku_game} + {self.user}"

    def __str__(self) -> str:
        return f"{self.sudoku_game} + {self.user}"
