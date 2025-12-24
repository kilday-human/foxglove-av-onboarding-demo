# KITTI to MCAP Converter

Convert KITTI autonomous driving dataset to MCAP format for visualization in Foxglove Studio.

## Overview

This pipeline converts KITTI dataset (LiDAR point clouds + camera images) into a unified MCAP file that can be opened directly in Foxglove Studio. This demonstrates the shift from fragmented workflows (days of manual data processing) to unified debugging (minutes in Foxglove).

## Prerequisites

- Python 3.8 or higher
- KITTI dataset (see download instructions below)

## Setup

### 1. Create Virtual Environment

```bash
cd data-pipeline
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Download KITTI Data

You have two options:

#### Option A: Manual Download (Recommended for testing)

1. Visit the [KITTI Raw Data](http://www.cvlibs.net/datasets/kitti/raw_data.php) website
2. Download a small sequence (e.g., `2011_09_26_drive_0001_sync`)
3. Extract the data - the KITTI structure already has the correct directories:

```
your-kitti-dir/
├── velodyne_points/
│   └── data/     # LiDAR .bin files (e.g., 000000.bin, 000001.bin, ...)
└── image_02/
    └── data/     # Camera .png files (e.g., 000000.png, 000001.png, ...)
```

**Quick setup helper:**
```bash
python download_kitti.py --output_dir sample-data/kitti
```

This creates the directory structure and provides detailed download instructions.

#### Option B: Use KITTI Raw Data Downloader

```bash
wget http://www.cvlibs.net/download.php?file=raw_data_downloader.zip
unzip raw_data_downloader.zip
python download_raw_data.py 2011_09_26 0001
```

Then organize the files as described above.

## Usage

### Basic Conversion

```bash
python kitti_to_mcap.py --kitti_dir /path/to/kitti --output kitti_data.mcap
```

### Options

- `--kitti_dir`: Path to KITTI directory (must contain `velodyne_points/data/` and `image_02/data/` subdirectories)
- `--output`: Output MCAP file path (default: `kitti_data.mcap`)
- `--frame_rate`: Playback frame rate in Hz (default: 10.0)

### Example

```bash
# Convert with default settings
python kitti_to_mcap.py --kitti_dir sample-data/kitti --output demo.mcap

# Convert with custom frame rate
python kitti_to_mcap.py --kitti_dir sample-data/kitti --output demo.mcap --frame_rate 5.0
```

## Output

The script generates an MCAP file with:
- **LiDAR data**: Published on `/velodyne_points` topic as `foxglove.PointCloud`
- **Camera data**: Published on `/camera/image_raw` topic as `foxglove.CompressedImage`
- **Synchronized timestamps**: Both sensors are time-aligned for synchronized playback

## Viewing in Foxglove Studio

1. Open [Foxglove Studio](https://studio.foxglove.dev/) (web or desktop app)
2. Click "Open file" and select your `.mcap` file
3. The data will load with synchronized LiDAR and camera streams

### Recommended Layout

For the best visualization experience, create a layout with:
- **3D View**: Display `/velodyne_points` point cloud
- **Image View**: Display `/camera/image_raw` camera feed
- **Timeline**: Navigate through the synchronized data

You can save and reuse layouts in the `foxglove-layouts/` directory.

## Expected Output

When successful, you should see:
```
Found 100 frames to convert
Processed 10/100 frames...
Processed 20/100 frames...
...
Successfully converted 100 frames to kitti_data.mcap

✓ Conversion complete! Open kitti_data.mcap in Foxglove Studio
```

## Troubleshooting

### "LiDAR directory not found" or "Camera directory not found"
- Ensure your KITTI directory has `velodyne_points/data/` and `image_02/data/` subdirectories
- Check that the paths are correct (use absolute paths if needed)

### "No matching LiDAR and camera frames found"
- Ensure frame IDs match between LiDAR and camera files (e.g., `000000.bin` and `000000.png`)
- Check that files are named consistently (zero-padded numbers)

### Import errors
- Make sure you've activated your virtual environment
- Run `pip install -r requirements.txt` again to ensure all dependencies are installed

### MCAP file doesn't open in Foxglove
- Check that the file was created successfully (file size > 0)
- Try opening in Foxglove Studio web version: https://studio.foxglove.dev/
- Check the console output for any error messages during conversion

## File Structure

```
data-pipeline/
├── requirements.txt          # Python dependencies
├── kitti_to_mcap.py         # Main converter script
├── download_kitti.py        # Helper script for setup
└── README.md                # This file
```

## Next Steps

After converting your data:
1. Open the MCAP file in Foxglove Studio
2. Create a custom layout with 3D + Image + Timeline views
3. Save the layout to `foxglove-layouts/` for reuse
4. Share the MCAP file and layout with your team for unified debugging

## References

- [Foxglove SDK Tutorial](https://foxglove.dev/blog/using-the-foxglove-sdk-to-generate-mcap)
- [KITTI Dataset](http://www.cvlibs.net/datasets/kitti/)
- [Foxglove Studio Documentation](https://docs.foxglove.dev/)

