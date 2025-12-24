#!/usr/bin/env python3
"""
KITTI Dataset Download Helper
Downloads a small sample of KITTI data for testing the converter.

Note: For full KITTI dataset, visit: http://www.cvlibs.net/datasets/kitti/
This script downloads a minimal sample for demo purposes.
"""

import argparse
import os
import requests
import zipfile
from pathlib import Path
from typing import Optional


def download_file(url: str, output_path: Path, chunk_size: int = 8192):
    """Download a file with progress indication."""
    print(f"Downloading {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    downloaded = 0
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)
    
    print(f"\n✓ Downloaded to {output_path}")


def extract_zip(zip_path: Path, extract_to: Path):
    """Extract zip file."""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✓ Extracted to {extract_to}")


def setup_kitti_sample(output_dir: Path, num_frames: int = 10):
    """
    Set up a minimal KITTI sample structure.
    
    This creates the directory structure and provides instructions
    for downloading actual KITTI data.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    velodyne_dir = output_dir / "velodyne"
    image_dir = output_dir / "image_2"
    
    velodyne_dir.mkdir(exist_ok=True)
    image_dir.mkdir(exist_ok=True)
    
    print(f"""
✓ Created KITTI directory structure at: {output_dir}

To download KITTI data:
1. Visit: http://www.cvlibs.net/datasets/kitti/raw_data.php
2. Download a small sequence (e.g., "2011_09_26_drive_0001")
3. Extract and copy:
   - velodyne_points/data/*.bin → {velodyne_dir}/
   - image_02/data/*.png → {image_dir}/

Or use the KITTI raw data downloader:
   wget http://www.cvlibs.net/download.php?file=raw_data_downloader.zip
   
For a quick test, you can manually download a few frames from:
   http://www.cvlibs.net/datasets/kitti/raw_data.php
""")


def main():
    parser = argparse.ArgumentParser(
        description="Set up KITTI dataset directory structure"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="sample-data/kitti",
        help="Output directory for KITTI data (default: sample-data/kitti)",
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    setup_kitti_sample(output_dir)
    
    print("\nNote: This script only creates the directory structure.")
    print("You'll need to download actual KITTI data from the official website.")
    print("See instructions above for details.")


if __name__ == "__main__":
    main()

