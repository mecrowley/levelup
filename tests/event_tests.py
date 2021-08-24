import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game, Gamer, Event


class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()

        game = Game()
        game.game_type_id = 1
        game.skill_level = 5
        game.title = "Monopoly"
        game.maker = "Milton Bradley"
        game.number_of_players = 4
        game.gamer_id = 1

        game.save()


    def test_create_event(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/events"
        data = {
            "gameId": 1,
            "date": "2021-09-01",
            "time": "12:00:00",
            "description": "Monopoly Party"
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["date"], "2021-09-01")
        self.assertEqual(json_response["time"], "12:00:00")
        self.assertEqual(json_response["description"], "Monopoly Party")

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with an event
        event = Event()
        event.organizer_id = 1
        event.game_id = 1
        event.date = "2021-09-01"
        event.time = "12:00:00"
        event.description = "Monopoly Party"
        event.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["date"], "2021-09-01")
        self.assertEqual(json_response["time"], "12:00:00")
        self.assertEqual(json_response["description"], "Monopoly Party")

    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        event.organizer_id = 1
        event.game_id = 1
        event.date = "2021-09-01"
        event.time = "12:00"
        event.description = "Monopoly Party"
        event.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameId": 1,
            "date": "2021-09-01",
            "time": "12:00:00",
            "description": "Monopoly Party"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["date"], "2021-09-01")
        self.assertEqual(json_response["time"], "12:00:00")
        self.assertEqual(json_response["description"], "Monopoly Party")

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        event.organizer_id = 1
        event.game_id = 1
        event.date = "2021-09-01"
        event.time = "12:00:00"
        event.description = "Monopoly Party"
        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
