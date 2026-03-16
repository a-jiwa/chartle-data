#!/usr/bin/env python3
"""
Simple script to fetch CSV data from Google Sheets and save it locally.
Also fetches all data from OWID_datalink column.
"""

import urllib.request
import csv
import sys
import os
import re
import time
from urllib.parse import urlparse

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ1ZutdIgCWij_xYeMYn5ye-ZtjgxtEBX_1Ic76F8bBwf027nMvXHYRbOTMDyz5ZpX-znTd2urlI_fK/pub?gid=1891885088&single=true&output=csv"
OUTPUT_FILE = "data.csv"
BACKUP_DIR = "backup"
MAPPING_FILE = "backup_mapping.csv"

def extract_filename_from_owid_url(url):
    """Extract filename from OWID URL.
    
    Example: https://ourworldindata.org/grapher/deaths-in-armed-conflicts-by-country.csv?v=1&...
    Example: https://ourworldindata.org/explorers/conflict-data.csv?v=1&...
    Example: https://raw.githubusercontent.com/.../data/years-of-schooling.csv
    Returns: (filename, extraction_method) where extraction_method is:
        - 'regex' if extracted using regex pattern
        - 'path' if extracted from URL path
        - 'fallback' if had to use hash-based fallback
    """
    # Pattern: /grapher/{filename}.csv?{query}
    match = re.search(r'/grapher/([^/?]+\.csv)', url)
    if match:
        return match.group(1), 'regex'
    
    # Pattern: /explorers/{filename}.csv?{query}
    match = re.search(r'/explorers/([^/?]+\.csv)', url)
    if match:
        return match.group(1), 'regex'
    
    # Pattern: GitHub raw URLs - /data/{filename}.csv
    match = re.search(r'/data/([^/?]+\.csv)', url)
    if match:
        return match.group(1), 'regex'
    
    # Fallback: try to extract from path
    parsed = urlparse(url)
    path = parsed.path
    if '/grapher/' in path:
        filename = path.split('/grapher/')[-1]
        if filename:
            return filename, 'path'
    elif '/explorers/' in path:
        filename = path.split('/explorers/')[-1]
        if filename:
            return filename, 'path'
    elif '/data/' in path:
        filename = path.split('/data/')[-1]
        if filename:
            return filename, 'path'
    
    # Last resort: use a hash or index
    return f"data_{hash(url) % 10000}.csv", 'fallback'

def fetch_and_save_csv():
    """Fetch CSV from URL and save to local file."""
    try:
        print(f"Fetching data from: {CSV_URL}")
        urllib.request.urlretrieve(CSV_URL, OUTPUT_FILE)
        print(f"Data successfully saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)

def fetch_owid_data():
    """Fetch all data from OWID_datalink column."""
    if not os.path.exists(OUTPUT_FILE):
        print(f"Error: {OUTPUT_FILE} not found. Please run the main fetch first.", file=sys.stderr)
        sys.exit(1)
    
    # Create backup directory for OWID data files
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            print("No data found in CSV file.")
            return [], [], [], []
        
        # Check if OWID_datalink column exists
        if 'OWID_datalink' not in rows[0]:
            print("Warning: OWID_datalink column not found in CSV.")
            return [], [], [], []
        
        # Fetch each OWID data link
        successful = []
        failed = []
        skipped = []
        correctly_extracted = []
        fallback_extracted = []
        
        rows_with_links = [row for row in rows if row.get('OWID_datalink', '').strip()]
        total_links = len(rows_with_links)
        
        print(f"\nFound {total_links} OWID data links to fetch.\n")
        
        for idx, row in enumerate(rows_with_links, 1):
            owid_link = row.get('OWID_datalink', '').strip()
            
            # Extract filename from URL
            filename, extraction_method = extract_filename_from_owid_url(owid_link)
            filepath = os.path.join(BACKUP_DIR, filename)
            
            # Get title for display purposes
            title = row.get('title', '').strip() or f"Row {idx}"
            date = row.get('date', '').strip() or 'N/A'
            
            # Determine extraction status message
            if extraction_method == 'regex':
                extraction_status = "✓ Correctly extracted"
                correctly_extracted.append(filename)
            elif extraction_method == 'path':
                extraction_status = "⚠ Extracted from path (fallback)"
                fallback_extracted.append(filename)
            else:
                extraction_status = "✗ Used hash fallback (URL pattern not recognized)"
                fallback_extracted.append(filename)
            
            print(f"[{idx}/{total_links}] Processing: {title} ({date})")
            print(f"  URL: {owid_link}")
            print(f"  Filename: {filename}")
            print(f"  Extraction: {extraction_status}")
            
            # Check if file already exists
            if os.path.exists(filepath):
                print(f"  ⊘ SKIPPED - File already exists: {filepath}\n")
                skipped.append({
                    'title': title,
                    'date': date,
                    'filename': filename,
                    'url': owid_link,
                    'extraction_method': extraction_method
                })
                continue
            
            try:
                urllib.request.urlretrieve(owid_link, filepath)
                print(f"  ✓ SUCCESS - Saved to {filepath}\n")
                successful.append({
                    'title': title,
                    'date': date,
                    'filename': filename,
                    'url': owid_link,
                    'extraction_method': extraction_method
                })
                # Add delay to avoid rate limiting (1.5 seconds between requests)
                time.sleep(1.5)
            except Exception as e:
                error_msg = str(e)
                print(f"  ✗ FAILED - Error: {error_msg}\n")
                failed.append({
                    'title': title,
                    'date': date,
                    'filename': filename,
                    'url': owid_link,
                    'error': error_msg,
                    'extraction_method': extraction_method
                })
                # Still add delay even on failure to avoid hammering the server
                time.sleep(1.5)
        
        # Print summary
        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Total links processed: {total_links}")
        print(f"✓ Successful: {len(successful)}")
        print(f"⊘ Skipped (already exists): {len(skipped)}")
        print(f"✗ Failed: {len(failed)}")
        
        # Filename extraction summary
        correctly_count = len(correctly_extracted)
        fallback_count = len(fallback_extracted)
        print(f"\nFilename Extraction:")
        print(f"  ✓ Correctly extracted from URL: {correctly_count}")
        print(f"  ⚠ Used fallback method: {fallback_count}")
        
        if successful:
            print(f"\n✓ Successfully downloaded files ({len(successful)}):")
            for item in successful:
                method_indicator = "✓" if item['extraction_method'] == 'regex' else "⚠"
                print(f"  {method_indicator} {item['filename']} ({item['title']})")
        
        if skipped:
            print(f"\n⊘ Skipped files (already exist) ({len(skipped)}):")
            for item in skipped:
                method_indicator = "✓" if item['extraction_method'] == 'regex' else "⚠"
                print(f"  {method_indicator} {item['filename']} ({item['title']})")
        
        if failed:
            print(f"\n✗ Failed downloads ({len(failed)}):")
            for item in failed:
                method_indicator = "✓" if item['extraction_method'] == 'regex' else "⚠"
                print(f"  {method_indicator} {item['filename']} ({item['title']})")
                print(f"    Error: {item['error']}")
                print(f"    URL: {item['url']}")
        
        # Show correctly extracted filenames (unique)
        unique_correctly_extracted = sorted(set(correctly_extracted))
        if unique_correctly_extracted:
            print(f"\n✓ Correctly extracted filenames ({len(unique_correctly_extracted)} unique):")
            for filename in unique_correctly_extracted:
                print(f"  - {filename}")
        
        # Show fallback filenames (unique)
        unique_fallback_extracted = sorted(set(fallback_extracted))
        if unique_fallback_extracted:
            print(f"\n⚠ Fallback filenames ({len(unique_fallback_extracted)} unique):")
            for filename in unique_fallback_extracted:
                print(f"  - {filename}")
        
        print(f"\nAll files saved to: {BACKUP_DIR}/")
        
        # Return data for mapping CSV
        return rows_with_links, successful, failed, skipped
        
    except Exception as e:
        print(f"Error processing OWID data: {e}", file=sys.stderr)
        sys.exit(1)

def create_mapping_csv(rows_with_links):
    """Create a CSV mapping date, title, and backup link."""
    try:
        print(f"\nCreating mapping CSV: {MAPPING_FILE}")
        
        with open(MAPPING_FILE, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['date', 'title', 'backup_link', 'filename', 'status']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in rows_with_links:
                owid_link = row.get('OWID_datalink', '').strip()
                if not owid_link:
                    continue
                
                filename, _ = extract_filename_from_owid_url(owid_link)
                filepath = os.path.join(BACKUP_DIR, filename)
                
                # Determine status
                if os.path.exists(filepath):
                    status = 'downloaded'
                else:
                    status = 'missing'
                
                writer.writerow({
                    'date': row.get('date', '').strip(),
                    'title': row.get('title', '').strip(),
                    'backup_link': owid_link,
                    'filename': filename,
                    'status': status
                })
        
        print(f"Mapping CSV created: {MAPPING_FILE}")
        
    except Exception as e:
        print(f"Error creating mapping CSV: {e}", file=sys.stderr)

if __name__ == "__main__":
    fetch_and_save_csv()
    print()
    rows_with_links, successful, failed, skipped = fetch_owid_data()
    create_mapping_csv(rows_with_links)
    
    # Re-run fetch for missing files
    print("\n" + "=" * 70)
    print("RE-RUNNING FETCH FOR MISSING FILES")
    print("=" * 70)
    print()
    fetch_owid_data()
