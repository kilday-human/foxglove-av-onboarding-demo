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

## Demo Videos

**Small videos (in repo):**
- [downloaded-blank-panels.mov](validation-experiment/videos/downloaded-blank-panels.mov) - Initial blank state
- [browser-demo-working.mov](validation-experiment/videos/browser-demo-working.mov) - Browser demo working

**Large videos (Google Drive):**
- [ai-assistant-demo.mov](https://drive.google.com/file/d/1PezSesfzreLpNgu1fB4ogSHwF697EdDf/view?usp=sharing) - AI assistant generating layout
- [final-working-layout.mov](https://drive.google.com/file/d/1VDRmAWjhKkitGa9fBNwI8GEtzyrnmxN1/view?usp=sharing) - Final working visualization
- [github-repo-walkthrough.mov](https://drive.google.com/file/d/1cysfLmDn-24n69lCmrAMi4mWrQuh5pLL/view?usp=sharing) - Repository walkthrough
- [manual-debugging-process.mov](https://drive.google.com/file/d/1tLUtEbdHld5BxDEL-SYGxta9iIDFhYD5/view?usp=sharing) - 4-hour debugging session

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
