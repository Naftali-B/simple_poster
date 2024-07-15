import os
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from datetime import timedelta

# class Poster(models.Model):
#     # user = models.ForeignKey('core.User', on_delete=models.CASCADE)
#     date_created = models.DateTimeField(default=timezone.now)
    
#     event_title = models.CharField(max_length=50, blank=True)
#     event_subtitle = models.CharField(max_length=50, blank=True)
#     event_description = models.CharField(max_length=50, blank=True)
#     event_date = models.CharField(max_length=50, blank=True)
#     event_time = models.CharField(max_length=50, blank=True)
#     venue = models.CharField(max_length=50, blank=True)
#     contact_or_cta = models.CharField(max_length=50, blank=True)
#     overlay_img = models.FileField(upload_to='posters', null=True, blank=True)
#     cropped_img = models.FileField(upload_to='posters', null=True, blank=True)

#     # custom_delete
#     def delete(self, *args, **kwargs):
#         if self.overlay_img:
#             if os.path.isfile(self.overlay_img.path):
#                 os.remove(self.overlay_img.path)

#         if self.cropped_img:
#             if os.path.isfile(self.cropped_img.path):
#                 os.remove(self.cropped_img.path)

#         super().delete(*args, **kwargs)

#     def __str__(self):
#         return self.event_title
