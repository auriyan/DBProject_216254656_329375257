import random
from datetime import datetime
import os

# מיקום תיקיית Programing בנתיב הנכון
network_path = "C:/Networks/work/programing"  # עדכן אם צריך

print(f"Saving to: {network_path}")

if not os.path.exists(network_path):
    os.makedirs(network_path)

# יצירת קובץ SQL עבור payment
file_path = os.path.join(network_path, 'payment_inserts.sql')
with open(file_path, 'w') as f:
    for pid in range(1, 401):  # 400 רשומות
        amount = round(random.uniform(10, 500), 2)
        pdate = datetime.now().strftime('%Y-%m-%d')
        lid = random.randint(1, 400)  # נניח שיש 200 שיעורים
        cid = random.randint(1, 400)  # נניח שיש 150 לקוחות
        eid = random.randint(1, 400)   # נניח שיש 20 קופאים
        insert_statement = f"INSERT INTO payment (pid, amount, pdate, lid, cid, eid) VALUES ({pid}, {amount}, '{pdate}', {lid}, {cid}, {eid});\n"
        f.write(insert_statement)

print(f"SQL script for payment created successfully at {file_path}")
