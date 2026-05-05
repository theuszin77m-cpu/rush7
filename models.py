from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
**tablename** = "users"

```
id = Column(Integer, primary_key=True)
username = Column(String, unique=True)
password = Column(String)
saldo = Column(Integer, default=100)
```

class Bet(Base):
**tablename** = "bets"

```
id = Column(Integer, primary_key=True)
user_id = Column(Integer)
game = Column(String)
result = Column(String)
amount = Column(Integer)
```
