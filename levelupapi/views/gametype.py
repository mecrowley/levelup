"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import GameType
from rest_framework import status


class GameTypeView(ViewSet):
    """Level up game types"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized game instance
        """
        gametype = GameType()
        gametype.label = request.data["label"]

        try:
            gametype.save()
            serializer = GameTypeSerializer(gametype, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type, context={'request': request})
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            gametype = GameType.objects.get(pk=pk)
            gametype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all()

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = GameTypeSerializer(
            game_types, many=True, context={'request': request})
        return Response(serializer.data)

class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types

    Arguments:
        serializers
    """
    class Meta:
        model = GameType
        fields = ('id', 'label')
