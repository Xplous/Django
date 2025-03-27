from django.db import models
from django.urls import reverse

class Partner(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    logo = models.ImageField(upload_to='partners_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('partner_detail', args=[str(self.id)])

class Comment(models.Model):
    partner = models.ForeignKey(Partner, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.author} для {self.partner.name}"
