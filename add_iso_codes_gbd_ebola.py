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

def add_iso_codes_to_gbd(input_csv, output_csv):
    iso_mapping = get_iso_mapping()
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames.copy()
        # Insert 'Code' after 'location'
        code_index = fieldnames.index('location') + 1
        fieldnames.insert(code_index, 'Code')
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            entity = row['location']
            code = iso_mapping.get(entity, MANUAL_CODES.get(entity, ''))
            row['Code'] = code
            writer.writerow(row)

if __name__ == '__main__':
    add_iso_codes_to_gbd(
        'data/GBD_ebola_death_rate.csv',
        'data/GBD_ebola_death_rate_with_codes.csv'
    )
