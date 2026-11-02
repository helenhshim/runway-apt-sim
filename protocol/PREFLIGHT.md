# Pre-flight (ticket T2, Linear HEL-64)

Goal: learn the constraints and rehearse the rubric on one throwaway run, spending free credits only. This run is not a case and never goes in the results CSV.

## Do
1. Open Runway on the free plan. Write down the credit balance (expected 125, one-time).
2. Pick the living room photo (EXIF stripped). Try Agent first. If Agent is not available on the free plan, use an image model (Gen-4 Image Turbo, listed at 2 credits).
3. Use the v1 prompt from `PROMPT.md` with one furniture piece and, if the app allows, the product reference image.
4. Before pressing run, write down the credit cost the app shows. After, check the balance.
5. Mark acceptable yes or no (gut call), then score the output with `RUBRIC.md`, using the 50% overlay on the real photo.

## Record
| Question | Answer |
|---|---|
| Plan and credit balance before |  |
| Agent available on this plan? |  |
| Surface used (agent / image model picker) |  |
| Is the model shown to the user? If so, which? |  |
| Credits shown before running |  |
| Credits actually charged |  |
| Minutes from start to output |  |
| Accepts a furniture reference image? |  |
| Output size and aspect ratio vs the input |  |
| Watermark on the export? Export resolution? (the guide says free tiers often limit these) |  |
| Photo quality check: bright, sharp, high resolution, straight verticals, original saved separately |  |
| Anything that changed that you did not ask for |  |

## Rehearse the rubric
Score the output and list every place you hesitated between two numbers:

Fix those anchors in `RUBRIC.md`, then fill in `landmarks.md`.

## Gate
When the protocol (`protocol/` folder, `schema.sql`) is final, commit it with a message like `freeze protocol v1 before generation`. Only then start T3.
