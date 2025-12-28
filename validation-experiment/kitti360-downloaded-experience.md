# KITTI-360 Downloaded MCAP Experience - COMPLETE

## Timeline
- **Start:** 11:05 AM (Dec 26, 2024)
- **Image working:** 11:30 AM (25 min)
- **Point cloud working:** 3:13 PM (4+ hours total, including breaks)
- **Final polish:** 5:35 PM

## Steps Required (NOT in documentation)

**Image Panel (25 minutes):**
1. Wrong default topic `/camera/image_raw` → doesn't exist
2. Trial-and-error to find `/camera_00_semantic/image`
3. Enable "Rectify" to stop jumpiness

**3D Panel (2+ hours):**
1. Enable all topics in Topics section - FAILED
2. Enable transforms - STILL FAILED
3. Read help docs - confusing, no clear steps
4. Multiple searches for "how to display point cloud"
5. Perplexity search #1 → found Frame settings critical
6. Fixed frame = `map`, Display frame = `velodyne_frame`
7. Point size = 5 (default too small)
8. Color mode settings to prevent jumping
9. Press `1` to recenter camera (not documented)
10. Axis scale = 0 to remove blue dot
11. Line width = 0 to remove yellow lines

## Comparison
**Browser:** 0 min → perfect demo
**Downloaded:** 4+ hours → same result

## Key Missing Documentation
- Fixed vs Display frame distinction
- Topic enablement in 3D panel vs global
- Point size defaults invisible
- Camera controls (press 1 to recenter)
- Transform visualization settings
- Search only works within current panel

## Conclusion
Even Foxglove's curated KITTI-360 example requires expert knowledge to use when downloaded. This is the onboarding gap.
