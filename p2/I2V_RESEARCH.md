# Image-to-video research for the Astra walkthrough eval (2026-11-03)

Task: one eye-level Astra still of the living room (plus optionally one real photo as a material reference) in, a 5 s photoreal walkthrough out, generated in the Runway app. Every claim below comes from a page opened on 2026-11-03 (sources at the end). "Not verified" means I could not confirm it.

**Access note:** help.runwayml.com returned HTTP 403 on every request, so I could not read any Runway help-center article. I did not try to work around it. Runway specs below come from runway.com (pricing, changelog, research pages) and Runway's developer docs. Check them in the app.

## 1. Leaderboards (re-verified, not copied)

| Model in picker | AA image-to-video (29 models) | Arena image-to-video (48 models, updated Sep 21 2026) | Arena text-to-video (48 models, updated Sep 21 2026) |
|---|---|---|---|
| Seedance 2.5 | #1 (1157) | #4 (1477, 720p) | #7 |
| Seedance 2.0 | #3 (1137) | #5 (1475, 720p) | not checked |
| MiniMax H3 (768p) | #4 (1131); H3 Max is #8 | #1 (1495) | not checked |
| Wan 3.0 (Alibaba) | #9 (1111) | #3 (1480) | not checked |
| FLUX 3 video (BFL) | #11 (1070) | #9 (1449) | not checked |
| Grok Imagine 1.5 | #13 (1051); 1.5 Lite is #19 | #8 (1456, 720p) | #4 (preliminary) |
| Gemini Omni 1.1 Flash | #14 (1046) | #2 (1488, only 3.7k votes) | #1 |
| Gemini Omni Flash (1.0) | not listed | #6 (1465) | #2 |
| Veo 3.1 | #21 (955); Fast is #22 | #13 to #17 (Audio variants, 1372 to 1398) | #12 to #15 |
| Kling 4.0 | not listed (Kling 3.0 Omni Pro is #17) | not listed (Kling 3.0 Pro is #19) | not listed |
| Runway Gen-4.5 | not listed | not listed (only Gen-4 Turbo, #47 of 48) | #27 (1225) |
| Gen-4 / Gen-4 Turbo | not listed | Gen-4 Turbo #47 | not listed |

- The previous pass's AA ranks hold. New detail: Kling is not just outside the top 15. Kling 4.0 is missing from every board, and Kling 3.0 sits at #17 to #19.
- **Gen-4.5 has no public image-to-video rank.** Its only public rank is Arena text-to-video #27. AA's text-to-video board no longer lists any Runway model. Runway's Dec 2025 launch post claimed #1 on AA text-to-video, so that claim is out of date.
- Not in the picker but in the AA top 10: Utopai X (#2, no API), Hyperflow H3 (#5), HeyGen Video 1 (#6), P-Video-2-Pro (#7), Agnes-Video-2.5 (#10). HiDream-O1 is #7 on Arena (preliminary).

## 2. What each model can do in Runway

Rates are from Runway's API pricing page, where 1 credit is $0.01. Where the app pricing page also lists a model, the numbers match (Gen-4.5 is 60 credits per 5 s, i.e. 12/s; Kling 4.0 1080p is 118 per 5 s, i.e. ~23.5/s). **All rates come from those pages; check them in the app.**

| Model | Start image | End frame / keyframes | Reference images | Camera control | Durations | Resolutions | Credits/s at 720p / 1080p |
|---|---|---|---|---|---|---|---|
| Gen-4.5 | Yes (changelog, Jan 21 2026) | Not verified. The changelog mentions first frame only, and the launch post said keyframes were "coming". | Not verified | Prompt only. No camera-control UI has been announced for Gen-4.5 (latest camera-control changelog entries are from 2024). | API example uses 5 s. Third-party sites say 2 to 10 s. | API example 1280:720. Third-party sites say 720p. | 12 (no resolution split listed) |
| Gen-4 Turbo | Yes | Not verified | Not verified | Not verified | Not verified | Not verified | 5 |
| Aleph 2.0 | Edits video, not image-to-video | "Keyframe-guided control" (dev docs) | Not verified | n/a | Not verified | Not verified | 28 (56-credit minimum) |
| Seedance 2.5 | Yes | First frame, last frame and reference images (changelog, Aug 11, for MCP) | Yes, free | Prompt only (not verified) | Up to 30 s, or auto | 480p, 720p, 1080p; draft mode at 480p | 30 / 68 (80-credit minimum); draft billed at the 480p rate (20) |
| Seedance 2.0 | Yes | Keyframes listed for 2.0 Mini/Fast (MCP) | Not verified | Not verified | Adjustable | 480p to 4K | 30 / 40 (Fast 24 at 720p, Mini 15 at 720p) |
| Kling 4.0 | Yes | "Frames" input (dev docs). Third-party hosts say first and last frame plus up to 10 keyframes. Not verified in Runway. | Image and video references | Not verified | 3 to 30 s | 720p, 1080p | 12.56 / 18.8 discounted until Nov 30 (list price 15.7 / 23.5); audio always on |
| Gemini Omni 1.1 Flash | Yes | Not verified | Yes, +1 credit each | Not verified | Not verified | 360p, 720p, 1080p, 4K | 10 / 15 |
| Veo 3.1 | Yes | Your picker shows "Keyframes". Not verified in docs. | Not verified | Not verified | Not verified | Not verified | 20 without audio, 40 with (no resolution split); Fast 10 / 15 |
| Grok Imagine 1.5 | Yes | Not verified | Yes, +1 credit each | Not verified | Not verified | 480p, 720p, 1080p | 16 / 29 (Lite 3 / 14) |
| Wan 3.0 (Alibaba tab) | Yes | Not verified | Image, video and audio references | Not verified | 2 to 30 s | 480p to 1080p | 10 / 20 |
| MiniMax H3 Max (MiniMax tab) | Yes | **First and last frame** (dev docs) | Not verified | Not verified | Not verified | 480p, 768p | 8 at 768p, no 1080p |

- Aspect ratios: none of the pages I could open list them per model. Choose the ratio in the app to match the Astra still. Kling 4.0's output ratio follows its input frames (third-party hosts; not verified in Runway).

## 3. GWM-1 and GWM Worlds

| Item | What I found |
|---|---|
| What it is | GWM-1 (Dec 11 2025) is an autoregressive, real-time world model built on Gen-4.5. Its variants are Worlds, Avatars and Robotics. GWM Worlds 2 is a research preview published Sep 3 2026. |
| Input | GWM-1 Worlds takes a prompt or an image reference (TechCrunch). Worlds 2 takes a text "genesis prompt" plus a first frame, optionally prefilled from a video. The Worlds 2 page does not say whether you can upload your own photo as that frame, and it supports no image references beyond the first frame. |
| Camera | Continuous per-frame camera translation and rotation. The demo steers with the mouse. WASD controls are not verified. |
| Duration and resolution | GWM-1: up to 2 min at 720p. Worlds 2: unbounded, 720p at 24 fps with 48 kHz audio. |
| Export as video | Not mentioned on any page I opened. Not verified. |
| Access | The GWM-1 page links to app.runwayml.com/live and to an access-request form. Worlds 2 is a research preview reached through a contact form. Neither page describes self-serve access. |
| Credits | Only GWM Avatars has a published rate (~0.33 credits/s). Worlds is not priced on the pricing page or in the API docs. Not verified. |
| Known limits | Fast camera rotation degrades detail, texture and geometry, and long-term memory is imperfect (Worlds 2 page). |
| Non-Runway world models in Runway | None found in the changelog, the pricing page or the dev-docs model list. |

**Implication:** treat GWM as a probe. If Helen can open Worlds in her app, can upload the Astra still as the first frame, and can export a 5 s clip, it is a strong "Runway-native" arm because it gives real camera control. If any of those three fails, record that as a finding and leave it out of the scored arms.

## 4. Runway prompting guidance

- I could not read Runway's own Gen-4.5 prompting guide (help center returned 403).
- From Runway's own pages:
  - The Gen-4.5 launch post lists known failure modes: objects appearing or vanishing (object permanence), effects before causes, and actions succeeding too often. Its sample prompts write camera moves in plain language (pan, tracking, orbit, handheld), which suggests camera control is prompt-based.
  - Runway's Architecture & Design page recommends animating a static render, trying material variants first with Vary Image, using References to Video, and chaining steps in node-based Workflows. It has no walkthrough-specific advice.
- Interior or real-estate guidance from Runway itself: none found.

## 5. Failure modes and mitigations for interior walkthroughs

| Failure | Where documented | Mitigation |
|---|---|---|
| Inventing unseen areas (rooms, walls behind camera) | Kling: "can't add a room, reveal what's off-camera" | Keep the camera inside the still's frustum. Use a push-in or a short lateral move, not a turn. |
| Walls bending, furniture warping, countertops distorting | Kling (aggressive motion, long clips); Worlds 2 (fast rotation) | One slow move, 3 to 5 s, no orbits or swoops |
| Objects appearing or vanishing (furniture morphing) | Gen-4.5 launch post (object permanence) | Avoid occluding moves. Inspect each clip frame by frame. |
| Viewpoint drift, camera ignoring the instruction | Worlds 2 (memory); Gen-4.5 has prompt-only camera control | State one camera verb plainly. Pin the end pose with a last frame where the model supports it (Seedance 2.5, MiniMax H3 Max; Kling 4.0 and Veo 3.1 not verified). |
| Materials drifting from the real room | General (no source) | Pass the real photo as a reference image where supported (Seedance 2.5, Gemini Omni 1.1, Grok 1.5, Wan 3.0) |
| Wasted credits | n/a | Draft at 480p first (Seedance 2.5 draft is billed at the 480p rate). Match the aspect ratio to the Astra still. |

- Keyframe caution: an end frame is a second invented image. If Astra renders a second still from a slightly forward camera position, use that as the last frame. Then both ends are plan-faithful, and the model only has to interpolate between them.

## 6. Recommendation

| Arm | Why | Risk |
|---|---|---|
| **Runway Gen-4.5** (required Runway arm) | Runway's flagship. 12 credits/s is the cheapest serious option. | No public image-to-video rank, start frame only, prompt-only camera. Expect drift; that is a finding in itself. |
| **GWM Worlds** (optional probe) | The only arm with real camera control | Research preview. Upload, export and credits are all not verified. Do not budget for it until it is confirmed in the app. |
| **Seedance 2.5** | #1 on AA image-to-video, #4 on Arena. First frame, last frame and free reference images. Cheap 480p draft mode. | Costs the most (30 credits/s at 720p, 80 minimum) |
| **Gemini Omni 1.1 Flash** | #2 on Arena image-to-video, #1 on Arena text-to-video, #14 on AA. Reference images. 10 credits/s at 720p. | The two boards disagree a lot (Arena #2 rests on only 3.7k votes). End-frame support not verified. |

- Alternates:
  - **Kling 4.0:** the newest Kling, with 3 to 30 s clips and possibly multi-keyframe input, but it is unranked everywhere and costs about 12.6 credits/s at 720p.
  - **MiniMax H3 Max:** first and last frame support and a high rank (AA #8, H3 #4), but 768p max. Use it only if it shows up in the MiniMax tab.
- For a "same conditions" comparison, run every arm at 720p, 5 s, the same prompt and the same aspect ratio, with a start frame only. Add a second condition (last frame plus reference image) only on the arms that support it.
- Popular models missing from the picker (or in tabs not yet checked): Utopai X, Hyperflow H3, HeyGen Video 1, P-Video-2-Pro, HiDream-O1. The Alibaba, MiniMax and Black Forest Labs tabs may hold Wan 3.0, MiniMax H3 and FLUX 3; check them in the app.

## Sources (all opened 2026-11-03)
- https://artificialanalysis.ai/video/leaderboard/image-to-video (AA-Video-I2V v2.1; no update date shown)
- https://artificialanalysis.ai/video/leaderboard/text-to-video
- https://arena.ai/leaderboard/image-to-video (updated Sep 21 2026)
- https://arena.ai/leaderboard/text-to-video (updated Sep 21 2026)
- https://docs.dev.runwayml.com/guides/pricing/ (no date shown; Kling 4.0 discount runs until Nov 30 2026)
- https://docs.dev.runwayml.com/guides/models/
- https://docs.dev.runwayml.com/guides/using-the-api/
- https://runway.com/pricing
- https://runway.com/changelog (latest entry Oct 27 2026)
- https://runway.com/research/introducing-runway-gen-4.5 (Dec 1 2025)
- https://runway.com/research/introducing-runway-gwm-1 (Dec 11 2025)
- https://runway.com/research/introducing-gwm-worlds-2 (Sep 3 2026)
- https://runway.com/solutions/industry/architecture-design
- https://techcrunch.com/2025/12/11/runway-releases-its-first-world-model-adds-native-audio-to-latest-video-model
- https://kling.ai/topics/ai-video-real-estate (Jul 10 2026)
- https://aistudio.google.com/docs/video (the Veo 3.1 preview models in the Gemini API shut down Oct 22 2026; effect on Runway not verified)
- Blocked (403, skipped): help.runwayml.com
