import csv

# Columns to keep in the final cleaned file
COLUMNS_TO_KEEP = ['location', 'Code', 'year', 'val']

def remove_unneeded_columns(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=COLUMNS_TO_KEEP)
        writer.writeheader()
        for row in reader:
            filtered_row = {col: row[col] for col in COLUMNS_TO_KEEP}
            writer.writerow(filtered_row)

if __name__ == '__main__':
    remove_unneeded_columns(
        'data/GBD_ebola_death_rate_cleaned.csv',
        'data/GBD_ebola_death_rate_final.csv'
    )
