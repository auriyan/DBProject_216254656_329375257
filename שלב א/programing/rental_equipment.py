import random
import os

# מיקום תיקיית Programing בנתיב הנכון
network_path = "C:/Networks/work/programing"  # עדכן אם צריך

print(f"Saving to: {network_path}")

if not os.path.exists(network_path):
    os.makedirs(network_path)

# יצירת קובץ SQL עבור rental_equipment
file_path = os.path.join(network_path, 'rental_equipment_inserts.sql')
with open(file_path, 'w') as f:
    for rid in range(1, 401):  # 400 רשומות
        eid = random.randint(1, 401)  # eid אקראי מ-1 עד 50
        insert_statement = f"INSERT INTO rental_equipment (rid, eid) VALUES ({rid}, {eid});\n"
        f.write(insert_statement)

print(f"SQL script for rental_equipment created successfully at {file_path}")
