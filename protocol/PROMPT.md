# Prompt template v1 (prompt_id = v1)

Follows the structure in Runway's own staging guide (https://runway.com/resources/ai-virtual-staging): room and a restrained style, then a preservation clause, then the furnishings, then lighting and realism requirements.

One template for every case. Variables: [room], [piece], [wall]. Nothing else changes between rooms, so differences in results come from the room and the model, not the wording.

> Stage this [room] in a restrained, minimal style with [piece] against [wall]. Keep the room exactly as photographed: the same camera position and perspective, room dimensions, walls, windows, doors, flooring, ceiling, trim, fixtures, vents and built-ins, and the view outside the window. Do not move, add or remove any opening. Scale [piece] to the door beside it and leave a clear walking path to the door. Match the photo's daylight, keep reflections consistent, and add contact shadows under the furniture.

Inputs
- Photo: bright, sharp, high resolution, straight verticals, clear room boundaries. Keep the untouched original saved separately.
- If the Runway app accepts a reference image, attach the product image of [piece]. If it does not, describe the piece in one short phrase and record "no reference image" in notes; that is a finding.
- One or two furnishings only. The guide notes restrained furniture shows scale better and leaves less room for error.

Rules
- Do not edit the prompt after the protocol commit. A changed prompt is a new version, committed before use, and results are never mixed across versions. v2 is already defined below as a planned condition.
- Two attempts per room, changing no variable between them (the guide suggests two or three options, one variable at a time; here the repeat measures variance).
- Same input photo and same surface for both attempts, unless the surface choice is the thing being logged.
- First-pass outputs only are scored in the MVP. A targeted fix with the AI photo editor is a separate follow-up (ticket T15).

## Prompt v2: context condition (living room only)

A single photo of one room does not show the apartment's real proportions. v2 adds a second image, the dining nook photo, and tells the model how the two spaces connect. It is a planned test condition, committed with v1 before any generation, and the two are never mixed.

Images: (1) the living room photo to stage, (2) the dining nook photo, (3) the product image of the piece. If the app takes fewer than three images, record that in the T2 comment and describe the missing ones in words instead (that change is itself noted in `notes`).

> Image 1 is the living room to stage. Image 2 is the dining nook of the same apartment, which connects directly to the living room [how they connect: fill in before the freeze, for example "through the open archway on the left of image 1"]. Use image 2 only to understand the real proportions of the space and how the rooms connect. Do not draw image 2 into image 1, and do not change anything visible in image 1. Image 3 is [piece and its real size, for example "The Wassily chair in black leather with a polished steel frame, about 80 cm high, 77 cm wide and 74 cm deep"]. Stage the living room in a restrained, minimal style, with [piece] [position, for example "to the left of the couch as seen in image 1"]. Keep the room exactly as photographed: the same camera position and perspective, room dimensions, walls, windows, doors, flooring, ceiling, trim, fixtures, vents and built-ins, and the view outside the window. Do not move, add or remove any opening. Scale [piece] to the door beside it and leave a clear walking path to the door. Match the photo's daylight, keep reflections consistent, and add contact shadows under the furniture.

Design
- Living room is run twice on v1 and twice on v2: 4 generations, 8 in total with the other two rooms. Same piece and position in both conditions.
- Log case ids `living_v1` and `living_v2` with `prompt_id` v1 and v2, so the roll-up keeps them apart.
- Do not use one attempt of each as the two repeats; the repeats measure variance, the condition measures the effect of context.
- Hypothesis H6: the extra context improves the furniture and scale scores for the living room. It is disproved if scale error and furniture score are no better under v2.
- No product link in any prompt: attach the product image instead. The piece's size comes from the product page (The Wassily: H 31.5 in, W 30.3 in, D 29.1 in per thorvalddesign.com; the centimetre figures are conversions).
