from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class AuthUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            return ValueError('Users must have an username')

        user = self.model(username=username, password=password)
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not username:
            return ValueError('Users must have an username')
        user = self.model(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class SRUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("ユーザID", unique=True, max_length=30)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, null=False)
    is_staff = models.BooleanField(default=False, null=False)

    USERNAME_FIELD = 'username'
    objects = AuthUserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def save(self, commit=True, *args, **kwargs):
        user = super(SRUser, self)
        user.set_password(user.password)
        super(SRUser, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=50, null=False)
    text = models.TextField(null=False)
    category = models.ForeignKey(Category, null=False)
    point = models.IntegerField(null=False)

    image = models.ImageField(upload_to="images/", blank=True)
    clear_user = models.ManyToManyField(SRUser, blank=True)

    def __str__(self):
        return self.title



