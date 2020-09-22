from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

GENDER = [("F", 'Female'),
          ("M", 'Male'),
          ("0", 'Other')]


class AccountManager(BaseUserManager):

    def create_user(self, email, mobile, password=None):
        if not email:
            raise ValueError("Email is Mandatory")
        if not mobile:
            raise ValueError("Username Number is Mandatory")

        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
            username=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, email, password):
        user = self.create_user(email=self.normalize_email(email),
                                password=password,
                                mobile=mobile)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Accounts(AbstractUser):
    email = models.EmailField(verbose_name="Email/Username", max_length=60, unique=True)
    # username = models.CharField(max_length=30, unique=True)
    # # id = models.IntegerField(db_index=True,auto_created=True,unique=True,primary_key=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    date_joined = models.DateTimeField(verbose_name="Date Login", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Last joined", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    gender = models.CharField(choices=GENDER, max_length=15)
    mobile = models.IntegerField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', ]

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
