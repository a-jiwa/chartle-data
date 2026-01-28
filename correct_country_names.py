import csv

# Mapping of incorrect to correct country names based on the provided list
COUNTRY_REPLACEMENTS = {
    'Democratic Republic of the Congo': 'Democratic Republic of Congo',
    'Türkiye': 'Turkey',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Iran (Islamic Republic of)': 'Iran',
    'Lao People\'s Democratic Republic': 'Laos',
    'Republic of Moldova': 'Moldova',
    'Russian Federation': 'Russia',
    'Syrian Arab Republic': 'Syria',
    'Democratic People\'s Republic of Korea': 'North Korea',
    'Republic of Korea': 'South Korea',
    'United States of America': 'United States',
    'Côte d\'Ivoire': 'Ivory Coast',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Viet Nam': 'Vietnam',
}

def correct_country_names(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            country = row[0]
            if country in COUNTRY_REPLACEMENTS:
                row[0] = COUNTRY_REPLACEMENTS[country]
            writer.writerow(row)

if __name__ == '__main__':
    correct_country_names(
        'data/GBD_breast_cancer_death_rate2.csv',
        'data/GBD_breast_cancer_death_rate2_corrected.csv'
    )
