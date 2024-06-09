from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The Phone Number field must be set")

        # create custom user instance
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create a corresponding Contact instance each time a user is created.
        # This allows us to search for details by name or phone number only
        # in the Contact model, without needing to query both the CustomUser
        # and Contact models.
        Contact.objects.create(
            owner=user,
            name=user.name,
            phone_number=user.phone_number,
            is_registered_user=True,
        )

        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)

    # Remove username from the required fields
    # Using phone_number as the unique identifier
    username = None
    phone_number = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number


class Contact(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="contacts"
    )
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_registered_user = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class SpamReport(models.Model):
    phone_number = models.CharField(max_length=15)
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Spam Report: {self.phone_number}"

    @classmethod
    def get_spam_report_cnt(cls, phone_number):
        return cls.objects.filter(phone_number=phone_number).count()
