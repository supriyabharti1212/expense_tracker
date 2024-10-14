from .models import Transaction
from django.contrib.auth.models import User
from faker import Faker
import random

fake = Faker('en_IN')

def transactionSeeder(records=10):
    users = User.objects.all()

    # Check if there are any users
    if not users.exists():
        print("No users found in the database. Please create some users before running the seeder.")
        return  # Exit the function if no users are found

    for i in range(records):
        description = fake.sentence(nb_words=6)
        amount = round(random.uniform(-1000, 1000), 2)
        created_by = random.choice(users)

        Transaction.objects.create(
            description=description,
            amount=amount,
            created_by=created_by
        )

    print(f'Successfully seeded {records} transactions.')
