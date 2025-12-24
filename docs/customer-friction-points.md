# Customer Friction Points Documented

15 friction points experienced during KITTI → Foxglove onboarding (Dec 23-24, 2024)

## Data Acquisition Friction

**#1: Manual Download = Customer Empathy**
- Experiencing friction firsthand helps write better docs
- Don't just automate - understand the pain

**#2: Hidden Login Wall**
- KITTI requires account creation (not obvious upfront)
- Customer doc should say: "Step 0: Create KITTI account (2 min)"
- Many datasets have authentication requirements

**#3: Privacy in Registration**
- Academic datasets ask for "research purpose"
- Customers don't want to expose internal projects
- Generic language needed to protect confidentiality

**#4: Two-Tier Academic Registration**
- KITTI has download vs. benchmark submission tiers
- Customers confused by "step 2" - think they need it
- Clear doc: "Stop after account activation"

**#5: Dataset Governance Friction**
- Academic datasets protect leaderboards (prevent gaming) Extra friction for researchers, necessary for credibility
- Commercial customers don't care about benchmarks

**#6: Multi-Level Navigation**
- KITTI separates datasets by task (stereo, flow, object, raw)
- Customers need to know: "You want Raw Data, not benchmarks"
- Clear onboarding prevents wrong dataset downloads

**#7: Dataset Choice Paralysis**
- 20+ sequences visible, customer doesn't know which to pick
- Good doc: "Download drive_0001 (smallest, good variety)"
- Explain synced+rectified vs unsynced

**#8: Data Size Matters**
- Sequences range 0.3-1.8 GB
- For demos/testing, smaller = faster iteration
- Customers appreciate "quick start" options

**#9: Multiple Download Options**
- 4 download links per sequence unclear which required
- Good doc: "Download TWO: synced+rectified AND calibration"
- Explain what each contains and why needed

## Technical Implementation Friction

**#10: Live Debugging IS The Job**
- Real customer onboarding = troubleshooting unknown errors
- CSE must handle uncertainty with confidence
- Document solutions for next customer

**#11: Tool/Model Comparison**
- GPT-5.2 vs Cursor "Auto" - different strengths
- Multiple AI models valuable for specific errors
- Best tool = one that ships

**#12: Partial Success IS Success**
- 100% perfect first try = rare
- Getting data loading, even partially = WIN
- Iterate from working baseline

**#13: Don't Rebuild What Exists**
- Check vendor docs BEFORE building custom solution
- CSE role = critique/improve existing docs
- Learn by doing, then compare to official path

**#14: "Weakness" Is Strength**
- "Not tech-savvy" = see what experts miss
- Most failed onboarding = CSE too technical, can't relate
- Fresh perspective catches documentation gaps

**#15: LISTEN TO THE CUSTOMER**
- Customer said "we need calibration data" early
- Initially dismissed domain expertise (9 years AV)
- Should have trusted customer knowledge immediately

## Strategic Friction (Market-Level)

**#16: Founder Assumptions**
- CEO email assumes "customers are ROS engineers"
- Misses 50%+ market: raw data → MCAP conversion
- University students, automotive, legacy systems ignored

**#17: University Market Invisible**
- UCF robotics club never heard of Foxglove until industry
- Students = top of funnel (become directors in 5 years)
- Viral adoption opportunity completely untapped

## Implications for Foxglove

### Documentation Gaps
- No "raw data to MCAP" conversion guide
- Assumes ROS/protobuf expertise
- Missing troubleshooting for non-ROS users

### Product Gaps  
- No auto-detection of data formats
- Manual schema registration (error-prone)
- No "describe your robot → generate layout" AI

### Market Gaps
- University students underserved
- Academic datasets (KITTI, nuScenes, Waymo) no official support
- Legacy system migration not addressed
- Non-ROS ecosystems ignored

## Recommendations

**Short-term (Documentation):**
1. Create "Non-ROS Data Onboarding" guide
2. Add KITTI/nuScenes conversion examples
3. Troubleshooting section for protobuf errors
4. "Common mista FAQ

**Medium-term (Product):**
1. AI-powered format detection
2. Auto-generate converters for known formats
3. One-click KITTI/nuScenes import
4. Schema validation before upload

**Long-term (Strategic):**
1. University education program (free tier)
2. "Foxglove.ai" - AI-native onboarding
3. Legacy system migration service
4. Expand beyond ROS ecosystem
