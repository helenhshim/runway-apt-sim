# Prompt template v1 (prompt_id = v1)

Follows the structure in Runway's own staging guide (https://runway.com/resources/ai-virtual-staging): room and a restrained style, then a preservation clause, then the furnishings, then lighting and realism requirements.

One template for every case. Variables: [room], [piece], [wall]. Nothing else changes between rooms, so differences in results come from the room and the model, not the wording.

> Stage this [room] in a restrained, minimal style with [piece] against [wall]. Keep the room exactly as photographed: the same camera position and perspective, room dimensions, walls, windows, doors, flooring, ceiling, trim, fixtures, vents and built-ins, and the view outside the window. Do not move, add or remove any opening. Scale [piece] to the door beside it and leave a clear walking path to the door. Match the photo's daylight, keep reflections consistent, and add contact shadows under the furniture.

Inputs
- Photo: bright, sharp, high resolution, straight verticals, clear room boundaries. Keep the untouched original saved separately.
- If the Runway app accepts a reference image, attach the product image of [piece]. If it does not, describe the piece in one short phrase and record "no reference image" in notes; that is a finding.
- One or two furnishings only. The guide notes restrained furniture shows scale better and leaves less room for error.

Rules
- Do not edit the prompt after the protocol commit. A changed prompt is `v2`, committed before use, and results are never mixed across versions.
- Two attempts per room, changing no variable between them (the guide suggests two or three options, one variable at a time; here the repeat measures variance).
- Same input photo and same surface for both attempts, unless the surface choice is the thing being logged.
- First-pass outputs only are scored in the MVP. A targeted fix with the AI photo editor is a separate follow-up (ticket T14).
