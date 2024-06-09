import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trueDialer.settings")
import django

django.setup()
import random

from faker import Faker
from server.models import Contact, CustomUser, SpamReport

faker = Faker()

# Clear existing data
SpamReport.objects.all().delete()
Contact.objects.all().delete()
CustomUser.objects.all().delete()

# admin is the permanent superuser
admin = CustomUser.objects.create_superuser(
    phone_number="1234",
    password="1234",
    name="admin",
    email="admin@1234",
)


# Function to generate digit-only phone numbers
def generate_phone_number():
    return faker.numerify(text="###########")


# Create random users
users = []
for _ in range(20):
    user = CustomUser.objects.create_user(
        phone_number=generate_phone_number(),
        password="password123",
        name=faker.name(),
        email=faker.email() if random.choice([True, False]) else None,
    )
    users.append(user)

# Create random contacts for each user
for user in users:
    for _ in range(5):
        contact = Contact.objects.create(
            owner=user,
            name=faker.name(),
            phone_number=generate_phone_number(),
        )

        # Create random spam reports for each contact
        for _ in range(random.randint(0, 3)):
            SpamReport.objects.create(
                phone_number=contact.phone_number, reported_by=random.choice(users)
            )

# Having some users in each other contact
# with random name
for i in range(4):
    for j in range(4):
        Contact.objects.create(
            owner=users[i],
            name=faker.name(),
            phone_number=users[i + j + 1].phone_number,
        )

# Adding contact to admin user
for i in range(3):
    Contact.objects.create(
        owner=admin, name=users[i].name, phone_number=users[i].phone_number
    )


# Adding admin contact info to some users
for i in range(3):
    Contact.objects.create(
        owner=users[i], name=admin.name, phone_number=admin.phone_number
    )

print("Database populated with random data.")
