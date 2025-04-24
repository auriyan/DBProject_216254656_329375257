import random
import os

# מיקום תיקיית Programing בנתיב הנכון
network_path = "C:/Networks/work/programing"  # עדכן אם צריך

print(f"Saving to: {network_path}")

if not os.path.exists(network_path):
    os.makedirs(network_path)

# יצירת קובץ SQL עבור lesson_participants
file_path = os.path.join(network_path, 'lesson_participants_inserts.sql')
used_pairs = set()

with open(file_path, 'w') as f:
    while len(used_pairs) < 400:  # מוודאים 400 זוגות ייחודיים
        lid = random.randint(1, 100)
        cid = random.randint(1, 400)
        pair = (lid, cid)
        if pair not in used_pairs:
            used_pairs.add(pair)
            insert_statement = f"INSERT INTO lesson_participants (lid, cid) VALUES ({lid}, {cid});\n"
            f.write(insert_statement)

print(f"SQL script for lesson_participants created successfully at {file_path}")
