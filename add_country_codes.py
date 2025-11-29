#!/usr/bin/env python3
"""
Script to add ISO 3-letter country codes to methane-emissions CSV file.
Adds a "Code" column as the second column.
"""

import csv
import os
import shutil

def get_iso_mapping():
    """
    Returns a comprehensive mapping from entity names to ISO 3-letter codes.
    Based on the mapping from FAOstat_clean.py.
    """
    return {
        # Countries with ISO codes
        "Afghanistan": "AFG",
        "Albania": "ALB",
        "Algeria": "DZA",
        "Andorra": "AND",
        "Angola": "AGO",
        "Antigua and Barbuda": "ATG",
        "Argentina": "ARG",
        "Armenia": "ARM",
        "Australia": "AUS",
        "Austria": "AUT",
        "Azerbaijan": "AZE",
        "Bahamas": "BHS",
        "Bahrain": "BHR",
        "Bangladesh": "BGD",
        "Barbados": "BRB",
        "Belarus": "BLR",
        "Belgium": "BEL",
        "Belgium-Luxembourg": "BEL",  # Historical
        "Belize": "BLZ",
        "Benin": "BEN",
        "Bhutan": "BTN",
        "Bolivia": "BOL",
        "Bolivia (Plurinational State of)": "BOL",
        "Bosnia and Herzegovina": "BIH",
        "Botswana": "BWA",
        "Brazil": "BRA",
        "Brunei": "BRN",
        "Brunei Darussalam": "BRN",
        "Bulgaria": "BGR",
        "Burkina Faso": "BFA",
        "Burundi": "BDI",
        "Cabo Verde": "CPV",
        "Cape Verde": "CPV",
        "Cambodia": "KHM",
        "Cameroon": "CMR",
        "Canada": "CAN",
        "Central African Republic": "CAF",
        "Chad": "TCD",
        "Chile": "CHL",
        "China": "CHN",
        "China, Hong Kong SAR": "HKG",
        "China, mainland": "CHN",
        "Colombia": "COL",
        "Comoros": "COM",
        "Congo": "COG",
        "Costa Rica": "CRI",
        "Cote d'Ivoire": "CIV",
        "Côte d'Ivoire": "CIV",
        "Croatia": "HRV",
        "Cuba": "CUB",
        "Cyprus": "CYP",
        "Czech Republic": "CZE",
        "Czechia": "CZE",
        "Czechoslovakia": "CSK",  # Historical
        "Democratic People's Republic of Korea": "PRK",
        "Democratic Republic of the Congo": "COD",
        "Democratic Republic of Congo": "COD",
        "Denmark": "DNK",
        "Djibouti": "DJI",
        "Dominica": "DMA",
        "Dominican Republic": "DOM",
        "Ecuador": "ECU",
        "Egypt": "EGY",
        "El Salvador": "SLV",
        "Equatorial Guinea": "GNQ",
        "Eritrea": "ERI",
        "Estonia": "EST",
        "Eswatini": "SWZ",
        "Ethiopia": "ETH",
        "Fiji": "FJI",
        "Finland": "FIN",
        "France": "FRA",
        "French Polynesia": "PYF",
        "Gabon": "GAB",
        "Gambia": "GMB",
        "Georgia": "GEO",
        "Germany": "DEU",
        "Ghana": "GHA",
        "Greece": "GRC",
        "Grenada": "GRD",
        "Guadeloupe": "GLP",
        "Guatemala": "GTM",
        "Guinea": "GIN",
        "Guinea-Bissau": "GNB",
        "Guyana": "GUY",
        "Haiti": "HTI",
        "Honduras": "HND",
        "Hungary": "HUN",
        "Iceland": "ISL",
        "India": "IND",
        "Indonesia": "IDN",
        "Iran": "IRN",
        "Iran (Islamic Republic of)": "IRN",
        "Iraq": "IRQ",
        "Ireland": "IRL",
        "Israel": "ISR",
        "Italy": "ITA",
        "Jamaica": "JAM",
        "Japan": "JPN",
        "Jordan": "JOR",
        "Kazakhstan": "KAZ",
        "Kenya": "KEN",
        "Kiribati": "KIR",
        "Kuwait": "KWT",
        "Kyrgyzstan": "KGZ",
        "Lao People's Democratic Republic": "LAO",
        "Latvia": "LVA",
        "Lebanon": "LBN",
        "Lesotho": "LSO",
        "Liberia": "LBR",
        "Libya": "LBY",
        "Liechtenstein": "LIE",
        "Lithuania": "LTU",
        "Luxembourg": "LUX",
        "Madagascar": "MDG",
        "Malawi": "MWI",
        "Malaysia": "MYS",
        "Maldives": "MDV",
        "Mali": "MLI",
        "Malta": "MLT",
        "Marshall Islands": "MHL",
        "Martinique": "MTQ",
        "Mauritania": "MRT",
        "Mauritius": "MUS",
        "Mexico": "MEX",
        "Micronesia": "FSM",
        "Monaco": "MCO",
        "Mongolia": "MNG",
        "Montenegro": "MNE",
        "Morocco": "MAR",
        "Mozambique": "MOZ",
        "Myanmar": "MMR",
        "Namibia": "NAM",
        "Nauru": "NRU",
        "Nepal": "NPL",
        "Netherlands": "NLD",
        "Netherlands (Kingdom of the)": "NLD",
        "New Zealand": "NZL",
        "Nicaragua": "NIC",
        "Niger": "NER",
        "Nigeria": "NGA",
        "North Korea": "PRK",
        "North Macedonia": "MKD",
        "Norway": "NOR",
        "Oman": "OMN",
        "Pakistan": "PAK",
        "Palau": "PLW",
        "Palestine": "PSE",
        "Panama": "PAN",
        "Papua New Guinea": "PNG",
        "Paraguay": "PRY",
        "Peru": "PER",
        "Philippines": "PHL",
        "Poland": "POL",
        "Portugal": "PRT",
        "Puerto Rico": "PRI",
        "Qatar": "QAT",
        "Republic of Korea": "KOR",
        "South Korea": "KOR",
        "Republic of Moldova": "MDA",
        "Moldova": "MDA",
        "Réunion": "REU",
        "Reunion": "REU",
        "Romania": "ROU",
        "Russia": "RUS",
        "Russian Federation": "RUS",
        "Rwanda": "RWA",
        "Saint Kitts and Nevis": "KNA",
        "Saint Lucia": "LCA",
        "Saint Vincent and the Grenadines": "VCT",
        "Samoa": "WSM",
        "San Marino": "SMR",
        "Sao Tome and Principe": "STP",
        "Saudi Arabia": "SAU",
        "Senegal": "SEN",
        "Serbia": "SRB",
        "Serbia and Montenegro": "SCG",  # Historical
        "Seychelles": "SYC",
        "Sierra Leone": "SLE",
        "Singapore": "SGP",
        "Slovakia": "SVK",
        "Slovenia": "SVN",
        "Solomon Islands": "SLB",
        "Somalia": "SOM",
        "South Africa": "ZAF",
        "South Sudan": "SSD",
        "Spain": "ESP",
        "Sri Lanka": "LKA",
        "Sudan": "SDN",
        "Sudan (former)": "SDN",
        "Suriname": "SUR",
        "Sweden": "SWE",
        "Switzerland": "CHE",
        "Syria": "SYR",
        "Syrian Arab Republic": "SYR",
        "Tajikistan": "TJK",
        "Tanzania": "TZA",
        "Thailand": "THA",
        "Timor-Leste": "TLS",
        "Togo": "TGO",
        "Tonga": "TON",
        "Trinidad and Tobago": "TTO",
        "Tunisia": "TUN",
        "Turkey": "TUR",
        "Türkiye": "TUR",
        "Turkmenistan": "TKM",
        "Tuvalu": "TUV",
        "Uganda": "UGA",
        "Ukraine": "UKR",
        "United Arab Emirates": "ARE",
        "United Kingdom": "GBR",
        "United States": "USA",
        "United States of America": "USA",
        "Uruguay": "URY",
        "USSR": "SUN",  # Historical
        "Uzbekistan": "UZB",
        "Vanuatu": "VUT",
        "Venezuela": "VEN",
        "Venezuela (Bolivarian Republic of)": "VEN",
        "Vietnam": "VNM",
        "Yemen": "YEM",
        "Yugoslavia": "YUG",  # Historical
        "Zambia": "ZMB",
        "Zimbabwe": "ZWE",
        
        # Regions and continents (empty codes - will be filtered out)
        "Africa": "",
        "Americas": "",
        "Asia": "",
        "Australia and New Zealand": "",
        "Caribbean": "",
        "Central America": "",
        "Central Asia": "",
        "Eastern Africa": "",
        "Eastern Asia": "",
        "Eastern Europe": "",
        "Europe": "",
        "European Union": "",
        "European Union (27)": "",
        "Land Locked Developing Countries": "",
        "Least Developed Countries": "",
        "Low Income Food Deficit Countries": "",
        "Melanesia": "",
        "Middle Africa": "",
        "Net Food Importing Developing Countries": "",
        "Northern Africa": "",
        "Northern America": "",
        "Northern Europe": "",
        "Oceania": "",
        "Other non-specified areas": "",
        "Polynesia": "",
        "Small Island Developing States": "",
        "South America": "",
        "South-eastern Asia": "",
        "Southern Africa": "",
        "Southern Asia": "",
        "Southern Europe": "",
        "Western Africa": "",
        "Western Asia": "",
        "Western Europe": "",
        "World": "",
    }

def add_country_codes(input_file):
    """
    Add ISO 3-letter country codes to the CSV file as the second column.
    """
    # Create backup
    backup_file = input_file.replace('.csv', '_backup.csv')
    shutil.copy2(input_file, backup_file)
    print(f"✓ Backup created: {backup_file}")
    
    # Load ISO mapping
    iso_mapping = get_iso_mapping()
    
    # Process the file
    rows_processed = 0
    countries_found = 0
    regions_removed = 0
    
    # Read original data
    data_rows = []
    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        for row in reader:
            if len(row) < 3:
                continue
                
            entity = row[0]
            year = row[1]
            value = row[2]
            
            # Get ISO code
            iso_code = iso_mapping.get(entity, "")
            
            if iso_code:  # Only keep rows with valid ISO codes (actual countries)
                data_rows.append([entity, iso_code, year, value])
                countries_found += 1
            else:
                regions_removed += 1
            
            rows_processed += 1
    
    # Write the modified file
    with open(input_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Write header with Code column as second column
        writer.writerow(['Entity', 'Code', 'Year', 'Methane emissions from all sectors'])
        
        # Write all data rows
        for row in data_rows:
            writer.writerow(row)
    
    print(f"✓ Processing complete!")
    print(f"  Total rows processed: {rows_processed}")
    print(f"  Countries kept: {countries_found}")
    print(f"  Regions/aggregates removed: {regions_removed}")
    print(f"  Final rows (including header): {len(data_rows) + 1}")

def main():
    """
    Main function to process the methane emissions file.
    """
    file_path = "/Users/rivaue01/Documents/perso/chartle-data/data/methane-emissions-from-all-sectors.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    
    print(f"Adding country codes to: {file_path}")
    add_country_codes(file_path)
    print("✓ Done! ISO 3-letter codes added as second column.")
    print("  Regional aggregates (World, Africa, etc.) have been removed.")

if __name__ == "__main__":
    main()