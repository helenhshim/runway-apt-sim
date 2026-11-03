# Eval + world-model research notes

Researched 2026-11-03. Every claim cites a page I opened that day (pub date in brackets). "Not verified" = I could not confirm from a primary page.
Blocked pages (HTTP 403, skipped): openai.com "Video generation models as world simulators", help.runwayml.com Aleph article.

## 1. How video generation/editing models are evaluated today

| Method | What it measures | Known weaknesses | Fit for structure-preserving v2v (render walkthrough to photoreal) |
|---|---|---|---|
| VBench [S1, 2023-11-29] | 16 dims. Temporal ones: Subject Consistency (DINO cosine sim to first + previous frame), Background Consistency (CLIP same scheme), Temporal Flickering (pixel MAE between consecutive frames, static scenes only), Motion Smoothness (AMT interpolation error), Dynamic Degree (RAFT flow). Human preference annotations per dim. | Authors say static output can "cheat" consistency scores; recommend reading with Dynamic Degree. Flicker defined on static scenes only. | Partial. Consistency/flicker assume no or little camera motion; a 5 s walkthrough moves, so raw frame MAE punishes correct motion. Text-to-video framing, no source-video reference. |
| VBench++ [S2, 2024-11-20] | Adds image-to-video (adaptive Image Suite) and trustworthiness (bias, safety). | Long-video scope not confirmed on abstract page. | Low. Still no input-video fidelity. |
| VBench-2.0 [S3, 2025-03] | "Intrinsic faithfulness": 18 dims across Human Fidelity, Controllability, Creativity, Physics, Commonsense. Includes Multi-View Consistency, Camera Motion, Instance Preservation, Material. | Authors say VLMs are weak at 3D understanding and counting; multi-view consistency has no 3D ground truth so uses proxies; clips under ~10 s limit narrative. | Ideas transfer (multi-view consistency, instance preservation), but it is prompt-driven, not v2v. |
| EvalCrafter [S4, 2023-10] | 700 prompts, 17 objective metrics over visual, content, motion quality and text alignment; fits weights to human opinion. | Specific temporal metric list not on abstract page (not verified there). | Low. T2V only. |
| WorldScore [S5, ICCV 2025, v2 2025-11-29] | World generation as camera-trajectory + prompt tasks. 3D Consistency = DROID-SLAM reprojection error; Photometric Consistency = forward-backward flow AEPE; Camera Control = pose error vs. target trajectory; Style Consistency = Gram-matrix diff first vs last frame. | Found video models lag 3D methods mainly on camera control (best video model 40.22), worse on long and outdoor sequences. | High conceptually. Closest public analogue to "does the model follow my path and keep 3D structure." |
| EditBoard [S6, AAAI 2025] | Text-based video editing: 4 dimensions, 9 automatic metrics, 3 new fidelity metrics. | Says prior editing evals are "limited and inconsistent" and hide per-task performance behind one score. | Medium. Built for editing, but dimension names not on abstract page. |
| Common editing metrics [S7, TokenFlow 2023] | Warping error: RAFT flow on the original video, warp edited frames, measure error. CLIP frame consistency: cosine sim of consecutive frame embeddings. | TokenFlow cannot do edits needing structural change; artifacts when correspondences fail. CLIP sims are coarse and ignore geometry. | High for warping error (uses the source video's motion, exactly the v2v promise). |
| FVD [S8, CVPR 2024] | Distribution distance in video-classifier feature space. | Content-biased: weakly sensitive to large temporal corruption; static videos can lower FVD; "conflict with human perception occasionally." | Poor. Needs many samples, no per-clip pairing with the input. |
| MEt3R [S9, CVPR 2025] | Pose-free multi-view consistency: DUSt3R point maps warp DINO features between two frames; gives score + error maps. Code public. | Pairwise only; depends on DUSt3R reconstruction quality; shown on RealEstate10K. | High for geometry, but heavier setup (GPU, model weights). |
| Artificial Analysis Video Editing Arena [S10, 2026-06-22] | Blind pairwise human votes, Elo. Six models incl. Runway Aleph 2.0 and Seedance 2.0; restyle, relight, background change, physics, etc. | Preference only, not API stability, price, latency. "No single model dominates editing yet." Current standings not verified. | Medium. Tells you what people prefer, not whether geometry held. |
| Arena Video Edit Arena [S11, 2026-03-31] | Anonymous side-by-side community votes. | Leading models shown only in an image (not verified). | Same as above. |
| Physics-IQ [S12, 2025-01] | 396 videos, physics continuation. Finding: physical understanding "severely limited, and unrelated to visual realism." | T2V/I2V continuation, not editing. | Supports keeping "realism" and "physics/structure" as separate rubric axes. |

Takeaway: public benchmarks are mostly T2V and reference-free. Few score "did the output preserve the input's 3D structure and camera path," which is Helen's core question.

## 2. Recommended single automated metric: input-flow warping error

Why this one: it is the standard editing metric [S7], it uses the input render's motion as the reference (the v2v promise), and it catches flicker, morph and pop, which complements a human temporal score without duplicating the geometry overlays.

Recipe (a few hours, Python):
1. Decode input render and each output to frames at the same fps and resolution (resize/crop outputs to match input; check for model-side cropping first).
2. Compute optical flow on the INPUT pair (t, t+1) with RAFT (torchvision `raft_large`). Input is a clean render, so flow is reliable. If the 3D tool can export ground-truth motion vectors, use those instead.
3. Occlusion mask: forward-backward flow check on the input; drop pixels that fail.
4. Warp OUTPUT frame t+1 back to t with that flow; score = mean L1 (or 1 minus SSIM) over unmasked pixels. Average over frames. Lower = more consistent with the intended motion.
5. Report a floor: run the same pipeline on the input video itself (ideally near 0) and, if available, on a real phone walkthrough of the room.
6. Plot per-frame error over time; spikes map to pop/flicker events, a rising trend maps to drift.

Pitfalls:
- Rewards blur and low detail (like VBench's static "cheat" [S1]). Pair with a sharpness or realism check, never use alone.
- Legit view-dependent changes (specular reflections, new realistic lighting) count as error. Mask windows/mirrors or report with and without.
- If a model ignores the camera path (path_ignored), the input flow no longer applies and error explodes. That is a signal, but label it separately from flicker.
- Textureless walls give near-zero error even if geometry is wrong. This metric is temporal, not geometric; keep landmark overlays for geometry.
- n is tiny (3 models, few clips). Report raw values and rank, not significance claims.

Optional next step if time: MEt3R on frame pairs for a geometry-aware score [S9], or WorldScore-style DROID-SLAM reprojection [S5].

## 3. World models and "simulation"

| Lab | Definition / claim | Source |
|---|---|---|
| Runway | World model = "an AI system that builds an internal representation of an environment" to predict events. GWM-1 (2025-12-11) is "built to simulate reality in real time": autoregressive, frame by frame, action-conditioned (camera pose, robot commands, audio). GWM Worlds claims spatial consistency over long movement: "Turn around, and what was behind you is still there." Variants (Worlds, Avatars, Robotics) are separate post-trained models; aim is to unify. Up to 2 min, 720p. | [S13] |
| Runway | Aleph (2025-07-25): "in-context video model" for add/remove/transform objects, new camera angles, style and lighting changes. Aleph 2.0 details not verified on a Runway page. | [S14] |
| Google DeepMind | World models = "AI systems that can use their understanding of the world to simulate aspects of it." Genie 3 (2025-08-05): consistency is emergent, no explicit 3D representation (contrasted with NeRF / Gaussian Splatting); consistent for several minutes; visual memory up to ~1 minute. Limits: real-world locations not geographically accurate, few-minute interactions. | [S15] |
| OpenAI | Sora "world simulators" framing: page blocked (403), not verified. | n/a |

Painting plausible frames vs. keeping a consistent scene:
- A frame painter optimizes each new frame to look plausible given recent frames and the prompt. Errors show up when the camera revisits or moves past something.
- A scene-consistent model behaves as if one 3D world exists: geometry, object identity and lighting stay fixed while only the viewpoint changes. Genie 3 and GWM both claim this emerges without explicit 3D [S13, S15]. WorldScore shows video models still trail explicit 3D methods on 3D consistency and camera control [S5].

Observable signs of scene understanding in a 5 s walkthrough:
- Parallax is correct: near furniture moves faster than far walls; straight wall edges stay straight.
- Object permanence: something occluded by a sofa comes back with the same shape and position.
- Scale constancy: a chair does not grow or shrink relative to the door as the camera passes.
- Lighting tied to the room: window light direction and shadow placement stay fixed in world space, not in screen space.
- View-dependent effects move correctly: reflections and specular highlights shift with the camera, textures do not.
- Path fidelity: the output camera follows the input trajectory (measurable with SLAM pose error, as WorldScore does [S5]).

## 4. Failure modes mapped to Helen's taxonomy

| Helen type | Reported evidence | Source |
|---|---|---|
| geometry, scale, opening | Video models weak on 3D consistency and camera control vs 3D methods; VLMs weak at 3D understanding, so automated judges miss it. | [S5], [S3] |
| placement, path_ignored | Camera control is the main video-model gap in WorldScore. Prompt non-adherence for camera moves in Aleph: third-party user reports only, not verified. | [S5] |
| identity, morph, drift | VBench Subject Consistency exists because identity drifts; VBench-2.0 adds Instance Preservation and identity dims. TokenFlow: when correspondences fail, artifacts follow. | [S1], [S3], [S7] |
| flicker | Prior methods show "severe jittering"; LDM decoder adds high-frequency flicker. | [S7] |
| pop | VBench-2.0 Instance Preservation (objects appearing/vanishing) is the closest formal dimension. | [S3] |
| hallucination | Instance Preservation and Commonsense dims [S3]; Genie 3 notes legible text mostly only when prompted [S15]. | [S3], [S15] |
| shadow, reflection, material | VBench-2.0 Physics includes Material and Thermotics; Physics-IQ: physics understanding unrelated to realism. | [S3], [S12] |
| render_look | No primary source found that names "still looks like a render" as a failure. Related: TokenFlow cannot make structural changes, so edits stay close to source. Not verified as a reported category. | [S7] |
| structure loss (general) | TokenFlow and similar structure-preserving editors trade editability for fidelity; FVD and CLIP scores would not catch it. | [S7], [S8] |
| resolution limits | Aleph default 5 s and auto-crop: from search snippet of a 403 page, not verified. GWM-1 720p cap [S13]. | [S13] |

## 5. Research-PM questions for this eval

1. Is there a realism vs. fidelity frontier? Does the most photoreal model also lose the most geometry, and does Physics-IQ's "realism unrelated to physics" [S12] hold for interiors?
2. Where in the clip do failures start? Does per-frame warping error rise after N frames (drift) or spike at occlusion events (pop), and does that match the "degrades after a few seconds" anecdote?
3. Which failure types does a cheap automated metric catch vs. miss? Agreement rate between warping-error spikes and human flicker/morph/pop tags tells a research team whether the metric is worth scaling.
4. Does the clean 3D render input help or hurt? Do models over-preserve render textures (render_look) vs. hallucinate new materials? That is a data/conditioning question public benchmarks do not ask.
5. Does a model keep one room or repaint each frame? Revisit tests (pan away and back) directly probe the "world model" claims in [S13, S15] on a real user task.
6. Which failures matter to the user? Rank types by how much they break the "is this my living room" judgment; a research team may be optimizing dims that users ignore.
7. How stable are results across seeds and prompts? With 3 models and few clips, is the ranking robust, and what n would a team need before shipping a claim?
8. What would an arena miss? Preference votes [S10, S11] reward looks; does Helen's fidelity ranking disagree with likely preference ranking, and why?

## Sources (opened 2026-11-03)
- S1 VBench: https://arxiv.org/html/2311.17982 [2023-11-29]
- S2 VBench++: https://arxiv.org/abs/2411.13503 [2024-11-20]
- S3 VBench-2.0: https://arxiv.org/html/2503.21755v2 [2025-03]
- S4 EvalCrafter: https://arxiv.org/abs/2310.11440 [2023-10-17, v3 2024-03-23]
- S5 WorldScore: https://arxiv.org/html/2504.00983v2 [v2 2025-11-29]
- S6 EditBoard: https://arxiv.org/abs/2409.09668 [2024-09-15, v2 2025-01-19]
- S7 TokenFlow: https://arxiv.org/html/2307.10373 [2023-07]
- S8 On the Content Bias in FVD: https://arxiv.org/abs/2404.12391 [2024-04-18]
- S9 MEt3R: http://vip.mpi-inf.mpg.de/met3r and https://arxiv.org/abs/2501.06336 (search snippet only for arXiv) [CVPR 2025]
- S10 AA Video Editing Arena (AlphaSignal coverage): https://alphasignal.ai/news/artificial-analysis-launches-a-video-editing-arena-pitting-6-frontier-models [2026-06-22]
- S11 Arena March 2026 update: https://arena.ai/blog/march-2026-arena-updates/ [2026-03-31]
- S12 Physics-IQ: https://arxiv.org/abs/2501.09038 [2025-01-14]
- S13 Runway GWM-1: https://runway.com/research/introducing-runway-gwm-1 [2025-12-11]
- S14 Runway Aleph: https://runway.com/research/introducing-runway-aleph [2025-07-25]
- S15 DeepMind Genie 3: https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/ [2025-08-05]
