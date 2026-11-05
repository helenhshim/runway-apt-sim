# Failure types p2 (must match `validate_p2.py`)

One failure row per clip that broke. Pick the single most important type; mention others in `notes`. Severity is defined in `RUBRIC.md`.

## Kept from P1
| failure_type | Definition |
|---|---|
| geometry | Walls, corners, ceiling line or floor plane shifted, warped or re-proportioned (in a single frame) |
| opening | A door, doorway or window added, removed, closed or moved |
| scale | A piece obviously too big or too small against the room in the start frame |
| placement | A piece in the wrong spot, floating, or intersecting a wall or another piece |
| identity | A piece does not match the start frame (shape, material, color) |
| shadow | Shadow direction wrong, or contact shadows missing |
| reflection | Reflections on the chrome lamp, glass table or TV inconsistent with the room |
| material | Floor or wall material replaced, repeated or not matching the real photo |
| hallucination | Something appears that is not in the start frame or the real room (an object, a person, text) |

`side_effect` from P1 is dropped: in image to video every unrequested change is one of the types above.

## New in P2
| failure_type | Definition |
|---|---|
| invented_area | Space the start frame does not show is invented wrong as the camera moves: an extra room, a different hallway, a wall or door that is not in the real room (judged against photo A and the start frame) |
| flicker | Texture, light or color pulses from frame to frame |
| morph | A piece or surface changes shape or identity over time |
| pop | Something appears or disappears without being hidden by something else |
| drift | Architecture slides or warps while the camera moves, parallax is wrong, or light moves with the screen instead of the room |
| path_ignored | The camera does not move forward as asked (turns, stops, reverses), or the clip freezes |
| render_look | The output still looks like a 3D render overall (it never became photoreal) |

A clip with no failure has blank failure_type and severity.
