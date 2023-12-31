from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    comment_count = models.IntegerField(default=0)
    tag = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/post/{self.slug}/"

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    website = models.CharField(max_length=128, blank=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)


class About(models.Model):
    title = models.CharField(max_length=128)
    about = models.TextField()
    image = models.ImageField(upload_to="images/")

    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)


class AboutPage(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    image = models.ImageField(upload_to="images/")


class ContactInfo(models.Model):
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    email = models.CharField(max_length=128)


class Contact(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    message = models.TextField()
