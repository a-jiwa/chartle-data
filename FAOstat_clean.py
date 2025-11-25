#!/usr/bin/env python3
"""
FAOstat_clean.py - Comprehensive script to clean FAOstat datasets

This script applies the following transformations:
1. Adds ISO 3-letter country codes
2. Removes all regions/continents (keeps only countries)
3. Reorders data chronologically (oldest to newest year)
4. Standardizes country names to match banana production dataset
5. Filters to keep only "Production" element (if applicable)
6. Removes unnecessary columns (Unit, Value Footnotes, etc.)
7. Standardizes column names to: Entity, CODE, Year, Value

Usage:
    python3 FAOstat_clean.py <filename>
    
Example:
    python3 FAOstat_clean.py Turkey_production_FAOstat.csv
"""

import csv
import os
import sys
from collections import defaultdict

def get_iso_mapping():
    """
    Returns a comprehensive mapping from entity names to ISO 3-letter codes.
    """
    return {
        # Countries with ISO codes
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
        
        # Regions and continents (empty codes - will be removed)
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

def load_banana_country_mapping(data_dir):
    """
    Load standardized country names from banana file if available.
    """
    banana_file = os.path.join(data_dir, "banana-production.csv")
    iso_to_name = {}
    
    if os.path.exists(banana_file):
        try:
            with open(banana_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Skip header
                
                for row in reader:
                    if len(row) >= 2:
                        entity_name = row[0]
                        iso_code = row[1]
                        
                        # Skip regions/continents
                        if (iso_code and len(iso_code) == 3 and iso_code.isupper() and 
                            not any(region in entity_name for region in [
                                'Africa', 'Europe', 'World', 'Americas', 'Asia', 'Oceania',
                                'Caribbean', 'Central', 'Eastern', 'Northern', 'Southern', 
                                'Western', 'Melanesia', 'Polynesia', 'Micronesia', 'Union',
                                'Developed', 'Developing', 'Income', 'Island'
                            ])):
                            iso_to_name[iso_code] = entity_name
        except Exception as e:
            print(f"Warning: Could not load banana mapping: {e}")
    
    return iso_to_name

def detect_file_structure(file_path):
    """
    Detect the structure of the input file to determine processing approach.
    """
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Check a few rows to understand structure
        sample_rows = []
        for i, row in enumerate(reader):
            sample_rows.append(row)
            if i >= 5:  # Just check first few rows
                break
    
    structure = {
        'header': header,
        'has_element': 'Element' in header or any('Element' in col for col in header),
        'has_unit': 'Unit' in header,
        'has_footnotes': any('footnote' in col.lower() for col in header),
        'entity_col': 0,  # Assume first column is entity
        'year_col': None,
        'value_col': None
    }
    
    # Find year and value columns
    for i, col in enumerate(header):
        if 'year' in col.lower():
            structure['year_col'] = i
        elif 'value' in col.lower() and 'footnote' not in col.lower():
            structure['value_col'] = i
    
    return structure

def clean_faostat_dataset(file_path):
    """
    Main cleaning function that processes any FAOstat dataset.
    """
    print(f"Cleaning FAOstat dataset: {file_path}")
    
    # Create backup
    backup_path = file_path.replace('.csv', '_original_backup.csv')
    import shutil
    shutil.copy2(file_path, backup_path)
    print(f"✓ Backup created: {backup_path}")
    
    # Detect file structure
    structure = detect_file_structure(file_path)
    print(f"✓ File structure detected")
    
    # Load mappings
    data_dir = os.path.dirname(file_path)
    iso_mapping = get_iso_mapping()
    banana_mapping = load_banana_country_mapping(data_dir)
    print(f"✓ Country mappings loaded ({len(banana_mapping)} from banana dataset)")
    
    # Process data
    country_data = defaultdict(list)
    rows_processed = 0
    rows_removed = 0
    countries_found = set()
    
    with open(file_path, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        for row in reader:
            rows_processed += 1
            
            if len(row) < 3:
                rows_removed += 1
                continue
            
            # Extract entity and year
            entity = row[structure['entity_col']].strip('"')
            
            # Find year
            year_str = None
            if structure['year_col'] is not None:
                year_str = row[structure['year_col']].strip('"')
            else:
                # Try to find year in any column
                for cell in row:
                    try:
                        year_val = int(cell.strip('"'))
                        if 1900 <= year_val <= 2030:  # Reasonable year range
                            year_str = str(year_val)
                            break
                    except ValueError:
                        continue
            
            if not year_str:
                rows_removed += 1
                continue
            
            try:
                year = int(year_str)
            except ValueError:
                rows_removed += 1
                continue
            
            # Check if this row should be kept based on element (if present)
            if structure['has_element']:
                element_col = None
                for i, col in enumerate(header):
                    if 'element' in col.lower():
                        element_col = i
                        break
                
                if element_col is not None and len(row) > element_col:
                    element = row[element_col].strip('"')
                    if element != "Production":
                        rows_removed += 1
                        continue
            
            # Get ISO code
            iso_code = iso_mapping.get(entity, "")
            
            # Only keep rows with ISO codes (actual countries)
            if iso_code:
                # Standardize country name using banana mapping if available
                if iso_code in banana_mapping:
                    entity = banana_mapping[iso_code]
                
                # Find value column
                value = ""
                if structure['value_col'] is not None:
                    value = row[structure['value_col']].strip('"')
                else:
                    # Try to find a numeric value in the row
                    for cell in row:
                        try:
                            float(cell.strip('"'))
                            value = cell.strip('"')
                            break
                        except ValueError:
                            continue
                
                # Store data for sorting
                new_row = [entity, iso_code, str(year), value]
                country_data[entity].append((year, new_row))
                countries_found.add(entity)
            else:
                rows_removed += 1
    
    print(f"✓ Data processed: {rows_processed} rows, {rows_removed} removed, {len(countries_found)} countries found")
    
    # Sort data chronologically for each country
    for entity in country_data:
        country_data[entity].sort(key=lambda x: x[0])  # Sort by year
    
    # Write cleaned data
    with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        
        # Write standard header
        writer.writerow(['Entity', 'CODE', 'Year', 'Value'])
        
        # Write data for each country in alphabetical order
        for entity in sorted(country_data.keys()):
            for year, row in country_data[entity]:
                writer.writerow(row)
    
    total_final_rows = sum(len(data) for data in country_data.values())
    print(f"✓ Dataset cleaned successfully!")
    print(f"  Final rows: {total_final_rows + 1} (including header)")
    print(f"  Countries: {len(countries_found)}")
    
    # Show sample year ranges
    if countries_found:
        print(f"  Sample countries and year ranges:")
        for entity in sorted(list(countries_found)[:5]):  # First 5 countries
            years = [year for year, row in country_data[entity]]
            if years:
                print(f"    {entity}: {min(years)}-{max(years)} ({len(years)} years)")

def main():
    """
    Main function to handle command line arguments.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 FAOstat_clean.py <filename>")
        print("Example: python3 FAOstat_clean.py Turkey_production_FAOstat.csv")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Handle both absolute and relative paths
    if not os.path.isabs(filename):
        # Assume file is in current directory or data/ subdirectory
        if os.path.exists(filename):
            file_path = filename
        elif os.path.exists(os.path.join('data', filename)):
            file_path = os.path.join('data', filename)
        else:
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
    else:
        file_path = filename
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)
    
    try:
        clean_faostat_dataset(file_path)
        print(f"\n🎉 Success! '{file_path}' has been cleaned and standardized.")
        print("   The file now has the format: Entity, CODE, Year, Value")
        print("   ✓ Only countries (no regions/continents)")
        print("   ✓ Chronologically ordered (oldest to newest)")
        print("   ✓ Standardized country names")
        print("   ✓ ISO 3-letter codes added")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()