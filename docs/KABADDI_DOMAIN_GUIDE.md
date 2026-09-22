# The Machine Learning Researcher's Guide to Kabaddi

A domain reference guide for data scientists and ML researchers working with **PKL-Bench**.

---

## 1. Court Geometry & Spatial Landmarks

The standard Pro Kabaddi playing court is a rectangular mat measuring **$13.0\text{ m} \times 10.0\text{ m}$**, bisected by a **Midline** into two equal halves ($6.5\text{ m} \times 10.0\text{ m}$):

```
+-------------------------------------------------------------+
|                          END LINE                           |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
|                         BONUS LINE                          | (1.0m from baulk)
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
|                         BAULK LINE                          | (3.75m from midline)
|                                                             |
|========================== MIDLINE ==========================|
|                                                             |
|                         BAULK LINE                          |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
|                         BONUS LINE                          |
| - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
|                          END LINE                           |
+-------------------------------------------------------------+
   |<--- 1.0m Lobby --->|               |<--- 1.0m Lobby --->|
```

- **Baulk Line ($3.75\text{ m}$ from midline)**: The raider must cross this line with at least one foot (and the trailing foot in the air) for the raid to be deemed legally valid.
- **Bonus Line ($4.75\text{ m}$ from midline)**: Active only when the defense has **$\ge 6$ players**. To score a bonus point (1 pt), the raider must plant a foot past the bonus line with the trailing foot completely off the ground before being touched.
- **Lobby ($1.0\text{ m}$ yellow border strips)**: Initially out of bounds. Once physical contact is established between raider and any defender, the lobbies activate as legal playing territory. Entering the lobby without prior contact results in dismissal.

---

## 2. Match Mechanics & Timing

- **Duration**: 40 minutes of regulation playing time, divided into two **20-minute halves** separated by a 5-minute interval.
- **30-Second Raid Clock**: Each raid has a strict 30-second time limit countdown. If the raider does not return to their half within 30 seconds, they are dismissed (out) and 1 point is awarded to the opponent.
- **Continuous Cant**: The raider must continuously chant the word *"Kabaddi"* without taking a fresh breath until returning across the midline.

---

## 3. Core Scoring Rules & Strategic Discontinuities

### 3.1 The Empty Raid & Do-or-Die (DOD) Rule
- **Empty Raid**: If a raider crosses the baulk line and returns to their half without touching a defender or securing a bonus point, the raid is "Empty" (0 points for both teams).
- **Do-or-Die (DOD) Raid**: If a team executes **two consecutive empty raids**, their third raid is classified as a **Do-or-Die raid**. The raider *must* score at least one point (touch or bonus); otherwise, the raider is declared out, and the defense receives 1 point. This rule eliminates passive, stalling strategies.

### 3.2 Super Tackle ($N_{def} \le 3$)
When a defending team has **3 or fewer active players on court**, any successful tackle awards **2 points** (rather than 1 point) to the defense. This creates a high-leverage defensive state where defenders frequently initiate coordinated multi-man traps.

### 3.3 Super Raid
Any raid in which the raider accumulates **$\ge 3$ points** (e.g. 3 touch points, or 1 bonus + 2 touch points) in a single 30-second raid.

### 3.4 All-Out (Lona) & Revival Dynamics
- **Revival Order**: When a team scores a point, their previously dismissed players are revived in the exact chronological sequence in which they were put out.
- **All-Out**: When all 7 active defenders of a team are dismissed, an **All-Out** is declared. The attacking team receives **2 bonus points** (in addition to the final touch point), and all 7 players of the opposing team are instantly revived back onto the court.

---

## 4. Player Tactical Roles & Mat Positions

A starting 7 lineup arranges defenders in structured arc formations:

| Position | Tactical Role | Primary Defensive Actions |
| :--- | :--- | :--- |
| **Right Corner** | Outer right anchor | Ankle hold, diving thigh hold, chain initiation |
| **Left Corner** | Outer left anchor | Ankle hold, diving thigh hold, chain initiation |
| **Right Cover** | Inside second defender (right) | Dash, body block, waist grab |
| **Left Cover** | Inside second defender (left) | Dash, body block, waist grab |
| **In / Supporting** | Flanking covers | Chain link support, barrier assist |
| **Main Raider** | Primary offensive attacker | Toe touch, hand touch, dubki, frog jump |
