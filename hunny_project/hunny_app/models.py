from django.db import models
from django.contrib.auth.models import User
from PIL import Image, ImageDraw
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime

class Room(models.Model):
    capacity = 0
    name = models.CharField("roomname", max_length = 120)
    chatter = models.CharField("roomname", max_length = 120)
    messages = models.TextField(blank= True)

    def __str__(self):
        return self.name

class Profile(models.Model):
     # gender choices
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Nonbinary', 'Nonbinary')
    ]
    # gender preference choices
    PREFERRED_GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('No Preference', 'No Preference')
    ]
    # relationship type choices
    RELATIONSHIP_CHOICES = [
        ('Casual Dating', 'Casual Dating'),
        ('Serious Relationship', 'Serious Relationship'),
        ('Dating', 'Dating'),
        ('No Preference', 'No Preference')
    ]
    # user profile information
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, null=True, blank=True)
    birthday = models.DateField(default=None, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    image0 = models.ImageField(default='static/profile_pics/default.jpg', upload_to='static/profile_pics')
    image1 = models.ImageField(default='static/profile_pics/default.jpg', upload_to='static/profile_pics')
    image2 = models.ImageField(default='static/profile_pics/default.jpg', upload_to='static/profile_pics')
    # user's preferences
    gender_preference = models.CharField(max_length=100, choices=PREFERRED_GENDER_CHOICES, null=True, blank=True)
    relationship_preference = models.CharField(max_length=100, choices=RELATIONSHIP_CHOICES, null=True, blank=True)
    age_range = models.CharField(max_length=100, null=True, blank=True)
    match_radius = models.CharField(max_length=100, help_text='miles', blank=True, null=True)
    objects = models.Manager()
    # matching
    matches = models.ManyToManyField(User, related_name='matches', blank=True)
    who_like_me = models.ManyToManyField(User, related_name='who_like_me', blank=True)
    current_check = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

    def next_check(self):
        super().save()
        self.current_check = "dosomethinghere"
        return self.current_check

    def get_all_matches(self):
        return self.matches.all()

    def get_matches_count(self):
        return self.matches.all().count()

    @property
    def age(self):
        if self.birthday is None:
            return "Not set."
        return int((datetime.now().date() - self.birthday).days / 365.25)

#lilly_note
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.userprofile.save()

STATUS_CHOICES = (('match2', 'match2'), ('match2', 'match2'),)

class MatchRequest(models.Model):
    sender = models.ForeignKey(Profile, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name="receiver", on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all().reverse()[:1000]
