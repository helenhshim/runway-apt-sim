# Automated warping error beside the human score (T32, HEL-94)

Method: `warp_metric.py`. Farneback flow between consecutive frames of the OUTPUT, forward-backward occlusion mask, mean L1 after warping frame t+1 back to t (640x360, 0 to 255). Lower = steadier. Floor = start frame held still with grain sigma 1.5 = **1.68**. Plots and CSVs: `evidence/warp/` (gitignored).

## Scored clips (run after T30 closed, so the numbers could not bias scoring)
| Clip | Model | Mean err | Spikes (s) | Mean flow | Human temporal | Human events | Agree? |
|---|---|---|---|---|---|---|---|
| A1 | Gen-4.5 | 2.13 | 4.38 to 4.83 | 1.47 | 5 | 0 | No, metric flags, human does not |
| A2 | Gen-4.5 | 2.33 | 4.50 | 1.63 | 2 | 2 (stools morph, invented painting and wood) | Yes |
| B1 | Seedance 2.5 | 1.20 | start only | 0.76 | 5 | 0 | Yes |
| B2 | Seedance 2.5 | 1.16 | none | 1.03 | 5 | 0 | Yes |
| C1 | Gemini Omni 1.1 Flash | 0.99 | none | 0.67 | 2 | 3 (wrong chair, fake nook, missing furniture) | No, metric misses |
| C2 | Gemini Omni 1.1 Flash | 1.79 | 4.17 to 4.71 | 1.30 | 5 | 0 (invented side table noted) | No, metric flags, human does not |

Clip-level agreement (flagged or not vs events or not): 3 of 6. One hit (A2), two quiet matches (B1, B2), two false alarms (A1, C2), one miss (C1). Per-event agreement cannot be checked: the human events carry no timestamps.

## Build clips (not scored)
Mean err: Gen-4.5 b01 1.94, b02 1.86, b03 1.97; Seedance b01 1.17, b02 1.28, b03 1.34; Gemini b01 1.66, b02 1.64, b03 1.80. Spikes cluster in the last second for Gen-4.5 b03 and Gemini b01 to b03.

## Reading
- Error tracks camera speed and softness more than defects: it rises with mean flow, Seedance (softest, noted by Helen) is lowest everywhere, and spikes bunch at 4 to 5 s in A and C clips, which looks like the push speeding up, not events.
- It misses what Helen scored lowest in C1: a static fake nook and a wrong chair are consistent frame to frame, so warping error is low. This is a temporal metric, not a geometry or identity one.
- With n = 6 this is a signal check, not a validation. Verdict: not worth scaling as a stand-in for the human temporal score.

## Pitfalls
No input walkthrough exists, so this is output self-consistency, not fidelity to a camera path. Farneback, not RAFT. Blur and flat walls score low. Real reflections and new lighting count as error. All clips sit within about 1 to 2.3 of a floor at 1.68, so spread is small. Floor is a noise floor, so values below it (Seedance, C1) mean smoother than grain, not better.
