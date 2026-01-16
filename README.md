# Foxglove AV Customer Onboarding Demo

KITTI dataset to Foxglove MCAP conversion pipeline + AI-assisted configuration tool.

## What This Demonstrates

1. **Data Pipeline** - End-to-end KITTI → MCAP conversion with proper TF transforms
2. **Onboarding Gap Validation** - 4-hour manual config documented vs AI-assisted approach
3. **AI POC** - Configuration generator showing 70-80% automation potential

## Completed

✅ Working KITTI → MCAP converter  
✅ 4-hour validation experiment (documented friction)  
✅ AI-assisted configuration generator (70-80% automation, needs refinement)  
✅ Interview presentation with embedded videos

## Key Files

- `data-pipeline/` - KITTI → MCAP converter
- `validation-experiment/` - Screenshots, friction docs, AI POC results
- `foxglove-ai-assistant.jsx` - React component for AI-assisted config
- `foxglove-interview-demo.html` - Complete presentation

## Quick Start

```bash
# Run converter
cd data-pipeline && python kitti_to_mcap.py

# Open in Foxglove
# Use generated layouts for visualization
```

## The Gap

Foxglove's browser demos showcase perfect visualization instantly. However, there is no documented, end‑to‑end path for taking the raw KITTI/KITTI‑360 datasets and reproducing those visualizations locally in MCAP and Foxglove; users must supply their own converters, topic mapping, and layout configuration. This undocumented gap is especially painful for academic users who primarily work from public datasets rather than ROS/MCAP‑native stacks. This gap particularly affects academic users learning on datasets like KITTI.

**Evidence:** 4-hour configuration timeline, student feedback, systematic friction documentation.

---

Project originally developed for a Foxglove Customer Success Engineer interview, now generalized as an AV onboarding demo.
