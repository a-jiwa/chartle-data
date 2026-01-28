import csv
from add_country_codes import get_iso_mapping

# Country name replacements for standardization
COUNTRY_REPLACEMENTS = {
    "Democratic Republic of the Congo": "Democratic Republic of Congo",
    "Viet Nam": "Vietnam",
    "Côte d'Ivoire": "Ivory Coast",
    "United Republic of Tanzania": "Tanzania",
    # Add more if needed
}

def clean_and_add_codes(input_csv, output_csv):
    iso_mapping = get_iso_mapping()
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames.copy()
        # Insert 'Code' after 'location' (country name)
        code_index = fieldnames.index('location') + 1
        fieldnames.insert(code_index, 'Code')
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            country = row['location']
            # Standardize country name
            country_std = COUNTRY_REPLACEMENTS.get(country, country)
            row['location'] = country_std
            code = iso_mapping.get(country_std, "")
            row['Code'] = code
            writer.writerow(row)

if __name__ == '__main__':
    clean_and_add_codes(
        'data/GBD_ebola_death_rate.csv',
        'data/GBD_ebola_death_rate_cleaned.csv'
    )
