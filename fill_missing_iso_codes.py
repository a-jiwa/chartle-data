import csv
from add_country_codes import get_iso_mapping

# Manual fixes for countries/entities that may not be in the mapping
MANUAL_CODES = {
    'Ivory Coast': 'CIV',
    'Northern Mariana Islands': 'MNP',
    'Bermuda': 'BMU',
    'Niue': 'NIU',
    # Add more as needed
}

def fill_missing_iso_codes(input_csv, output_csv):
    iso_mapping = get_iso_mapping()
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            entity = row['entity']
            code = row['Code']
            if not code:
                # Try to get code from mapping or manual fixes
                code = iso_mapping.get(entity, MANUAL_CODES.get(entity, ''))
                row['Code'] = code
            writer.writerow(row)

if __name__ == '__main__':
    fill_missing_iso_codes(
        'data/GBD_ebola_death_rate_ready.csv',
        'data/GBD_ebola_death_rate_ready_full.csv'
    )
