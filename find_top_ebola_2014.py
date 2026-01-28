import csv

# Find the top value for 2014 in the Ebola death rate dataset
input_csv = 'data/GBD_ebola_death_rate.csv'
top_val = None
top_row = None

with open(input_csv, newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        if row.get('year') == '2014':
            try:
                val = float(row['val'])
                if (top_val is None) or (val > top_val):
                    top_val = val
                    top_row = row
            except Exception:
                continue

if top_row:
    print(f"Top value in 2014: {top_val} for {top_row['location']} (Code: {top_row.get('Code', '')})")
else:
    print("No data for 2014 found.")
