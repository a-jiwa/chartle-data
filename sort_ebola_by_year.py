import csv

input_csv = 'data/GBD_ebola_death_rate.csv'
output_csv = 'data/GBD_ebola_death_rate_chronological.csv'

with open(input_csv, newline='', encoding='utf-8') as infile:
    reader = list(csv.DictReader(infile))
    fieldnames = reader[0].keys() if reader else []
    # Sort by Year (as int), then by Entity
    reader_sorted = sorted(reader, key=lambda x: (int(x['Year']), x['Entity']))

with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader_sorted:
        writer.writerow(row)

print(f"Data reordered chronologically and saved to {output_csv}")
