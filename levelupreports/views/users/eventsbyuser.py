"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection


def userevent_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    e.id,
                    e.date,
                    e.time,
                    g.title game_name,
                    e.description,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_event e
                JOIN
                    levelupapi_game g ON e.game_id = g.id
                JOIN
                    levelupapi_eventgamer eg ON eg.event_id = e.id
                JOIN
                    levelupapi_gamer gamer ON gamer.id = eg.gamer_id
                JOIN
                    auth_user u ON gamer.user_id = u.id
            """)

            dataset = db_cursor.fetchall()

            events_attended_by_user = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                event = Event()
                event.date = row["date"]
                event.time = row["time"]
                event.game_name = row["game_name"]
                event.description = row["description"]

                # Store the user's id
                uid = row["user_id"]

                # If the user's id is already a key in the dictionary...
                if uid in events_attended_by_user:

                    # Add the current game to the `games` list for it
                    events_attended_by_user[uid]['events'].append(event)

                else:
                    # Otherwise, create the key and dictionary value
                    events_attended_by_user[uid] = {
                        "id": uid,
                        "full_name": row["full_name"],
                        "events": [event]
                    }

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_events = events_attended_by_user.values()

        # Specify the Django template and provide data context
        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }

        return render(request, template, context)
