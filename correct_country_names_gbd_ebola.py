import csv

# Country name replacements for standardization
COUNTRY_REPLACEMENTS = {
    "Côte d'Ivoire": "Ivory Coast",
    "Viet Nam": "Vietnam",
    "Democratic Republic of the Congo": "Democratic Republic of Congo",
    "United Republic of Tanzania": "Tanzania",
    "Türkiye": "Turkey",
    "Bolivia (Plurinational State of)": "Bolivia",
    "Iran (Islamic Republic of)": "Iran",
    "Lao People's Democratic Republic": "Laos",
    "Republic of Moldova": "Moldova",
    "Russian Federation": "Russia",
    "Syrian Arab Republic": "Syria",
    "Democratic People's Republic of Korea": "North Korea",
    "Republic of Korea": "South Korea",
    "United States of America": "United States",
    "Venezuela (Bolivarian Republic of)": "Venezuela",
    # Add more as needed
}

def correct_country_names(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            country = row['location']
            row['location'] = COUNTRY_REPLACEMENTS.get(country, country)
            writer.writerow(row)

if __name__ == '__main__':
    correct_country_names(
        'data/GBD_ebola_death_rate_with_codes.csv',
        'data/GBD_ebola_death_rate_with_codes_corrected.csv'
    )
