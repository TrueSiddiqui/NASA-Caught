# Comprehensive Frame-by-Frame Analysis — NASA Artemis II Re-entry Broadcast

**Source:** 266 screenshot frames extracted from *"NASA's Artemis II Crew Comes Home (Official Broadcast)"* (YouTube `watch?v=nfhDuOHMp0A`)
**Scope:** On-screen telemetry dials during the re-entry / plasma-blackout segment (video time ≈ 1:28:19 → 1:31:33)
**Method:** OCR of each frame's three dials — **VELOCITY M/H**, **FROM EARTH Miles**, **TO MOON Miles** — followed by **manual visual verification** of every value flagged as anomalous.

> **This is a revised report.** An earlier version of this analysis contained several errors caused by OCR misreads and a misunderstanding of the on-screen time field. Those errors, and the corrections, are documented in full in Section 2 below. This revision separates **what is provable from the frames** from **what is assumption or interpretation**, per the project's accuracy standard.

---

## 1. What the footage actually shows (critical context)

Before any anomaly claim, the nature of the footage must be stated plainly, because it changes how the dial readings should be interpreted:

- The segment is **explicitly labeled "VISUALIZATION"** on-screen (top-left of the video frame).
- The broadcast narration during this segment states, in substance, *"this is a visualization of the plasma build-up around the spacecraft."*
- This segment coincides with the **communications blackout** during peak heating. The narration explicitly notes NASA does **not** have live communications from the crew during this window (e.g., *"still do not have communications from the crew"*).

**Implication:** The three dials in this segment are part of an **acknowledged animation/model**, shown *during a period when live hardware telemetry is not being received*. They therefore represent **modeled/predicted values driving a graphic**, not a live downlink from the vehicle. Any irregularity in these dials is an irregularity **in a visualization**, and must be described as such — not as a discrepancy in NASA's flight telemetry.

---

## 2. Corrections to the prior analysis

The following claims appeared in the earlier report. Each has been re-examined against the original frames and is **retracted or corrected**:

| # | Prior claim | Finding on re-check | Status |
|---|-------------|---------------------|--------|
| 1 | "**−142 minute time reset** at scene 2817 (jumps to 3:53:40)" | The video overlay shows time as **CURRENT / TOTAL**. "3:53:40" is the **total video duration**, not a timestamp. Scene 2817's actual current time is **1:31:25**, fully consistent with its neighbors (2806 = 1:31:24, 2828 = 1:31:26). The OCR had captured the duration field. | **RETRACTED (false positive)** |
| 2 | "**+2,937 mph velocity reversal** at scenes 2872 / 2883" | OCR misread the leading digit **1 as 4**: "11,778"→"14,778" and "11,745"→"14,745". The true sequence is a smooth deceleration 11,841 → 11,778 → 11,745 → 11,711. | **RETRACTED (OCR error)** |
| 3 | Scene 144 velocity "25,108" | Correct value on visual check is **25,105**. | **CORRECTED** |
| 4 | Scene 265 To-Moon "248,256" | Correct value on visual check is **248,254**. | **CORRECTED** |

**Process note:** Two independent OCR passes produced the *same* digit-misread in case #2, so OCR cross-checking alone was insufficient — every flagged value was ultimately confirmed by reading the pixels of the original frame crop. The corrected values are reflected in `telemetry_clean.json` and `complete_telemetry_table.*`.

**Two interpretive claims from the prior report are also withdrawn** as not substantiated:
- *"Velocity increasing during re-entry is anomalous."* A small climb (25,064 → 25,192 mph over ~25 s) before/at atmospheric entry interface is consistent with continued gravitational acceleration prior to significant atmospheric drag. It is not, on its own, evidence of an error.
- *"Geometrically impossible that both Earth-distance and Moon-distance increase."* Both distances increasing simultaneously is geometrically possible during an altitude-gaining (skip) phase and is not a contradiction.

---

## 3. Verified observations (provable from the frames)

These are stated conservatively and are directly checkable in the data table.

### 3.1 Byte-identical (duplicate) frames
Of the 266 frames, **only 155 are unique**; 111 are exact byte-for-byte duplicates (verified by MD5 hash) of another frame. Three duplicate blocks account for the bulk:

| Block | Frame hash | # frames | Scene range | Video time shown | Dials shown |
|-------|-----------|---------:|-------------|------------------|-------------|
| A | `318cbfe6` | 65 | 430–1134 | 1:28:20 | v=25,067 · earth=28 · moon=248,177 |
| B | `c6ca2230` | 47 | 1–1673 | 1:28:19 | v=25,064 · earth=28 · moon=248,174 |
| C | `f5accc2c` | 2 | 419–1167 | 1:28:19 | v=25,064 · earth=28 · moon=248,175 |

**Honest interpretation:** Every frame within a duplicate block **shares the same on-screen video time**. They are therefore the *same broadcast moment* captured multiple times by the screenshot process — **not** different points in time showing frozen numbers. This is the single most important correction to the project's working hypothesis (see Section 5). It is consistent with the segment being a held/looping visualization graphic during the blackout.

### 3.2 The 110-second jump
Between the end of the duplicated 1:28:19–1:28:20 material (scene 1673) and the next distinct frame (scene 1684, time **1:30:09**), the video time advances ~110 s and velocity drops **25,064 → 14,492 mph**. This is the peak-heating / blackout interval. The dials resume smooth behavior after it. Whether this represents a genuine ~110 s hold of the graphic or simply a gap in the screenshot sampling **cannot be determined from the frames alone** and is left as undetermined.

### 3.3 Minor velocity non-monotonicities in the second segment
After the jump, velocity generally decelerates (≈14,492 → 11,650 mph) but shows six small *increases* between consecutive advancing frames:

| Between scenes | Video time | Velocity change |
|----------------|-----------|-----------------|
| 2069 → 2080 | 1:30:34→35 | +30 mph |
| 2102 → 2113 | 1:30:36→37 | +61 mph |
| 2146 → 2157 | 1:30:39→40 | +101 mph |
| 2245 → 2256 | 1:30:46→47 | +166 mph |
| 2311 → 2322 | 1:30:50→51 | +103 mph |
| 2355 → 2366 | 1:30:53→54 | +95 mph |

These were visually confirmed as real (not OCR errors). They are small relative to the overall ~3,000 mph decline across the same window and are **consistent with interpolation/animation artifacts in a visualization graphic**. They are the only genuine non-physical micro-fluctuations found in the corrected dataset.

### 3.4 Overall telemetry is internally consistent and physically plausible (after correction)
- **Velocity:** monotonic-with-minor-jitter deceleration from ~25,192 mph (entry interface) down to ~11,650 mph.
- **From Earth (mi):** 28 → 32 (segment 1), then 40 → 34 (segment 2) — a dip-then-climb profile consistent with an Orion skip-entry trajectory.
- **To Moon (mi):** steady increase 248,174 → 248,628 (spacecraft moving away from the Moon).
- **Outlier scan of the corrected data:** **zero** remaining velocity OCR outliers; the only large velocity change is the expected drop across the 110 s blackout gap.

---

## 4. Claims NOT supported by the evidence

To keep provable findings separate from speculation, the following are explicitly **not** supported by these frames:
- No evidence that the telemetry "stayed the same while time advanced." Every duplicate frame shares the same displayed time.
- No evidence of a time reversal, a velocity reversal, or a geometric impossibility (all three were OCR/interpretation errors — Section 2).
- No basis to characterize the modeled dial values as falsified data; they are a labeled visualization shown during the comms blackout.

---

## 5. Honest conclusion

The corrected, verified dataset does **not** support the hypothesis that *"the speed should have changed but the telemetry did not."* The opposite is true in this footage: **whenever the on-screen video time advances, the telemetry changes accordingly**, and every apparently "frozen" frame is a byte-identical duplicate that also carries the **same** displayed timestamp — i.e., the same broadcast moment captured more than once, not a later moment with stale numbers.

The genuine, defensible observations are narrower:
1. The segment is a **NASA-labeled visualization shown during the communications blackout**, so its dials are modeled values, not a live downlink.
2. The screenshot set is **~42% exact duplicates**, which can create a misleading impression of "frozen" telemetry if timestamps are not checked.
3. There are **small (≤166 mph) non-monotonic velocity blips** in the second segment, consistent with animation interpolation, not physics.

The earlier "anomalies" (time reset, velocity reversal, geometric impossibility) were **artifacts of OCR misreads and a misread time field**, and are withdrawn. This revision documents them transparently rather than leaving them in the record.

---

*Data: `telemetry_clean.json` (corrected) · `complete_telemetry_table.{csv,md,txt}` · 266 source frames in `frames/`. Values obtained by OCR with manual pixel-level verification of all flagged readings. Licensed CC BY-NC 4.0.*
