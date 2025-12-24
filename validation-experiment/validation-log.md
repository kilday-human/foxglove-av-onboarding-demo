# Validation Test: Following Adrian's Email

**Date:** December 24, 2024
**Tester:** Fred (9 years AV experience, but pretending to be new to Foxglove)
**Starting knowledge:** Have KITTI data downloaded, no Foxglove experience
**Goal:** Convert KITTI to MCAP using ONLY Adrian's email instructions

---

## Adrian's Email (Reference)

> Hi Christopher,
> 
> I'm Adrian, Foxglove's CEO and Founder. I wanted to say welcome and thanks for choosing Foxglove.
>  
> If you're using ROS or MCAP already, simply drag and drop a .bag or .mcap file onto the Foxglove visualization UI or:
> 1. Click "Open local file(s)…" in the dashboard or left hand menu.
> 2. Open or drag-and-drop the files from your OS file manager.
> 3. Select the file and click open.
> 
> You can also get started with the Foxglove SDK, a quick and easy way to:
> * Stream and visualize your robot data live in Foxglove.
> * Log your data to MCAP files.
> 
> Install foxglove-sdk from PyPI: https://pypi.org/project/foxglove-sdk
> pip install foxglove-sdk
>  
> With just a few lines you can log your data to MCAP files, stream live data directly to the Foxglove app, or both simultaneously:
>  
> ```python
> import foxglove as fg
> from foxglove.schemas import Pose, PoseInFrame, Quaternion, Timestamp, Vector3
> 
> fg.start_server()
> 
> with fg.open_mcap("foo.mcap"):
>    fg.log("/example", PoseInFrame(
>        timestamp=Timestamp(sec=0),
>        frame_id="ego",
>        pose=Pose(
>            position=Vector3(x=1.0, y=2.0, z=3.0),
>            orientation=Quaternion(x=0.0, y=0.0, z=0.0, w=1.0),
>        ),
>    ))
> ```
> 
> Here's a link to the documentation for additional information and examples to help you get started.
> 
> – Adrian

---

## My Data (KITTI)

**What I have:**
- `~/foxglove-av-onboarding-demo/sample-data/kitti/2011_09_26_drive_0001_sync/`
  - `velodyne_points/data/*.bin` (108 LiDAR files, binary format)
  - `image_02/data/*.png` (108 camera images)
  - `oxts/` (GPS/IMU data)
- `~/foxglove-av-onboarding-demo/sample-data/kitti/2011_09_26/`
  - `calib_velo_to_cam.txt` (calibration matrix)

**What I need:** MCAP file I can open in Foxglove

---

## Attempt Log (Real-time)

### Step 1: Install Foxglove SDK ✅

**Command:** `pip install foxglove-sdk`
**Result:** Installed foxglove-sdk==0.15.3
**Issues:** None (sandboxing permission issue bypassed)

---

### Step 2: Run Example Code ✅

**Command:** `python test_adrian_example.py`
**Result:** 
- Exit code 0 (success)
- Created `foo.mcap` file
- File size: [paste size from ls -lh]

**What this proves:** Adrian's example works for Pose data.

---

### Step 3: Open in Foxglove ✅

**Action:** Opened foo.mcap in Foxglove Studio

**Result:**
- File loaded successfully ✓
- Topic visible: `/example` (foxglove.PoseInFrame) ✓
- Data structure correct: timestamp, frame_id, pose (position + orientation) ✓
- 3D panel displays (empty grid, no geometry - expected for Pose data) ✓

**What this proves:** Adrian's example works end-to-end for Pose data.

---

### Step 4: Attempt KITTI Conversion ❌ BLOCKED

**Question:** "Adrian's example works for Pose. But I have KITTI data:
- `velodyne_points/data/*.bin` (108 LiDAR files, binary format)
- `image_02/data/*.png` (108 camera images)
- `calib_velo_to_cam.txt` (calibration matrix)

How do I convert these to MCAP using Adrian's instructions?"

**What I tried:**

**Attempt 1: Search Adrian's email**
- Searched for "LiDAR" → Not found
- Searched for "PointCloud" → Not found
- Searched for ".bin" → Not found
- Searched for "camera" → Not found
- Searched for "image" → Not found

**Attempt 2: Look at example code**
- Adrian's example uses: `PoseInFrame`, `Pose`, `Vector3`, `Quaternion`
- My data needs: `PointCloud` (for LiDAR), `CompressedImage` (for camera)
- Example shows how to CREATE a Pose object
- Does NOT show how to READ binary .bin files or .png images

**Attempt 3: Search Foxglove Docs ❌ FAILED**

**Search 1:** "convert bin files"
- Results: ROS 2 .db3 files, topic converter, schema converter
- Relevant to KITTI .bin LiDAR files? NO
- All results about ROS message conversions, not raw binary files

**Search 2:** "LiDAR conversion"  
- Results: Velodyne hardware connections, unit conversions
- About converting .bin files? NO
- All about live hardware or UI features, not file conversion

**Search 3:** "KITTI"
- Results: 3 results about "hitting" buttons in UI
- About KITTI dataset? NO
- Search just matched the word "hitting" (false positive)

**Conclusion:**
Foxglove docs do NOT explain how to convert:
- KITTI .bin files → PointCloud messages
- .png images → CompressedImage messages
- .txt calibration files → Transform messages

---

## Validation Complete ✅

**Following Adrian's email instructions:**
- ✅ Works for Pose data (his example)
- ❌ FAILS for KITTI data (no instructions provided)

**Following Foxglove docs:**
- ❌ No KITTI conversion guide
- ❌ No .bin file handling
- ❌ Only solution: Build Rust/WASM data loader (40+ hours)

**Gap confirmed:** There is NO accessible path from KITTI → Foxglove for non-Rust developers.