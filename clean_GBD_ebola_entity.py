import csv

def fix_entity_and_missing_codes(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['entity', 'Code', 'year', 'val']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            # Rename 'location' to 'entity'
            entity = row['location']
            code = row['Code']
            # Only write rows with a non-empty ISO code
            if code:
                writer.writerow({
                    'entity': entity,
                    'Code': code,
                    'year': row['year'],
                    'val': row['val']
                })

if __name__ == '__main__':
    fix_entity_and_missing_codes(
        'data/GBD_ebola_death_rate_final.csv',
        'data/GBD_ebola_death_rate_ready.csv'
    )
