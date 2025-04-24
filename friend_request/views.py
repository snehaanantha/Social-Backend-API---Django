from rest_framework import viewsets, permissions
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from django.db.models import Q                   
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User
from random import sample

class FriendRequestViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def send(self, request):
        to_user = User.objects.get(id=request.data['to_user'])
        req, _ = FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user, status='pending')
        return Response(FriendRequestSerializer(req).data)

    @action(detail=False, methods=['post'])
    def respond(self, request):
        try:
            # Get the friend request based on the request_id
            fr = FriendRequest.objects.get(id=request.data['request_id'])
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=404)

        action = request.data['action']

        if action == 'accept':
            # Change the status of the friend request to 'accepted'
            fr.status = 'accepted'

            # Ensure the friendship is created only once, with the smaller ID first
            if fr.from_user.id > fr.to_user.id:
                fr.from_user, fr.to_user = fr.to_user, fr.from_user

            # Check if the friendship already exists
            existing_friendship = Friendship.objects.filter(
                user1=fr.from_user, user2=fr.to_user
            ).exists()

            if not existing_friendship:
                # Create the friendship if it doesn't exist
                Friendship.objects.create(user1=fr.from_user, user2=fr.to_user)

        elif action == 'reject':
            fr.status = 'rejected'

        # Save the friend request after updating the status
        fr.save()

        return Response(FriendRequestSerializer(fr).data)

    @action(detail=False, methods=['get'])
    def get_list(self, request):
        user = request.user
        print(user.id)
        # Get the current user

        # Get all friends where the current user is either user1 or user2
        friends = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

        # Get the distinct list of users who are friends with the current user
        friends_ids = friends.values_list('user1', 'user2')
        # Flatten the list and remove duplicates, excluding the current user
        friend_ids = set([uid for pair in friends_ids for uid in pair if uid != user.id])

        # Fetch all users who are friends
        users = User.objects.filter(id__in=friend_ids)
        
        return Response(UserSerializer(users, many=True).data)


    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        all_users = User.objects.exclude(id=request.user.id)
        current_friends = Friendship.objects.filter(user1=request.user).values_list('user2', flat=True)
        suggestions = all_users.exclude(id__in=current_friends)
        sampled = sample(list(suggestions), min(5, suggestions.count()))
        return Response(UserSerializer(sampled, many=True).data)
