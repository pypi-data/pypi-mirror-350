# 📦 PureDB

PureDB — bu Flask asosida ishlaydigan oddiy va xavfsiz JSON (pdb) bazasi tizimi.

## 🔧 O‘rnatish

```bash
pip install flask requests
```

Serverni ishga tushiring:

```bash
python app.py
```

## 🚀 Ishlatish

### 📡 Server orqali ishlash

API Endpointlar:
```
GET    /api/<server>/records
POST   /api/<server>/records
PUT    /api/<server>/records/<id>
DELETE /api/<server>/records/<id>
```

Har bir so‘rovga header kerak:
```
X-DB-Password: <hashed_password>
```

### 🧑‍💻 Python’da foydalanish

```python
from puredb import ServerDB

db = ServerDB('http://localhost:5000/api/mydb')
db.password('your_hashed_password')
db.add({'name': 'Ali'})
print(db.all())
```

## 🔐 Parol hashing

```python
from hashlib import sha256
h = sha256('your_password'.encode()).hexdigest()
```

## ❗ Xatoliklar

| Kod | Sabab              |
|-----|--------------------|
| 401 | Parol noto‘g‘ri    |
| 403 | Ruxsat yo‘q        |
| 404 | Server topilmadi   |

## 🧪 Test qilish

```bash
curl -H "X-DB-Password: <hash>" http://localhost:5000/api/mydb/records
```

## 📫 Muallif

Salohiddin Esanbekov  
Telegram: https://t.me/SalohiddinEsanbekov
