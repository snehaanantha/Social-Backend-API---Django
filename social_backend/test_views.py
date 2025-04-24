from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import FriendRequest, Friendship

class UserTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password123', email='user2@example.com')
        self.user3 = User.objects.create_user(username='user3', password='password123', email='user3@example.com')
        self.user4 = User.objects.create_user(username='user4', password='password123', email='user4@example.com')

    # Test user registration
    def test_user_registration(self):
        data = {
            'username': 'new_user',
            'password': 'password123',
            'email': 'new_user@example.com'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 5)  # Ensure a new user is created

    # Test user login (JWT)
    def test_user_login(self):
        data = {
            'username': 'user1',
            'password': 'password123',
        }
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Ensure JWT token is returned

    # Test get user profile
    def test_get_user_profile(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get('/api/auth/register/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user1')

    # Test list users excluding self
    def test_list_users_excluding_self(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get('/api/auth/register/list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        usernames = [user['username'] for user in response.data]
        self.assertNotIn('user1', usernames)  # Ensure user1 is not in the list

    # Test friend suggestions
    def test_friend_suggestions(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get('api/friends/suggestions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Should return 3 friend suggestions excluding user1

    # Test send friend request
    def test_send_friend_request(self):
        self.client.login(username='user1', password='password123')
        data = {'to_user_id': self.user2.id}
        response = self.client.post('/api/friends/send_request/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FriendRequest.objects.count(), 1)  # Ensure a new friend request is created

    # Test accept friend request
    def test_accept_friend_request(self):
        self.client.login(username='user2', password='password123')
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2, status='pending')
        data = {'request_id': 1, 'action': 'accept'}
        response = self.client.post('/api/friends/respond/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequest.objects.get(id=1).status, 'accepted')
        self.assertTrue(Friendship.objects.filter(user1=self.user1, user2=self.user2).exists())

    # Test reject friend request
    def test_reject_friend_request(self):
        self.client.login(username='user2', password='password123')
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2, status='pending')
        data = {'request_id': 1, 'action': 'reject'}
        response = self.client.post('/api/friends/respond/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(FriendRequest.objects.get(id=1).status, 'rejected')

    # Test list friends
    def test_list_friends(self):
        self.client.login(username='user1', password='password123')
        Friendship.objects.create(user1=self.user1, user2=self.user2)
        response = self.client.get('/api/friends/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        friend_usernames = [user['username'] for user in response.data]
        self.assertIn('user2', friend_usernames)  # Ensure user2 is listed as a friend
