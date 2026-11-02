# Prompts v1 and v2 (prompt_id = v1, v2)

Follows the structure in Runway's own staging guide (https://runway.com/resources/ai-virtual-staging): room and a restrained style, then the furnishing, then a preservation clause, then lighting and realism requirements.

Scope of the frozen run (decided 2026-11-02): the living room only, 2 attempts on v1 and 2 attempts on v2, 4 generations. The dining nook and bedroom are not run; their landmarks and pieces are deferred (see `COVERAGE.md`). The text below is final for the living room. Nothing is edited after the freeze commit.

## The piece

The Wassily chair, Midnight Black Premium Leather (https://thorvalddesign.com/product/the-wassily/). Listed size H 31.5 in x W 30.3 in x D 29.1 in, seat height 17.3 in. The centimetre figures (80.0 x 77.0 x 73.9 cm, seat 43.9 cm) are our conversion, not the listing. Full grain aniline leather seat with a polished #304 stainless steel frame. Attach the product image. No product link goes in any prompt.

## Prompt v1: baseline

Inputs: (1) the living room photo, (2) the product image of the chair.

> Image 1 is a photo of my living room. Image 2 is a product photo of one chair. Stage the room in a restrained, minimal style by adding one chair from Image 2: The Wassily in black full grain leather with a polished stainless steel frame, 31.5 in high, 30.3 in wide, 29.1 in deep (80 x 77 x 74 cm), seat height 17.3 in. Place it on the open floor in the foreground of Image 1, to the left of the grey couch and in front of the wooden stool, angled toward the couch. Keep the room exactly as photographed: the same camera position and perspective, room dimensions, walls, flooring, ceiling, trim, fixtures, vents and built-ins. Do not move, add or remove any opening. Do not change, move, resize, recolor or remove the couch, the TV, the TV console and everything on the console, or the open doorway on the left of the far wall, and keep that doorway clear. Add nothing except the chair. Scale the chair to its listed size using the couch, the stool and the console beside it, and leave a clear walking path to the dark front door at the far end. Match the photo's daylight, keep reflections consistent, and add contact shadows under the chair.

## Prompt v2: context condition

A single photo of one room does not show the apartment's real proportions. v2 adds the dining nook photo as a second image and says how the two spaces connect. It is a planned test condition, committed with v1 before any generation. Results are never mixed across versions.

Inputs: (1) the living room photo, (2) the dining nook photo, (3) the product image of the chair. If the app takes fewer than three images, record that in the T3 notes and describe the missing one in words; that change is itself noted in `notes`.

> Image 1 is a photo of my living room. Image 2 is a photo of the dining nook of the same apartment, which adjoins this living room on the right and behind the camera in Image 1, through the opening just past the near end of the couch wall. Use Image 2 only to understand the real proportions, ceiling height and floor of the apartment. Do not draw the nook, its white tulip table, its chairs or its window into Image 1. Image 3 is a product photo of one chair. Stage the living room in a restrained, minimal style by adding one chair from Image 3: The Wassily in black full grain leather with a polished stainless steel frame, 31.5 in high, 30.3 in wide, 29.1 in deep (80 x 77 x 74 cm), seat height 17.3 in. Place it on the open floor in the foreground of Image 1, to the left of the grey couch and in front of the wooden stool, angled toward the couch. Keep the room exactly as photographed: the same camera position and perspective, room dimensions, walls, flooring, ceiling, trim, fixtures, vents and built-ins. Do not move, add or remove any opening. Do not change, move, resize, recolor or remove the couch, the TV, the TV console and everything on the console, or the open doorway on the left of the far wall, and keep that doorway clear. Add nothing except the chair. Scale the chair to its listed size using the couch, the stool and the console beside it, and leave a clear walking path to the dark front door at the far end. Match the photo's daylight, keep reflections consistent, and add contact shadows under the chair.

The only difference from v1 is the added nook photo and the context sentences about it.

## Design

- Living room run twice on v1 and twice on v2: 4 generations. Same piece and position in both conditions.
- Case ids `living_v1` and `living_v2`, with `prompt_id` v1 and v2, so the roll-up keeps them apart. `room` is `living` for both.
- The two attempts within a condition are repeats and measure variance; the condition measures the effect of context. Do not use one attempt of each as the two repeats.
- Hypothesis H6: the extra context improves the furniture and scale results for the living room. It is disproved if mean furniture score and the share of runs with scale error over 10% are no better under v2 than under v1.
- The Astra render of the nook is not given to Runway as context. It would leak Astra's layout into Runway's result.

## Keep-list

The preservation clause protects exactly these existing items: the couch, the TV, the TV console and everything on it, and the open doorway on the left of the far wall. The stool, the arc lamp and the drying rack are not on the list. A change to a listed item is a `side_effect` failure (RUBRIC.md). A change to an unlisted item is written in `notes` and is not a failure by itself.

## Rules

- Do not edit a prompt after the freeze commit. A changed prompt is a new version, committed before use, and results are never mixed across versions.
- Two attempts per condition, changing no variable between them. Run order is interleaved: v1 attempt 1, v2 attempt 1, v1 attempt 2, v2 attempt 2, so drift over time does not land on one condition. Score the four outputs in a shuffled order without looking at which prompt made them, where you can.
- Same input photo and same surface for all four generations, unless the surface choice is the thing being logged.
- First-pass outputs only are scored in the MVP. A targeted fix with the AI photo editor is a separate follow-up (T15).
- Inputs: bright, sharp, high resolution, straight verticals. Use `evidence/input_living_stripped.jpg` (v1 and v2) and `evidence/input_nook_stripped.jpg` (v2 only): EXIF and GPS stripped copies of the originals in `~/claude/interior design`, which stay untouched.

## Surface settings and logging (frozen with the protocol)

- Surface: Runway Agent in Ask mode (not Auto), so the plan and the cost are visible before each run. Optimize generations is set to Quality for every formal run. A Cost-optimized run is an optional comparison, logged as its own case, because the setting changes routing and credit cost (hypothesis H5).
- The model named in the chat (for example Sonnet 5.5) is the orchestrator, not the image model. Record it in `notes`. `model_shown` is the image model, and "not shown" is a valid answer.
- Agent rewrites the prompt before it calls the image model; the "Generated image" step shows its own version. Expand it and screenshot it for every run, and note in `notes` whether the rewrite dropped or changed a clause.
- `minutes` runs from the approval click to the finished image; note how many approvals were needed.
- `credits` is the cost shown on the approval card if there is one, otherwise the balance difference before and after. The pilot cost 25 credits for one Agent image edit.
