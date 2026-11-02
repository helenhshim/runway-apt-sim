# Rubric v1 (frozen with the T2 protocol commit)

Each generation is scored 1 to 5 on three criteria. Anchors are fixed before the first run. The three criteria follow the quality checklist in Runway's own staging guide (https://runway.com/resources/ai-virtual-staging): architecture maps to layout fidelity, lighting and materials to lighting and material realism, and furniture and scale to furniture accuracy. Every anchor below is meant to be decidable without a gut feel. If a score is still a coin flip, pick the lower score and write the two numbers in `notes`.

## Layout fidelity
Checked with a 50% overlay of the output on the real photo, against the 8 landmarks in `landmarks.md`. A landmark is kept if it sits within 2% of the image width of its position in the photo, measured on the overlay. Record `landmarks_kept` (0 to 8). The score comes from the count alone:

| landmarks_kept | Score |
|---|---|
| 8 | 5 |
| 7 | 4 |
| 6 | 3 |
| 4 or 5 | 2 |
| 3 or fewer | 1 |

Caps: an opening added, removed or resized caps the score at 1. A listed doorway closed or blocked caps it at 2. Soft or shifted edges that stay inside the 2% rule do not change the count.

## Lighting and material realism
Four checks: (a) shadow direction matches the photo's light; (b) a contact shadow under every added piece; (c) reflections (the chrome lamp shade, the TV screen, glass) consistent with the room; (d) floor and wall materials continuous, not repeated or replaced. A flaw is minor if it is visible only when zoomed to full size or on the overlay, and clear if it is visible at normal viewing size.

| Score | Anchor |
|---|---|
| 5 | All four checks pass |
| 4 | One minor flaw |
| 3 | One clear flaw, or two minor flaws |
| 2 | Two clear flaws, or three or more flaws of any kind |
| 1 | Lit from the wrong side, an object floating, or materials broken or replaced |

## Furniture accuracy
Four checks, each pass, marginal or fail:

| Check | Pass | Marginal | Fail |
|---|---|---|---|
| Identity (vs the reference image) | Shape, color and material match | One detail differs (for example frame finish) | A different type of piece |
| Scale | Looks right against the console, couch and stool | Looks a little too big or too small, but could pass for real | Obviously too big or too small |
| Placement | At the stated spot, on the floor | Within about one chair width of the spot | Elsewhere, floating, or intersecting a wall or other furniture |
| Walking path to the dark front door | Clear | Narrowed but passable | Blocked |

Scale is judged by eye on the overlay and the output, against things in the same room, not against the far door. The Wassily is 80 cm tall with a seat at about 44 cm. Compare it with the TV console (35 cm tall), the couch seat and the stool, taken at about the same distance from the camera: its top should sit a little more than twice the height of the console top, and its seat near the couch seat height. "A little too big or small" means a visible but plausible error; "obviously" means a viewer would notice without comparing.

`scale_error_pct` is optional supporting evidence. Fill it only when the chair and the console are at a similar distance from the camera (within about 1.5 times). Measure both heights in pixels from their floor contact points: `|chair_px / console_px / (80.0 / 35) - 1| x 100`. Otherwise leave it blank and say why in `notes`. The Pass, Marginal or Fail call never needs the number, and a blank is not a logging error.

| Score | Anchor |
|---|---|
| 5 | All four checks pass |
| 4 | One marginal, none fail |
| 3 | Two marginal, or one fail |
| 2 | Two fails |
| 1 | The wrong piece (identity fail on type), or the piece blocks the path |

## Acceptable (gut call, made right after generating, before scoring)
Question: would I trust this image to decide whether to buy this furniture for this room? Yes or no. Runway's guide grades each image Pass, Revise or Reject: Pass means acceptable = yes. Revise (fixable with one targeted edit) and Reject both mean acceptable = no; write the word Revise or Reject at the start of `notes` so it can be counted. After scoring, the page reports how often the gut call agrees with layout >= 4 and furniture >= 4.

## Side effects
A listed keep-item (see `PROMPT.md`: couch, TV, TV console and its contents, left doorway) that is moved, resized, recolored or removed is a `side_effect` failure, severity 2 or higher. An unlisted item that changes goes in `notes` only.

## Severity (for failure rows)
- 1: only noticeable on the overlay or when looking closely.
- 2: visible to a casual viewer; could mislead a purchase decision.
- 3: the room is not recognizable, or an opening is wrong; unusable.

## Consistency
Re-score 3 of the 4 outputs at least 48 hours after the first pass, shuffled, without looking at the first scores (ticket T11).
