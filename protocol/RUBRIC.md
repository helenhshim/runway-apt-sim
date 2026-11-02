# Rubric v1 (DRAFT until committed as the T2 protocol commit)

Each generation is scored 1 to 5 on three criteria. Anchors are fixed before the first run. The three criteria follow the quality checklist in Runway's own staging guide (https://runway.com/resources/ai-virtual-staging): architecture maps to layout fidelity, lighting and materials to lighting and material realism, and furniture and scale to furniture accuracy. If a score is a coin flip between two numbers, the anchor is too vague: fix it before the commit, never after.

## Layout fidelity
Checked with a 50% overlay of the output on the real photo, against the 8 landmarks written in `landmarks.md`. Record `landmarks_kept` (0 to 8): a landmark is kept if it sits within about 2% of the image width of its position in the photo.

| Score | Anchor |
|---|---|
| 5 | All 8 landmarks kept; no opening added, removed or resized; doorways still open and usable; the view outside the window unchanged |
| 4 | 7 kept, deviations only visible on the overlay |
| 3 | 6 kept, or one edge visibly softened or shifted |
| 2 | 4 to 5 kept |
| 1 | 3 or fewer kept, or an opening added or removed |

## Lighting and material realism

| Score | Anchor |
|---|---|
| 5 | Shadow direction matches the window; contact shadows under all added furniture; reflections consistent; floor and wall materials continuous |
| 4 | One minor flaw (for example one weak contact shadow) |
| 3 | One clear mismatch (wrong shadow softness, a reflection that disagrees with the room) |
| 2 | Two or more clear mismatches |
| 1 | Lit from the wrong side, floating objects, or materials broken or replaced |

## Furniture accuracy
Four checks: identity matches the reference image; scale within +-10% of the door ruler (record `scale_error_pct`); placement is sensible; a clear walking path to the door.

| Score | Anchor |
|---|---|
| 5 | All four checks pass |
| 4 | One check marginal |
| 3 | One check clearly fails |
| 2 | Two checks fail, or scale is more than 25% off |
| 1 | Wrong piece, or the piece blocks the path |

## Acceptable (gut call, made right after generating, before scoring)
Question: would I trust this image to decide whether to buy this furniture for this room? Yes or no. Runway's guide grades each image Pass, Revise or Reject: Pass means acceptable = yes. Revise (fixable with one targeted edit) and Reject both mean acceptable = no; write the word Revise or Reject at the start of `notes` so it can be counted. After scoring, the page reports how often the gut call agrees with layout >= 4 and furniture >= 4.

## Severity (for failure rows)
- 1: only noticeable on the overlay or when looking closely.
- 2: visible to a casual viewer; could mislead a purchase decision.
- 3: the room is not recognizable, or an opening is wrong; unusable.

## Consistency
Re-score 3 of the 6 outputs at least 48 hours after the first pass, shuffled, without looking at the first scores (ticket T11).
