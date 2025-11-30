from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Collection(models.Model):
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
        ('public', 'Public'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    emoji = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.owner})'

class Tag(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('owner', 'name')
        ordering = ['name']

        def __str__(self):
            return self.name

class Item(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    note = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='items')

    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or self.url or f'Item {self.pk}'