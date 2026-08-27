# NASA-Caught — Full Issues Deep Dive

**Purpose:** An honest, complete inventory of every known limitation, contradiction, and open problem in this project. Nothing hidden. Every claim below is traceable to the data files in this repo or to direct visual analysis of the NASA video. Where something is an assumption, it is labelled ⚠. Where something is a defect in our own work, it is labelled 🔧.

---

## 0. THE BIG ONE — both "sources" are NASA-produced (no independent verification exists)

You are correct: **our telemetry is itself read from NASA screenshots.** This collapses the central premise the earlier "NASA vs our telemetry" framing implied.

- The **mission-map animation** (`jsc2025m000169_Artemis_II_Mission_Map_4K.mp4`) is a NASA-rendered stylised animation.
- The **telemetry dials** (velocity / altitude / distance-to-Moon / mission clock) were read frame-by-frame off a **NASA broadcast graphics overlay** — i.e. NASA's own on-screen numbers, not raw instrument data.
- Therefore **both data sets originate from NASA.** This project is **NASA-vs-NASA**, not NASA-vs-independent-measurement.

**Consequences that must be stated plainly:**
1. **There is no independent verification anywhere in this project.** Nothing here can confirm or refute NASA's real trajectory — only compare two NASA-authored depictions to each other.
2. Our telemetry is a **second-hand reading** (human/OCR reading of rendered pixels). That adds a reading-error layer *on top of* NASA's already-rendered numbers. We are two removes from any instrument.
3. Any language anywhere in this repo that implies our telemetry is "our data" in the sense of independent evidence is misleading and must be corrected to "our reading of NASA's broadcast dials."

This does **not** make the analysis worthless — comparing two NASA products can still expose internal inconsistencies, frozen graphics, gaps, and stylisation-vs-numbers mismatches. But it can never be "catching" reality; at most it catches **inconsistencies inside NASA's own outputs.**

---

## 1. Provenance issues (where the numbers actually come from)

| # | Issue | Evidence |
|---|-------|----------|
| 1.1 | Telemetry source is a **separate, longer broadcast video**, not the 30 s mission-map animation. | `scene` field runs 1→2916 (≈2915 source frames ≈ **97 s at 30 fps**); mission-map mp4 is only 30.1 s. |
| 1.2 | **Mission clock advances ~2× the video wall-time.** 193 s of mission clock (1:28:19→1:31:32) is captured across ~97 s of video. Either the broadcast was time-lapsed or the on-screen clock is not wall-clock. | `sec` span 5299→5492 = 193 s vs ~97 s of source frames. |
| 1.3 | Reading method (OCR/manual) is **not documented in the repo.** No extraction script for `traj_telemetry.json` is committed — we cannot audit how the numbers were read or what the error bars are. | Only `build_truesiddiqui_anim.py` references the JSON; no OCR/`cv2`/`ffmpeg` extractor present. |
| 1.4 | No frame-level confidence / read-error estimate exists. Dial glare, motion blur, and interlacing can misread a digit and nothing flags it. | No confidence field in the schema (`idx, scene, t, sec, vel, alt, moon, md5, rel, downrange`). |

---

## 2. Data-completeness issues (how much is actually real, moving data)

| # | Issue | Evidence |
|---|-------|----------|
| 2.1 | **43% of frames are a FROZEN display.** 115 of 265 frames (idx 38–152) are stuck at mission clock 1:28:19–1:28:20. The graphic was frozen/looping, not advancing. | Run analysis: idx 39–103 all `t=1:28:20` (65 frames); idx 105–152 all `t=1:28:19` (48 frames). |
| 2.2 | Only **107 unique mission-timestamps** exist across all 265 frames. The rest are repeats. | `len(set(t))` = 107. |
| 2.3 | **45% of the mission timeline has NO data.** Of 194 possible mission-seconds in the window, only 107 are represented — **87 seconds are missing entirely.** | Distinct `sec` = 107 of 194. |
| 2.4 | **The single most important phase happened entirely inside the data blackout.** During the +110 s gap (idx 152→153), velocity fell **25,064 → 14,492 mph** and altitude rose **28 → 40 mi** — the whole deceleration and the skip-entry peak occurred with **zero captured data.** | idx 152: 25064 mph / 28 mi / t=1:28:19 → idx 153: 14492 mph / 40 mi / t=1:30:09. |
| 2.5 | 111 byte-identical duplicate frames (by md5) inflate the apparent sample count. Only **154 md5-unique frames.** | `len(set(md5))` = 154 / 265. |

---

## 3. Data-integrity anomalies (things that are physically impossible / broken)

| # | Issue | Evidence |
|---|-------|----------|
| 3.1 | **Two clock reversals.** At idx 38 and idx 105 the mission clock jumps *backward* to 1:28:19. Time cannot run backward — this is a broadcast replay/looping artifact. | idx 37 `t=1:28:44` → idx 38 `t=1:28:19`; idx 104 `t=1:28:21` → idx 105 `t=1:28:19`. |
| 3.2 | **Velocity is non-monotonic during re-entry** (should be steadily decelerating). e.g. idx 188→189 vel 13,812→13,842 (rises), idx 194→196 13,641→13,658, idx 210→211 13,296→13,399. Read-noise wobble ~idx 189–211. | Direct values in `traj_telemetry.json`. |
| 3.3 | **Long constant-velocity plateau of 13,658 mph** across idx 196–202 (7 frames identical) is suspicious for a decelerating capsule — likely a stuck digit, not real physics. | idx 196–202 all `vel=13658`. |
| 3.4 | The frozen block (§2.1) sits **exactly before** the blackout gap (§2.4). The broadcast froze, then skipped 110 s — the two worst artifacts are adjacent and bracket the critical maneuver. | idx 38–152 frozen, idx 152→153 gap. |

---

## 4. Derived-quantity issues (numbers we computed, not read)

| # | Issue | Evidence |
|---|-------|----------|
| 4.1 | ⚠ **Downrange (0→948 mi) is NOT measured.** It is integrated as ∫velocity·dt, which assumes (a) `t` is true seconds and (b) motion is purely horizontal. Both are unproven, and (a) is contradicted by §1.2 and §2. Downrange should be treated as an *illustrative estimate*, not data. | `downrange` field is computed in-repo, not a dial reading. |
| 4.2 | ⚠ **g-forces (peak ~9.16 g) are derived** from velocity differences and inherit all velocity noise (§3.2/3.3) plus the timing uncertainty. The "peak" may partly reflect read-noise. | `g` computed in `build_truesiddiqui_anim.py` from Δvel/Δt. |
| 4.3 | ⚠ Altitude **28→40→34 mi "skip-entry signature"** is an *observation of the dial*, not a confirmed maneuver — and the rise happened during the blackout (§2.4), so we never saw it occur. | `alt` values; gap at §2.4. |

---

## 5. Geography issues (there is none in the data)

| # | Issue | Evidence |
|---|-------|----------|
| 5.1 | **No latitude, longitude, or heading exists in any dial.** Every geographic element in both animations is illustrative. | Schema has no lat/lon/heading field. |
| 5.2 | ⚠ Entry point (48°N 165°W) and splashdown region in `TrueSiddiquiAnimation.html` are **visual estimates from the NASA video**, not measurements. | Anchors hard-coded in `build_truesiddiqui_anim.py`. |
| 5.3 | The NASA (cyan) arc is a **smooth interpolated great-circle** — an invented continuous path for illustration, not an observed frame-by-frame track. | `NASA_ARC` slerp in the generator. |

---

## 6. 🔧 Internal contradictions in our OWN repo (defects to fix)

| # | Issue | Evidence |
|---|-------|----------|
| 6.1 | 🔧 **Two animations disagree on where splashdown is.** `reentry_animation.html` centres on and labels splashdown **Atlantic, 28.5°N 75°W (off Florida)**; `TrueSiddiquiAnimation.html` shows **Pacific, off Baja**. Both are in the repo simultaneously. | `reentry_animation.html` line 40: "⚠ ASSUMED splashdown ~28.5°N 75°W". |
| 6.2 | 🔧 The Atlantic assumption was **retracted** in the comparison docs and memory, but `reentry_animation.html` was **never updated** — the retraction is not reflected in that file. | Retraction noted in `nasa_vs_telemetry_comparison.*`; old file unchanged. |
| 6.3 | 🔧 The comparison docs (`nasa_vs_telemetry_comparison.*`, commit e2e1719) predate the **"both sources are NASA"** realization (§0) and may still frame telemetry as independent. Needs a provenance addendum. | Docs authored before this finding. |
| 6.4 | 🔧 Deprecated modeled files remain in the repo (`modeled_descent.json`, `modeled_reentry_*`) and can mislead a reader into thinking modeled content is current. | Files present; flagged deprecated only in memory. |

---

## 7. Cross-verification impossibility (the logical ceiling)

- NASA animation has **geography but no numbers**; our telemetry reading has **numbers but no geography** — and now we know **both are NASA's own outputs.**
- They share **no common measurable quantity**, so they cannot numerically confirm or contradict each other, and even if they could, agreement would only show NASA is self-consistent, not that either is *true*.
- **Honest ceiling of this project:** it can document NASA's own internal inconsistencies (frozen graphic, 110 s gap, clock reversals, stylised-vs-numeric mismatch). It **cannot** independently establish the real trajectory or "catch" NASA in a factual error about reality.

---

## 8. Why some tasks were pending (straight answer)

I owe you a direct answer rather than an excuse:

1. **I had not been keeping a visible task list**, so "pending" work wasn't surfaced to you — that's on me. There is now a live todo list tracking every item in this turn.
2. The genuinely **unfinished items before this turn were:**
   - The **Atlantic/Pacific contradiction** (§6.1/6.2) — `reentry_animation.html` was never reconciled after the retraction. **Still open → being fixed this turn.**
   - The **provenance realization** (§0) — the "both sources are NASA" point had not been written into any doc. **Being fixed this turn (this file).**
   - The comparison docs' independence framing (§6.3) — **flagged, addendum pending.**
3. Nothing was "stuck" for a hidden reason and nothing was skipped to look complete. The gaps above are the real, complete list.

---

*Generated as part of the NASA-Caught TRUTH-MODE audit. If any statement here is not backed by a file in this repo or the NASA video, treat it as an error and report it.*
