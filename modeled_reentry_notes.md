# How the Telemetry *Should* Look — A Physics-Based Re-entry Model

**Question addressed:** *Based on the speed of the spacecraft, what would a realistic telemetry table look like, from start to splashdown?*

This document accompanies `modeled_reentry_table.{csv,md,txt}`. It builds a **physics-based reference trajectory** for an Orion lunar-return re-entry so the broadcast's dial values can be compared against a realistic profile.

> **This is a MODEL, not observed data.** It is a plausible engineering trajectory built from published Orion entry parameters (entry speed, entry altitude, skip-entry profile, parachute deploy altitudes, splashdown speed) and made consistent with the values actually seen on the broadcast dials (~25,190 mph decaying to ~11,650 mph across the plasma window). Real mission telemetry would differ in the exact numbers, but the **shape** of the curve — the phases, the order, and the magnitudes — is what physics requires.

---

## 1. Why a lunar return looks different from a normal re-entry

Orion returns from the Moon at roughly **25,000 mph** — far faster than a spacecraft returning from low Earth orbit (~17,500 mph). To avoid a single brutal deceleration and to extend range/control, Orion uses a **skip (skip-glide) entry**:

1. **First entry** — dips into the atmosphere, sheds a large chunk of speed and endures a first peak-heating / peak-g event.
2. **Skip / loft** — the capsule generates lift and *climbs back up* briefly; drag drops, velocity decreases slowly, altitude increases.
3. **Second entry** — descends again into thicker air for a second heating event and the final deceleration.
4. **Parachutes** — drogues, then mains, bring it to a gentle splashdown.

This is exactly why, in the observed dials, the "FROM EARTH / altitude-like" value **dipped and then rose again** — a skip signature, not an error.

---

## 2. What the model shows (key waypoints)

| MET (from Entry Interface) | Velocity | Altitude | What is happening |
|:--------------------------:|---------:|---------:|:------------------|
| **0:00** | ~24,600 mph | 400,000 ft | **Entry Interface** — atmosphere begins |
| 0:30 | ~25,190 mph | 350,000 ft | Slight gravitational speed-up before drag dominates |
| 1:50 | ~19,500 mph | 220,000 ft | **First peak heating / peak-g** (~6 g) |
| 2:30 | ~14,500 mph | 205,000 ft | **Comms blackout** (plasma sheath) — matches the broadcast segment |
| 3:20 | ~11,650 mph | 210,000 ft | End of first entry (matches last observed dial value) |
| 5:00 | ~8,300 mph | 255,000 ft | **Skip apogee** — capsule has lofted back up |
| 7:10 | ~7,600 mph | 205,000 ft | **Second entry** — atmosphere re-engages |
| 8:00 | ~5,200 mph | 165,000 ft | Second peak heating |
| 11:40 | ~340 mph | 25,000 ft | **Drogue parachutes** deploy |
| 13:10 | ~95 mph | 9,500 ft | **Main parachutes** deploy |
| **19:00** | **~17 mph** | **0 ft** | **Splashdown** (Pacific Ocean) |

Full **second-by-second** table (1,141 rows, 0:00→19:00): `modeled_reentry_table.{csv,md,txt}`.

---

## 3. How this compares to the observed broadcast dials

- The observed segment (video 1:28:19 → 1:31:33) covers roughly the **first-entry deceleration and comms-blackout window** — velocity ~25,190 → ~11,650 mph. In the model this is the **0:30 → 3:20 stretch**, and the numbers line up by design.
- The observed **altitude-like dip-then-rise** matches the model's **first-entry → skip transition**.
- The broadcast did **not** show the later phases (skip apogee, second entry, chutes, splashdown) in the captured frames, which is why the model extends beyond what the screenshots contain.

**Bottom line:** the observed dial values, once OCR errors are removed, are **consistent with a realistic skip-entry deceleration**. The model in this table is what a full "start-to-splashdown" telemetry readout should look like for a lunar return.

---

## 4. Assumptions & limits (so nothing is overstated)

- Entry Interface fixed at **400,000 ft** by convention.
- Total EI→splashdown duration modeled at **~19 minutes**; real Orion lunar returns are in the ~20-minute range.
- Between waypoints, velocity and altitude are **linearly interpolated** — real curves are smooth, not piecewise-linear, so the per-10-second `g` figures are approximate.
- Peak-g modeled at ~6 g (first entry); real peaks depend on the exact flight-path angle.
- The "TO MOON" dial from the broadcast is not modeled here (it is a range-to-Moon distance, not part of the entry dynamics).
- Numbers are a **reference model**, not a prediction of any specific flight. Treat them as "what the shape should be," not exact truth.

*Companion to the corrected `comprehensive_frame_report.md`. Licensed CC BY-NC 4.0.*
