import csv
from pathlib import Path

output = Path('users.csv')
output.parent.mkdir(exist_ok=True)
with output.open('w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['username', 'password']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='unix')
    writer.writeheader()
