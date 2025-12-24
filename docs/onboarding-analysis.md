# Foxglove Onboarding Analysis

## CEO Welcome Email (Received Dec 2024)

From: Adrian Macneil, CEO & Founder, Foxglove

> Hi Christopher,
> 
> I'm Adrian, Foxglove's CEO and Founder. I wanted to say welcome and thanks for choosing Foxglove.
>  
> If you're using ROS or MCAP already, simply drag and drop a .bag or .mcap file onto the Foxglove visualization UI...
> 
> [Assumes user has: .bag/.mcap files, ROS knowledge, schema understanding]

## Gap Analysis

**What Adrian Assumes:**
- User already has `.bag` or `.mcap` files
- Familiarity with ROS message types  
- Understanding of schemas and frame IDs
- Can write Python with protobuf

**My Reality (Non-ROS Customer):**
- Had raw KITTI sensor data (not MCAP)
- Needed data conversion pipeline
- Hit 15+ friction points
- No docs for "raw data → MCAP" path

## Market Gaps Identified

### 1. University Students
- **Finding**: UCF robots club president never heard of Foxglove until Luminar internship
- **Implication**: Entire university market untapped
- **Opportunity**: Free tier + educational positioning = viral adoption

### 2. Non-ROS Ecosystems
- Automotive Tier 1s with proprietary formats
- Academic researchers (KITTI, nuScenes, Waymo)
- Legacy systems with custom bag files

### 3. "Automagical" Onboarding Missing
- Current: Manual setup, assumes expertise
- Opportunity: AI-powered "describe your robot → auto-generate layout"
- Parallel: Cursor transformed VS Code with AI layer

## Strategic Insight

**Foxglove today** = Great tool for ROS professionals  
**Foxglove.ai vision** = AI-native platform that works with ANY data

**The $1B play**: Capture students + legacy systems + non-ROS markets
