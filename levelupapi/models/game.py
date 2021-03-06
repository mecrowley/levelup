from django.db import models


class Game(models.Model):
    """Game Model
    Fields:
        title (CharField): The title of the game
        game_type (ForeignKey): The type of game
        number_of_players (IntegerField): The max number of players of the game
        skill_level (IntegerField): The skill level of the game
        maker (CharField): The company that made the game
    """
    title = models.CharField(max_length=100)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    maker = models.CharField(max_length=50)

    def __str__(self):
        return self.title
