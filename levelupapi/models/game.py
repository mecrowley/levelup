from django.db import models


class Game(models.Model):
    """Game Model
    Fields:
        name (CharField): The name of the game
        game_type (ForeignKey): The type of game
        description (CharField): The description of the game
        number_of_players (IntegerField): The max number of players of the game
        maker (CharField): The company that made the game
    """
    name = models.CharField(max_length=100)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    number_of_players = models.IntegerField()
    maker = models.CharField(max_length=50)