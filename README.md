# Foxglove AV Customer Onboarding Demo

KITTI dataset to Foxglove MCAP conversion pipeline + AI-powered configuration assistant.

## What This Demonstrates

1. **Data Pipeline** - End-to-end KITTI → MCAP conversion with proper TF transforms
2. **Onboarding Gap Validation** - 4-hour manual config documented vs 5-minute AI-guided
3. **AI POC** - Layout generator achieving 95% automation (topic detection, frame settings, point cloud config)

## Status

- ✅ Phase 1: Working converter (151MB demo, 216 messages)
- ✅ Phase 1.5: Validation experiment (4-hour friction documented)
- ✅ AI POC: Layout generator achieving 95% automation

## Interview Evidence Package

- **Manual Validation**: 4-hour KITTI-360 configuration timeline with screenshots
- **Student Conversation**: UCF robotics student feedback (redacted)
- **Before/After**: Browser demo (0 min) vs downloaded MCAP (4 hours)
- **AI Acceleration**: Generic (70%) → Validated data (95%)

## Key Insight

Foxglove's examples showcase capabilities but lack conversion onboarding. This gap particularly affects academic users learning on datasets like KITTI. AI-powered assistance can bridge this gap by automating expert configuration knowledge.

## Key Files

- `data-pipeline/` - KITTI → MCAP converter
- `validation-experiment/` - Screenshots, friction docs, AI POC results
- `foxglove-ai-assistant.jsx` - React component for AI-guided config
- `test-layout-v5.json` - Working AI-generated layout

## Quick Start
```bash
# Run converter
cd data-pipeline && python kitti_to_mcap.py

# Open in Foxglove
# Import test-layout-v5.json for instant visualization
```

---
Built for Foxglove Customer Success Engineer interview.
