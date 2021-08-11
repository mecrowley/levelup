from django.db import models


class Event(models.Model):
    """Event Model
    Fields:
        organizer (ForeignKey): the user that made the event
        game (ForeignKey): the game associated with the event
        date (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (TextField): The text description of the event
        attendees (ManyToManyField): The gamers attending the event
    """
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")

    def __str__(self):
        return self.description

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
