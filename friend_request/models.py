from django.db import models
from users.models import User

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} | Status: {self.status}'

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_2')

    class Meta:
        unique_together = ('user1', 'user2')  # Ensures the pair is unique

    def save(self, *args, **kwargs):
        # Ensure user1 is always less than user2 to prevent duplication of friendships
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super(Friendship, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user1} <-> {self.user2}'
