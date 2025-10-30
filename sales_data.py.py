import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
db_file = "sales_data.db"
if os.path.exists(db_file):
    os.remove(db_file)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")
sales_data = [
    ("Apple", 10, 0.8),
    ("Banana", 20, 0.5),
    ("Orange", 15, 0.6),
    ("Apple", 12, 0.8),
    ("Banana", 18, 0.5),
    ("Orange", 10, 0.6),
    ("Mango", 8, 1.2),
]

cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sales_data)
conn.commit()
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)
print("=== SALES SUMMARY ===")
print(df)
plt.figure(figsize=(6, 4))
df.plot(kind='bar', x='product', y='revenue', legend=False)
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
print("\nBar chart saved as 'sales_chart.png'")
plt.show()
conn.close()
