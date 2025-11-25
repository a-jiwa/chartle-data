# FAOstat_clean.py - Automated FAOstat Dataset Cleaner

This script automatically cleans and standardizes FAOstat datasets to match your project's format.

## What it does:

1. **Adds ISO 3-letter country codes** in a new `CODE` column
2. **Removes all regions/continents** (keeps only actual countries)
3. **Reorders data chronologically** (oldest to newest year for each country)
4. **Standardizes country names** to match your banana production dataset
5. **Filters to "Production" data only** (if Element column exists)
6. **Removes unnecessary columns** (Unit, Value Footnotes, etc.)
7. **Standardizes column names** to: `Entity, CODE, Year, Value`

## Usage:

```bash
# From the main directory:
python3 FAOstat_clean.py <filename>

# Examples:
python3 FAOstat_clean.py Turkey_production_FAOstat.csv
python3 FAOstat_clean.py data/Rice_production_FAOstat.csv
python3 FAOstat_clean.py /path/to/Wheat_production_FAOstat.csv
```

## Input file requirements:

- CSV format with headers
- Must have columns for: Country/Entity, Year, and Value
- Can have additional columns (Element, Unit, Value Footnotes) - they'll be handled appropriately

## Output:

- **Backup created**: Original file is saved as `*_original_backup.csv`
- **Standardized format**: `Entity,CODE,Year,Value`
- **Clean data**: Only countries, chronologically ordered, standardized names

## Example transformation:

**Before:**
```csv
"Country or Area","Element","Year","Unit","Value","Value Footnotes"
"Africa","Production","2021","t","43944.00",""
"United States of America","Production","2021","t","678207.00",""
```

**After:**
```csv
Entity,CODE,Year,Value
United States,USA,1961,678207.00
United States,USA,1962,654321.00
```

## Features:

- ✅ **Smart detection** of file structure
- ✅ **Comprehensive country mapping** (200+ countries/territories)
- ✅ **Region filtering** (automatically removes 50+ regional groupings)
- ✅ **Name standardization** (matches your existing datasets)
- ✅ **Chronological sorting** (oldest to newest within each country)
- ✅ **Error handling** with informative messages
- ✅ **Automatic backup** (never lose your original data)

## Supported datasets:

Works with any FAOstat export containing production, trade, or other country-level data.