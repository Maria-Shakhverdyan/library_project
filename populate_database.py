import asyncio
import httpx
import random
from faker import Faker

BASE_URL = "http://127.0.0.1:8000"  # URL вашего приложения
fake = Faker()

# --- Функция для создания книг ---
async def create_books(client, count=100):
    for _ in range(count):
        book_data = {
            "title": fake.catch_phrase(),
            "author": fake.name(),
            "publisher": fake.company(),
            "theme": random.choice(["Fiction", "Science", "History", "Technology", "Other"]),
            "description": fake.text(max_nb_chars=200)
        }
        response = await client.post(f"{BASE_URL}/books/", json=book_data)
        if response.status_code == 201:
            print(f"Book created: {response.json()['id']}")
        else:
            print(f"Failed to create book: {response.status_code}")

# --- Функция для создания читателей ---
async def create_readers(client, count=50):
    for _ in range(count):
        reader_data = {
            "name": fake.name(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "passport_number": fake.uuid4(),
            "is_active": random.choice([True, False])
        }
        response = await client.post(f"{BASE_URL}/readers/", json=reader_data)
        if response.status_code == 201:
            print(f"Reader created: {response.json()['id']}")
        else:
            print(f"Failed to create reader: {response.status_code}")

# --- Функция для создания выдач ---
async def create_loans(client, book_ids, reader_ids, count=30):
    for _ in range(count):
        loan_data = {
            "book_id": random.choice(book_ids),
            "reader_id": random.choice(reader_ids),
            "issue_date": fake.date_this_year().isoformat(),
            "due_date": fake.future_date(end_date="+30d").isoformat(),
        }
        response = await client.post(f"{BASE_URL}/loans/", json=loan_data)
        if response.status_code == 201:
            print(f"Loan created: {response.json()['id']}")
        else:
            print(f"Failed to create loan: {response.status_code}")

# --- Основной скрипт ---
async def main():
    async with httpx.AsyncClient() as client:
        # Создание книг
        print("Creating books...")
        await create_books(client, count=100)

        # Получение ID всех созданных книг
        response = await client.get(f"{BASE_URL}/books/")
        book_ids = [book["id"] for book in response.json()]

        # Создание читателей
        print("Creating readers...")
        await create_readers(client, count=50)

        # Получение ID всех созданных читателей
        response = await client.get(f"{BASE_URL}/readers/")
        reader_ids = [reader["id"] for reader in response.json()]

        # Создание выдач
        print("Creating loans...")
        await create_loans(client, book_ids, reader_ids, count=30)

# Запуск скрипта
if __name__ == "__main__":
    asyncio.run(main())