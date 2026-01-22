# UZH-FPV Drone Racing Dataset - FLAID Validation Results

**Dataset:** UZH-FPV Drone Racing (High-speed 6DoF visual-inertial odometry)  
**File:** `example-002-drone-ds.mcap`  
**Test Date:** January 22, 2026  
**Validation Method:** Compare FLAID-generated config against manually validated ground truth

---

## Ground Truth (Manual Validation)

**Status:** 🚧 TO BE FILLED AFTER MANUAL INSPECTION

After manual testing with actual UZH-FPV drone data:

**Critical Topics (Must Have):**
- `[CAMERA_TOPIC]` - Camera feed (to be determined)
- `[IMU_TOPIC]` - IMU data for visual-inertial odometry
- `[ODOMETRY_TOPIC]` - Pose/odometry estimates
- `/tf` - Transform tree

**Optional But Useful:**
- `[CAMERA_INFO_TOPIC]` - Camera calibration (if available)
- `[VELOCITY_TOPIC]` - Velocity/twist (if available)

**All Available Topics:**
```
[RUN: mcap info example-002-drone-ds.mcap]
[PASTE OUTPUT HERE]
```

---

## Test Setup

**Input to FLAID:**
1. **Description:** "UZH-FPV Drone racing dataset with visual-inertial odometry"
2. **Topic List:** [TO BE PASTED AFTER MCAP INSPECTION]

**Expected Behavior:**
- Parse topic list
- Identify camera topic (likely contains "image" or "cam")
- Identify IMU topic (likely contains "imu")
- Identify odometry/pose topic
- Include `/tf` for transforms
- Generate drone-optimized layout (camera-first view)

---

## FLAID Output (First Pass)

**Status:** 🚧 TO BE FILLED AFTER RUNNING TEST

### Generated Topics

[PASTE FLAID OUTPUT HERE]

### Layout Configuration

**Primary Image Topic:** `[DETECTED_CAMERA]`  
**Primary IMU Topic:** `[DETECTED_IMU]`  
**Frame Settings:**
- Fixed frame: `[DETECTED_FIXED]`
- Display frame: `[DETECTED_DISPLAY]`

**Camera Settings:**
- Smooth: true
- Rotation: [DETECTED]

**Layout Style:**
- [DESCRIBE PANEL ARRANGEMENT]

---

## Validation Results

**Status:** 🚧 TO BE CALCULATED AFTER TEST

### Critical Topics: ?/4 (?%)

| Ground Truth Topic | Detected? | Status |
|-------------------|-----------|---------|
| `[CAMERA_TOPIC]` | ❓ | TO BE TESTED |
| `[IMU_TOPIC]` | ❓ | TO BE TESTED |
| `[ODOMETRY_TOPIC]` | ❓ | TO BE TESTED |
| `/tf` | ❓ | TO BE TESTED |

### Overall Accuracy: ?%

**[SUMMARY TO BE WRITTEN]**

---

## What Worked Well

**Status:** 🚧 TO BE FILLED AFTER TEST

1. **Topic Parsing:** [RESULT]
2. **Type Detection:** [RESULT]
3. **Priority Assignment:** [RESULT]
4. **Primary Topic Selection:** [RESULT]
5. **Layout Generation:** [RESULT]

---

## Issues Found

**Status:** 🚧 TO BE FILLED AFTER TEST

### 1. [ISSUE NAME]
**Issue:** [DESCRIPTION]  
**Impact:** [HIGH/MEDIUM/LOW]  
**Fix Time:** [ESTIMATE]

### 2. [ISSUE NAME]
**Issue:** [DESCRIPTION]  
**Impact:** [HIGH/MEDIUM/LOW]  
**Fix Time:** [ESTIMATE]

---

## Time Comparison

### Manual Configuration (Before FLAID)
- **Time:** ~1-2 hours (estimated)
- **Process:**
  1. Open MCAP in Foxglove (5 min)
  2. Browse topic list, identify sensors (10 min)
  3. Configure camera view (15 min)
  4. Set up IMU visualization (10 min)
  5. Configure frames for drone (20 min)
  6. Optimize for high-speed playback (20 min)
  7. Arrange panels (15 min)
  8. Export layout (5 min)

**Pain Points:**
- High-speed drone data requires special settings
- Frame configuration for 6DoF movement
- Camera orientation/rotation
- Trajectory visualization

### FLAID-Assisted (With AI)
- **Time:** ~5 minutes (estimated)
- **Process:**
  1. Run `mcap info example-002-drone-ds.mcap` (30 sec)
  2. Copy topic list (10 sec)
  3. Paste into FLAID (10 sec)
  4. Add description (20 sec)
  5. Generate config (2 sec)
  6. Copy JSON (5 sec)
  7. Import to Foxglove (30 sec)
  8. Minor tweaks (2 min)

**Pain Points:**
- [TO BE FILLED AFTER TEST]

**Time Saved:** ~[CALCULATE] minutes ([CALCULATE]% reduction)

---

## Recommendations

**Status:** 🚧 TO BE FILLED AFTER TEST

### For FLAID v2
1. **Drone-Specific Heuristics:**
   - [BASED ON TEST RESULTS]

2. **High-Speed Visualization:**
   - [BASED ON TEST RESULTS]

3. **6DoF Frame Handling:**
   - [BASED ON TEST RESULTS]

---

## Conclusion

**Status:** 🚧 TO BE WRITTEN AFTER TEST

**FLAID performance on UZH-FPV Drone dataset:**
- ✅/❌ [ACCURACY] on critical topics
- ✅/❌ [ACCURACY] on optional topics
- ✅/❌ Valid layout JSON generated
- ✅/❌ [TIME SAVINGS]% time reduction
- ⚠️ [ISSUES FOUND]

**Status:** [READY/NEEDS WORK] for real-world use with drone datasets

**Key Insight:** [TO BE DETERMINED AFTER TEST]

---

## Next Steps

1. **Run Manual Inspection:**
```bash
# Get topic list
mcap info example-002-drone-ds.mcap > drone-topics.txt

# Open in Foxglove to identify critical topics
foxglove example-002-drone-ds.mcap
```

2. **Test with FLAID:**
   - Open `test-drone.html`
   - Paste actual topics
   - Generate configuration
   - Document results

3. **Validate in Foxglove:**
   - Import generated layout
   - Test playback
   - Note any issues
   - Time the process

4. **Update This Document:**
   - Fill in ground truth
   - Document FLAID output
   - Calculate accuracy
   - Write conclusions

---

## Appendix: Test Files

- `test-drone.html` - Standalone test harness with flexible validation
- `example-002-drone-ds.mcap` - Test dataset (not in repo)

### Running the Test

```bash
# Open test harness in browser
open test-drone.html

# Or serve with Python
python3 -m http.server 8000
# Then navigate to http://localhost:8000/test-drone.html
```

The test will:
1. Pre-fill dataset description
2. Wait for manual topic paste
3. Generate configuration
4. Display flexible validation (sensor type coverage)
5. Show expected time savings

---

**Validated by:** [TO BE COMPLETED]  
**Tool Version:** FLAID v1 (attempt-following-adrian implementation)  
**Next Dataset:** [TBD - Waymo? nuScenes?]
