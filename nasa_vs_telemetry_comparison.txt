# NASA Mission-Map Animation vs. Our Telemetry — Entry Point → Splashdown

### A truth-mode, side-by-side forensic comparison

**Scope of this document.** It compares exactly two things, and nothing else:

1. **NASA's own animation** — the file `jsc2025m000169_Artemis_II_Mission_Map_4K.mp4`, specifically the last-day re-entry segment (Entry Point → Splashdown), as it visually appears on screen.
2. **Our telemetry** — `traj_telemetry.json`, 265 frames read directly off the on-screen dials of the broadcast we captured.

Everything below is separated into **PROVABLE** (directly visible in one of those two sources) and **ASSUMED / UNKNOWN** (not present in either, or inferred). No outside data was consulted. No number was invented. Where the two sources disagree or cannot check each other, that is stated plainly.

---

## 1. The two sources are not the same kind of thing

| | NASA mission-map animation | Our captured telemetry |
|---|---|---|
| **What it is** | A stylised whole-mission visualisation (launch → free-return → splashdown) | A frame-by-frame log of the on-screen numeric dials during re-entry |
| **Re-entry segment length** | ~3 seconds of screen time (~00:26 → 00:29 of a 30 s clip) | 193 real seconds (video clock 1:28:19 → 1:31:32) |
| **Carries geography?** | **Yes** — Earth, continents, a drawn ground track, a splashdown point | **No** — not one latitude, longitude, or heading value exists in the data |
| **Carries numbers?** | **No** — zero velocity/altitude/time/coordinate readouts on screen | **Yes** — velocity, altitude, downrange, mission time, Moon distance per frame |
| **Style** | Smooth, continuous, artist-rendered arc | Raw samples with duplicates, a time reversal, and a blackout gap |

**The single most important fact in this whole comparison:** the two sources have **no overlapping measurable quantity**. NASA shows *where*; our dials show *how fast / how high / when*. Neither can confirm or refute the other's unique claims. Any statement that "the telemetry matches the NASA animation" (or contradicts it) on trajectory **cannot be proven** — they do not measure the same thing.

---

## 2. What is PROVABLE from NASA's animation (Entry → Splashdown)

These are things visibly on screen in NASA's own file. No interpretation:

- **P-N1.** The re-entry portion occupies roughly the final ~3 seconds of the clip (~00:26–00:29).
- **P-N2.** A glowing entry marker approaches Earth **from the west** (out of the North Pacific) and travels generally **west-to-east** across northern latitudes.
- **P-N3.** The depicted **splashdown is in the Pacific Ocean, off the west coast of North America** (California / Baja region).
- **P-N4.** There are **no numeric readouts of any kind** in the animation — no velocity, no altitude, no timestamp, no coordinates, no scale bar.
- **P-N5.** The arc is **smooth and continuous** — it contains no visible duplicated frames, no backward jump, and no blackout gap.

## 3. What is PROVABLE from our telemetry (the dials)

Directly read or arithmetically derived from `traj_telemetry.json`:

- **P-T1.** 265 frames span video clock **1:28:19 → 1:31:32** = **193 s** of coverage.
- **P-T2.** Velocity falls **25,064 → 11,650 mph** (peak reading 25,192 mph).
- **P-T3.** Altitude ("FROM EARTH" dial) goes **28 → 40 → 34 mi** — it **rises 12 mi and then dips**, rather than descending monotonically.
- **P-T4.** Downrange (integrated from dial velocity) reaches **≈ 948 mi** by the last frame.
- **P-T5.** Peak deceleration derived from the velocity trace is **≈ 9.16 g** (around frame 203).
- **P-T6.** **154 unique frames + 111 byte-identical duplicate frames** (109 duplicate-of-previous transitions inside the animation window).
- **P-T7.** **Two time reversals** — the clock jumps *backward* at frame 38 (and again at 105) to 1:28:19.
- **P-T8.** **One blackout gap** — between frame 152 and 153 the clock jumps forward **+110 s** with no data in between.
- **P-T9.** The data **ends at 34 mi altitude / 11,650 mph** — a craft still travelling at hypersonic speed, **well above the ocean**. Our telemetry **never records a splashdown**.

---

## 4. Differences, ambiguities, and anomalies (the deep dive)

### 4.1 Splashdown location — a corrected assumption
- **NASA (P-N3):** Pacific, off western North America.
- **Our data:** contains **no location at all** (P-T9) and stops while still aloft.
- **Earlier in this project we had assumed splashdown ~28.5°N 75°W — the Atlantic, off Florida.** That assumption is **contradicted by NASA's own depiction** and was never supported by our dials. **It is retracted.** The honest position is: *our data cannot place the splashdown anywhere; NASA's animation places it in the Pacific.*
- **Status:** our old Atlantic guess = **wrong/unsupported**; NASA Pacific = **what NASA shows** (we did not independently verify it, but it is their own claim).

### 4.2 Geography vs. numbers — the unbridgeable gap
- NASA has a ground track but no numbers (P-N4); we have numbers but no ground track (P-T… no geography).
- **Ambiguity:** the direction of travel around the globe, the entry corridor, and the landing coordinates are **UNKNOWN from our telemetry**. Our replica therefore refuses to draw a map and instead plots an **altitude-vs-downrange profile** — the only spatially honest thing our data supports.

### 4.3 Our data ends before splashdown
- NASA's arc reaches the water (P-N3); ours stops at 34 mi / 11,650 mph (P-T9).
- **≈ the entire final descent (from 34 mi down to sea level) is absent from our telemetry.** Anyone claiming our data "shows the landing" would be wrong.

### 4.4 The altitude rise — possible skip-entry signature
- Altitude climbs 28 → 40 mi then settles to 34 (P-T3). A monotonic fall would be expected for a simple ballistic descent.
- **A rise-then-fall is consistent with a skip / lofted entry** (the vehicle uses lift to climb back out briefly before final descent). **This is an observation, not a confirmed maneuver** — the dials show the altitude numbers; they do not label a "skip." NASA's smooth arc (P-N5) shows no such feature, but it also carries no altitude scale, so it **cannot confirm or deny** it.

### 4.5 Anomalies present in our data, absent in NASA's
NASA's animation is smooth and continuous (P-N5). Our raw telemetry is not:
- **Time reversals** (P-T7) at frames 38 and 105 — the clock runs backward to the start. Consistent with a **broadcast replay/loop artifact**, not real vehicle motion.
- **Blackout gap** (P-T8) — +110 s missing at frame 153, exactly where altitude reads its 40 mi peak. Whatever happened during those 110 s was **not captured**.
- **111 duplicate frames** (P-T6) — long stretches where the image is byte-identical; the broadcast was static/frozen there.
- **A velocity wobble** near frames 189–211 (readings jitter up and down a few hundred mph, e.g. 13,764 → 13,842 → 13,721) — consistent with **OCR / dial-read noise**, not real re-acceleration.
- **None of these appear in NASA's animation** because it is an artist-smoothed rendering, not a live data feed.

### 4.6 Timescale mismatch
- NASA compresses the whole mission into 30 s and the re-entry into ~3 s (P-N1); our telemetry covers 193 real seconds of that same re-entry (P-T1). They are **not frame-comparable**; you cannot line up "NASA second 27" with any specific telemetry frame.

---

## 5. What our replica (`TrueSiddiquiAnimation.html`) does and does not claim

**Does (all from real dials):**
- Plots every one of the 265 frames as an **altitude (real) vs. downrange (real)** profile.
- Shows live velocity, altitude, downrange, derived g-force, mission time, and Moon distance.
- Marks the **entry point**, the **40 mi altitude peak** (skip signature), the **time reversal**, the **blackout gap**, and the **hard data-end** at 34 mi / 11,650 mph.

**Does NOT (honest omissions):**
- Does **not** draw a map, a ground track, continents, or a splashdown point — we have no geography.
- Does **not** continue the trajectory to the ocean — our data stops while the craft is still aloft.
- Does **not** smooth away the duplicates, reversal, or gap — they are shown as they are.

---

## 6. Bottom line

- **NASA's animation and our telemetry measure different things and cannot verify each other.** NASA = geography, no numbers. Us = numbers, no geography.
- **NASA depicts a Pacific splashdown.** Our data neither confirms nor denies it — and our earlier Atlantic/Florida assumption is **retracted as unsupported.**
- **Our telemetry stops at 34 mi / 11,650 mph, still aloft** — it contains **no splashdown**, so the final descent is simply missing from our record.
- **Our data carries real anomalies** (2 time reversals, a 110 s blackout, 111 duplicate frames, read-noise wobble) that NASA's smooth animation does not — because one is a raw capture and the other is a stylised rendering.
- **The altitude 28→40→34 profile is a genuine, provable feature** of our data and is consistent with a skip/lofted entry, but the dials do not label it as such, so it stays an **observation, not a claim.**

*Truth, nothing but truth: where the data could not prove something, this document says so instead of guessing.*
