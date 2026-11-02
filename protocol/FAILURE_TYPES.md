# Failure types (must match `validate_log.py`)

One failure row per generation that broke. Pick the single most important type; mention others in `notes`. Severity is defined in `RUBRIC.md`.

| failure_type | Definition |
|---|---|
| geometry | Walls, corners, ceiling line or floor plane shifted, warped or re-proportioned |
| opening | A door or window added, removed, resized or moved |
| scale | Furniture more than 10% off against the door ruler |
| placement | Furniture in the wrong spot, floating, intersecting a wall, or blocking the path |
| identity | The piece does not match the reference (shape, material, color) |
| shadow | Shadow direction wrong, or contact shadows missing |
| reflection | Mirror or glass reflections inconsistent with the room |
| material | Floor or wall texture changed, repeated or discontinuous |
| hallucination | An object appears that was not requested and is not in the photo or reference |
| side_effect | An existing item or the lighting changed without being asked |

A generation with no failure has blank failure_type and severity.
