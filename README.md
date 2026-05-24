# 🚀 Talk To My Database

A Natural Language to SQL API built using **FastAPI, PostgreSQL, and SQLAlchemy** that allows users to query databases using plain English.

Example:

```text
total amount per user
```

gets converted into:

```sql
SELECT users.name,
SUM(transactions.amount)
FROM users
JOIN transactions
ON transactions.user_id = users.id
GROUP BY users.name;
```

---

# ✨ Features

✅ Natural Language Query Support  
✅ Dynamic SQL Query Generation  
✅ Automatic JOIN Detection  
✅ Aggregation Support (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`)  
✅ Group By Support  
✅ Ordering & Limiting  
✅ Filter Support (`>`, `<`, `=`)  
✅ Semantic Schema Generation  
✅ Swagger API Testing  
✅ PostgreSQL Integration  
✅ SQLAlchemy ORM Support  
✅ Rule-Based NLP Parser  
✅ Optional LLM Fallback Support  

---

# 🛠️ Tech Stack

## ⚙️ Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic

## 🧠 NLP & Query Parsing

- Regex-Based NLP
- Rule-Based Intent Parsing
- Semantic Schema Mapping

## 🤖 Optional AI Support

- OpenRouter
- Ollama

---

# 📂 Project Structure

```text
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
```

---

# ⚙️ Installation

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/talk_to_my_db.git

cd talk_to_my_db
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv dbenv
```

### Activate Virtual Environment

#### Linux / MacOS

```bash
source dbenv/bin/activate
```

#### Windows

```bash
dbenv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ Configure Database

Update your PostgreSQL connection inside:

```text
app/database.py
```

Example:

```python
DATABASE_URL = "postgresql://postgres:password@localhost/mydb"
```

---

# ▶️ Run Server

```bash
uvicorn app.main:app --reload
```

---

# 📘 Swagger API Docs

After running the server, open:

```text
http://127.0.0.1:8000/docs
```

---

# 🔍 Example Queries

---

## 📄 Basic Queries

```text
show all users
list transactions
show all orders
```

---

## 📊 Aggregation Queries

```text
total amount
average amount
count users
maximum amount
minimum amount
```

---

## 👥 Group By Queries

```text
total amount per user
sum amount by user
average amount by user
```

---

## 🎯 Filter Queries

```text
amount > 1000
amount < 500
age = 25
```

---

## 📈 Ordering Queries

```text
top 3 users by amount
highest amount
lowest amount
```

---

# 🧠 How It Works

---

## Step 1 — Schema Extraction

The application automatically extracts:

- Tables
- Columns
- Foreign Keys
- Relationships

from PostgreSQL databases.

---

## Step 2 — Semantic Schema Generation

Builds a semantic layer with:

- Aliases
- Relationships
- Human-readable mappings

---

## Step 3 — NLP Intent Parsing

Converts natural language into structured intent.

### Example Intent

```json
{
  "tables": ["transactions", "users"],
  "operation": "sum",
  "aggregation_column": "amount",
  "group_by": "user_id"
}
```

---

## Step 4 — Dynamic SQL Generation

Builds optimized SQL queries dynamically using SQLAlchemy.

---

## Step 5 — Query Execution

Executes queries safely and returns structured JSON responses.

---

# 📌 Sample API Response

```json
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
```

---

# 🔥 Future Improvements

✅ Smarter NLP Parsing  
✅ Better JOIN Handling  
✅ Multi-Table Querying  
✅ LLM-Powered Query Understanding  
✅ Chat-Based Interface  
✅ Query History  
✅ Authentication & User Roles  
✅ Frontend Dashboard  

---

# 🚀 Use Cases

- AI-powered Database Assistants
- Analytics Dashboards
- Business Intelligence Tools
- Internal Admin Tools
- Chat-to-SQL Applications
- Data Exploration Systems

---

# 📚 Key Learnings

This project helped in understanding:

- Natural Language Processing
- SQL Query Generation
- Database Relationships
- Dynamic ORM Queries
- FastAPI Backend Architecture
- Semantic Schema Design
- AI + Database Integrations

---

# 🤝 Contributing

Contributions are welcome.

## Steps

```bash
Fork → Clone → Create Branch → Commit → Push → Pull Request
```

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## Ali Sarosh

🎓 BTech CSE Student  
💻 Backend Developer (Python)  
🚀 Open Source Contributor  

### Interests

- Backend Development
- FastAPI & Flask
- SQLAlchemy
- AI-integrated Applications
- Database Systems
- NLP-based APIs

---

# 🔗 Connect With Me

## GitHub

https://github.com/AliSarosh15

## LinkedIn

https://www.linkedin.com/in/ali-sarosh-332b90280/

---

# ⭐ Support

If you found this project useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 🧠 Share feedback & suggestions

---

# 📌 Final Note

Talk To My Database is a real-world backend project that demonstrates how Natural Language Processing and database systems can work together to create intelligent SQL-powered APIs using FastAPI, PostgreSQL, and SQLAlchemy.
