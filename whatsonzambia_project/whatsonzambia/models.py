from audioop import reverse
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from PIL import Image
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.text import slugify
from hitcount.models import HitCountMixin, HitCount

class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    fullname = models.CharField(max_length=100)
    contact = PhoneNumberField(null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Category(models.Model):
    name = models.CharField(verbose_name='Category', max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('whatsonzambia-home')


class Post(models.Model):
    title = models.CharField(verbose_name='Event Name', max_length=100)
    content = models.TextField(verbose_name='More Information', max_length=350)
    date_posted = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['-date_posted']

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    views = models.ManyToManyField(IpModel, related_name="post_views", blank=True)
    likes = models.ManyToManyField(IpModel, related_name="post_likes", blank=True)
    charge = models.CharField(verbose_name='Charges', max_length=100)
    venue = models.CharField(verbose_name='Event Venue', max_length=100)
    event_day = models.CharField(verbose_name='Event Day',max_length=100)
    event_date = models.CharField(verbose_name='Event Date', max_length=50)
    town = models.CharField(verbose_name='Town/City', max_length=100)
    event_time = models.TimeField(verbose_name='Event Time',)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    category = models.CharField(max_length=255)
    post_image = models.ImageField(verbose_name='Uploadadvert Image', upload_to='post_img', null=True, blank=True)

    def __str__(self):
        return self.title

    def total_views(self):
        return self.views.count()

    def total_likes(self):
        return self.likes.count()

    def save(self):
        super().save()

        img = Image.open(self.post_image.path)

        if img.height > 350 or img.width > 700:
            output_size = (700, 350)
            img.thumbnail(output_size)
            img.save(self.post_image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class PostFeature(models.Model):
    ft_title = models.CharField(verbose_name='Event Name', max_length=100)
    ft_content = models.TextField(verbose_name='More Information', max_length=350)
    ft_date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ft_charge = models.CharField(verbose_name='Charges',max_length=100)
    ft_venue = models.CharField(verbose_name='Venue',max_length=100)
    ft_event_day = models.CharField(verbose_name='Event Day',max_length=100)
    ft_views = models.ManyToManyField(IpModel, related_name="feature_views", blank=True)
    ft_likes = models.ManyToManyField(IpModel, related_name="feature_likes", blank=True)
    ft_event_date = models.CharField(verbose_name='Event Date',max_length=50)
    ft_town = models.CharField(verbose_name='Town/City', max_length=100)
    ft_event_time = models.TimeField(verbose_name='Event Time')
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    ft_post_image = models.ImageField(verbose_name='Upload Advert Image', upload_to='feat_img', null=True, blank=True)

    def __str__(self):
        return self.ft_title

    def total_ft_views(self):
        return self.ft_views.count()

    def total_ft_likes(self):
        return self.ft_likes.count()

    def save(self):
        super().save()

        img = Image.open(self.ft_post_image.path)

        if img.height > 700 or img.width > 800:
            output_size = (800, 700)
            img.thumbnail(output_size)
            img.save(self.ft_post_image.path)

    def get_absolute_url(self):
        return reverse('whatsonzambia-home')
