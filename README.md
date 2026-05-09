🚀 Talk To My Database

A Natural Language to SQL API built using FastAPI, PostgreSQL, and SQLAlchemy that allows users to query databases using plain English.

Example:

total amount per user

gets converted into:

SELECT users.name, SUM(transactions.amount)
FROM users
JOIN transactions ON transactions.user_id = users.id
GROUP BY users.name;

✨ Features
✅ Natural language query support
✅ Dynamic SQL query generation
✅ Automatic JOIN detection
✅ Aggregation support (SUM, AVG, COUNT, MIN, MAX)
✅ Group By support
✅ Ordering & Limiting
✅ Filter support (>, <, =)
✅ Semantic schema generation
✅ Swagger API testing
✅ PostgreSQL integration
✅ SQLAlchemy ORM support
✅ Rule-based NLP parser
✅ Optional LLM fallback support

🛠️ Tech Stack
Python
FastAPI
PostgreSQL
SQLAlchemy
Pydantic
Regex-based NLP
OpenRouter / Ollama (Optional LLM Support)

📂 Project Structure
talk_to_my_db/
│
├── app/
│   │
│   ├── nlp/
│   │   └── intent_parser.py
│   │
│   ├── schema/
│   │   ├── extractor.py
│   │   ├── schema_store.py
│   │   ├── semantic_builder.py
│   │   └── semantic_store.py
│   │
│   ├── database.py
│   ├── executor.py
│   ├── llm_parser.py
│   ├── main.py
│   ├── query_builder.py
│   └── schemas.py
│
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
1️⃣ Clone Repository
git clone <your-repo-url>
cd talk_to_my_db
2️⃣ Create Virtual Environment
python -m venv dbenv

Activate:

Linux/Mac
source dbenv/bin/activate
Windows
dbenv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
🗄️ Configure Database

Update your PostgreSQL connection inside:

app/database.py

Example:

DATABASE_URL = "postgresql://postgres:password@localhost/mydb"
▶️ Run Server
uvicorn app.main:app --reload
📘 Swagger API Docs

Open:

http://127.0.0.1:8000/docs
🔍 Example Queries
Basic Queries
show all users
list transactions
Aggregation Queries
total amount
average amount
count users
maximum amount
Group By Queries
total amount per user
sum amount by user
average amount by user
Filter Queries
amount > 1000
amount < 500
Ordering Queries
top 3 users by amount
highest amount
lowest amount

🧠 How It Works
Step 1 — Schema Extraction

The application automatically extracts:

tables
columns
foreign keys
relationships

from PostgreSQL.

Step 2 — Semantic Schema Generation

Builds a semantic layer with:

aliases
relationships
readable mappings
Step 3 — NLP Intent Parsing

Converts natural language into structured intent:

Example:

{
  "tables": ["transactions", "users"],
  "operation": "sum",
  "aggregation_column": "amount",
  "group_by": "user_id"
}
Step 4 — Dynamic SQL Generation

Builds SQL queries dynamically using SQLAlchemy.

Step 5 — Query Execution

Executes query safely and returns JSON response.

📌 Sample Response
{
  "success": true,
  "count": 4,
  "data": [
    {
      "display_value": "Ali",
      "sum_amount": 1700.5
    }
  ]
}
🔥 Future Improvements
✅ Smarter NLP parsing
✅ Better JOIN handling
✅ Multi-table querying
✅ LLM-powered query understanding
✅ Chat-based interface
✅ Query history
✅ Authentication & user roles
✅ Frontend dashboard
👨‍💻 Author
Ali Sarosh

Backend Developer passionate about:

Python
FastAPI
Flask
Databases
Backend Systems
AI-integrated applications
