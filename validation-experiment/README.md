# Validation Experiment - FLAID Testing

Testing the Foxglove AI Assistant (FLAID) against real robotics datasets to measure accuracy and time savings.

## Test Datasets

### ✅ KITTI-360 (Autonomous Vehicle)
- **File:** `ai-poc-results.md`
- **Accuracy:** 95% (after manual validation refinement)
- **Status:** Validated ground truth integrated into FLAID

### ✅ Hilti Robot SLAM (Indoor Construction)
- **File:** `hilti-results.md`
- **Accuracy:** 100% on critical topics
- **Status:** First-pass test with real topic list

## Running Tests

### Quick Test (Hilti)
```bash
# Open test harness in browser
open ../test-hilti.html

# Or serve locally
cd ..
python3 -m http.server 8000
# Navigate to http://localhost:8000/test-hilti.html
```

The test will:
1. Auto-load Hilti SLAM dataset description
2. Pre-fill all 11 Hilti topics
3. Generate configuration
4. Display validation results with accuracy score

### Manual Testing

1. **Get Dataset Topics:**
```bash
# From MCAP file
mcap info your-dataset.mcap

# From ROS bag
rosbag info your-dataset.bag
```

2. **Test with FLAID:**
   - Open `test-hilti.html` (or main component)
   - Paste dataset description
   - Paste topic list
   - Click "Generate Configuration"

3. **Validate Results:**
   - Check critical topics are included
   - Verify message types are correct
   - Test layout JSON in Foxglove
   - Document in new markdown file

## Test Results Summary

| Dataset | Critical Topics | Accuracy | Time Manual | Time FLAID | Savings |
|---------|----------------|----------|-------------|------------|---------|
| KITTI-360 | 4 | 95% | 4 hours | 5 min | 99% |
| Hilti SLAM | 3 | 100% | 2 hours | 5 min | 96% |

**Average Time Savings:** 97.5%  
**Average Accuracy:** 97.5%

## Files

- `ai-poc-results.md` - KITTI-360 validation (70% → 95% with ground truth)
- `hilti-results.md` - Hilti SLAM validation (100% first pass)
- `videos/` - Demo videos (small files in repo, large in Google Drive)
- `screenshots/` - Manual debugging screenshots

## Next Datasets to Test

- [ ] Waymo Open Dataset
- [ ] nuScenes
- [ ] CARLA Simulator output
- [ ] Custom industrial robot data

## Adding New Test

1. Create `[dataset-name]-results.md`
2. Document ground truth (manual validation)
3. Run FLAID with actual topic list
4. Compare results
5. Calculate accuracy: `correct_critical_topics / total_critical_topics * 100`
6. Document time savings
7. Update this README

## Key Insights

1. **Paste topics = 95%+ accuracy:** When users provide actual topic names, FLAID is highly accurate
2. **Generic descriptions = 70%:** Without topic list, accuracy drops but still useful
3. **Time savings consistent:** ~2-4 hours → 5 minutes across datasets
4. **Minor tweaks common:** Frame names, value ranges need dataset-specific tuning
5. **Critical vs optional matters:** 100% on critical topics is achievable, optional is bonus

---

**Test Framework:** Manual validation + automated comparison  
**Status:** Production validation ongoing  
**Goal:** 95%+ accuracy across 10+ diverse datasets
