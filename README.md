<!-- 
README:
This HTML file is part of a Django web application that allows users to upload CSV files,
process them asynchronously using Celery, and display the processed results dynamically.

Features:
- Upload CSV files via the form.
- Display upload status and processing status.
- Show processed data in a table format.
- Implement search functionality to filter data by product name.

Technologies Used:
- jQuery for AJAX requests and DOM manipulation.
- Bootstrap for styling.
- Django for backend processing.
- Celery for asynchronous task handling.

Instructions:
1. Upload a CSV file using the form.
2. The upload status will be displayed.
3. Once processing is complete, the processed data will be shown in the table.
4. Use the search input to filter the displayed data.

-->
## 🔧 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/maheshballi/Django-Celery-CSV.git
cd csv_processor
```

### 2️⃣ Create a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root and add:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=*
CELERY_BROKER_URL=redis://localhost:6380/0
```

### 4️⃣ Run Redis Server

Ensure Redis is running on **port 6380**:

```bash
redis-server --port 6380
```

Check Redis is running:

```bash
redis-cli -p 6380 ping  # Should return "PONG"
```

### 5️⃣ Run Celery Worker

Start the Celery worker in a separate terminal:

```bash
celery -A csv_processor worker --loglevel=info --pool=solo 
```

### 6️⃣ Run Django Server

Apply migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

### 7️⃣ Upload a CSV File & Test

- Open `http://127.0.0.1:8000/` in your browser.
- Upload a CSV file and observe the processed results.
- Use the search functionality to filter data dynamically.

## 🎯 Features Implemented

✅ **Django Views** – Handle file uploads\
✅ **Celery Integration** – Process CSV files asynchronously\
✅ **Redis Setup** – Acts as a message broker for Celery\
✅ **Pandas for Data Processing** – Perform sum, average, and count calculations\
✅ **Dynamic Search** – Filter records by product name\
✅ **JavaScript & AJAX for Dynamic Updates** –  Ensure real-time feedback and data display
   