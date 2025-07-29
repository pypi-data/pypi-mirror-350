
# Abstract Frame Hub Client

**AbstractFrameHubClient** is a Python client for interacting with **AbstractFrameHub**, a secure, schema-aware, and cloud-ready data layer inspired by MongoDB. It supports document validation, user and permission management, and future AI-enhanced data features.

---

## 📦 Installation

Install via PyPI:

```bash
pip install abstract-framehub-client
```

Or install from source:

```bash
git clone https://gitlab.com/stackngo-client/abstractframehub-client-python.git
cd abstractframehub-client-python
pip install .
```

---

## 🚀 Quick Start

```python
from abstract-framehub-client import AbstractFrameHubClient

# Connect and authenticate
client = AbstractFrameHubClient()
client.login("root", "afh-password")

# Select a database and collection
db = client.database("mydb")
try:
    db.create()
except AlreadyExistsException as e:
    pass
collection = db.collection("mycollection")

# Insert a document
collection.insert_one({"title": "Hello, FrameHub!", "likes": 0})

# Query documents
results = collection.find({"likes": {"$gte": 0}})
print(results)
```

---

## 🔐 Authentication

```python
client.login("root", "afh-password")
```

Stores a session token used automatically in future requests.

---

## 🗃️ Database & Collection API

```python
db = client.database("blog")
db.create()
db.drop()

collection = db.collection("posts")
collection.insert_one({...})
collection.find_one({"key": "value"})
collection.delete_many({})
```

---

## 📐 Schema Support

Define and enforce JSON schemas per collection:

```python
collection.schema({
    "bsonType": "object",
    "required": ["title", "content"],
    "properties": {
        "title": {"bsonType": "string"},
        "content": {"bsonType": "string"}
    },
    "additionalProperties": False
})
```

---

## 👤 User Management

```python
client.add_user({
    "username": "admin",
    "password": "securepass",
    "permissions": {"blog": "*"}
})
client.drop_user("admin")
```

---

## ❗ Error Handling

All errors raise custom exceptions:

- `NotAuthenticatedException`
- `ValidationException`
- `AlreadyExistsException`
- `AfhException` (generic)

---

## 🧪 Testing Example

```python
def test_insert_and_find():
    client = AbstractFrameHubClient()
    client.login("admin", "123456")
    db = client.database("testdb")
    coll = db.collection("items")
    doc_id = coll.insert_one({"name": "test item"})
    result = coll.find_one({"_id": doc_id})
    assert result["name"] == "test item"
```

---

## 📁 Project Structure

```
├── abstract_framehub_client
│   ├── __init__.py
│   ├── client.py
│   ├── exceptions.py
│   └── wrappers
│       ├── __init__.py
│       ├── collection.py
│       └── database.py
```

---

## 📝 License

This project is licensed under the MIT License.
