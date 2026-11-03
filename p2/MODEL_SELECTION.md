# Model selection research: Astra 3D walkthrough to photoreal (v2v)

Researched 2026-11-03. Task: 5 s eye-level camera path, restyle to photoreal, keep geometry and camera motion, optional 1 real room photo as material/style reference. All models run inside Runway's picker.

Key source for the case study's "Why these models" section. Decided with Helen on 2026-11-03:
- Arms: Aleph 2.0 (Runway-native), Seedance 2.5, Gemini Omni Flash. Swap rule: if the Alibaba tab shows Wan 3.0 with editing (or MiniMax H3), it replaces Gemini Omni Flash. Checked in pre-flight, before the freeze.
- Selection order: functional (takes an input video) first, then popularity (leaderboards, adoption), then runs in the picker, then cheaper.
- Every arm at 720p, 5 s, the input's aspect ratio (Gemini Omni Flash is 720p only).
- Budget: about 2,075 credits at the prices below (5 clips per model). Helen upgrades to Pro for one month.
- Popular models outside the picker are a stated limit, not an extra arm.
- Aleph's low leaderboard rank is stated on the page as prior evidence against H1.
- Open: Aleph's keyframe step uses a selectable image model (Nano Banana Pro, GPT Image 2, Gen-4 Image). Which one is frozen in the protocol.

## Recommendation

| Slot | Model (picker name) | Why |
|---|---|---|
| Runway-native | **Aleph 2.0** (Edit videos) | Runway's only v2v editing model. Keyframe-edit workflow: restyle one frame (optionally with a reference image), Aleph propagates it while "preserving everything else". Accepts 2 to 30 s, 480p to 1080p input. |
| Non-Runway #1 | **Seedance 2.5** (ByteDance) | Top-tier on both video-editing leaderboards (AA #2 to 4 tied, Arena #2). Top usage on the one adoption tracker found. Runway doc confirms Edit mode, matches input length and aspect ratio, up to 30 image refs, and explicitly says video refs can "keep the structure while swapping out other elements". |
| Non-Runway #2 | **Gemini Omni Flash** (Edit Video tag) | Arena video-edit #4 (gemini-omni-flash). Its 1.1 version is AA video-editing #2 to 4 tied. Runway doc confirms Edit Video mode, input up to 10 s, optional reference image. Output fixed at 720p. |

Runner-up: Kling 4.0 (picker shows Edit Video + References), but it has no leaderboard placement yet and no Runway doc found. Grok Imagine (Edit Video) ranks #7 on Arena video-edit, but its edit input is capped at about 8.7 s and 720p (third-party docs), and no Runway edit doc was found.

**Caveat on Gemini:** in Helen's picker, "Gemini Omni 1.1 Flash" shows Text/Image to Video + References only (no Edit Video). "Gemini Omni Flash" shows Edit Video. The leaderboard entry that ranks highest (AA) is 1.1. The Arena entry (gemini-omni-flash) appears to be the one with Edit Video in Runway. Use **Gemini Omni Flash**, not 1.1, for the v2v run, and note that the 1.1 AA rank may not transfer.

## 1. Popularity evidence

| Model | AA Video Editing (v1.1) | Arena Video Edit (Aug 26, 2026) | AA Image-to-Video | Usage (muapi, 7-day) |
|---|---|---|---|---|
| Wan 3.0 (Alibaba) | #1, 1196 | #1, 1414 | #9 | #7 (631 req) |
| Seedance 2.5 | #2 to 4, 1152 | #2, 1410 | #1, 1157 | #1 (6,315 req, 28.4%) |
| Hyperflow H3 | #2 to 4, 1151 | not listed | #5 | not verified |
| Gemini Omni Flash 1.1 | #2 to 4, 1149 | not listed (1.1) | #14 | not verified |
| gemini-omni-flash | not listed | #4, 1367 | not listed | not verified |
| MiniMax H3 | #5, 1123 | #3, 1392 | #4 | not verified |
| Seedance 2.0 | #6 to 8, 1079 | #5, 1365 | #3 | #2 (5,420 req) |
| Grok Imagine Video | not listed | #7, 1258 | 1.5: #13 | Grok Imagine #8 (603 req) |
| Kling (3.0 Omni / O3 Pro) | #10, 1000 (anchor) | O3 Pro #8, 1255 | not top 15 | Kling 3.0 #3 (1,502 req) |
| **Kling 4.0** | not listed | not listed | not listed | not verified |
| Aleph 2.0 | #9, 1009 | Gen-4 Aleph (older) #10, 1182 | n/a | n/a |
| Veo 3.1 | not listed | not listed | not verified (T2V #22) | #6 (658 req, T2V) |

Notes: Aleph 2.0 ranks low on both editing boards. That is a real finding to put in the writeup, not hide. AA rank ranges mean statistical ties. The muapi stats cover one API marketplace's request volume, not overall market share. No credible cross-platform usage-share source was found.

## 2. Functional fit (from Runway help center unless noted)

| Model | Input video (v2v) | Reference images | Duration | Resolution | Aspect ratio | Structure preservation |
|---|---|---|---|---|---|---|
| Aleph 2.0 (Edit Studio) | Yes, 2 to 30 s, 24 to 30 fps, 480p to 1080p, 10 cuts max | Yes, on keyframe edit (refs for "characters, products, objects, or styles") | Matches input, up to 30 s | Input up to 1080p | "Conventional" ratios only | Designed to change only what's asked and preserve the rest. Restyle is a listed use case. |
| Seedance 2.5 | Yes (Edit and Extend modes); up to 10 ref videos of 30 s max each | Up to 30 images (50 refs total) | Edit matches input length (4 to 30 s for generation) | 480p, 720p, 1080p | Edit matches input | Doc: video refs can "keep the structure while swapping out other elements" |
| Gemini Omni Flash | Yes (Edit Video), under 100 MB and 10 s max | Edit: 1 optional ref image (Frames mode: up to 10) | 3 to 10 s | 720p only | Auto 16:9 or 9:16 | Google doc tip: add "Keep everything else the same" |
| Gemini Omni 1.1 Flash | In picker: no Edit tag. Google API supports `edit` task on gemini-omni-1.1-flash. Runway v2v: not verified | Yes (References tag) | not verified in Runway | not verified in Runway | not verified in Runway | not verified |
| Kling 4.0 | Per fal (citing Kling release notes): edit 1 primary + up to 4 clips, 3 to 30 s each, 30 s combined. Runway doc: not verified | Up to 10 (15 refs total) | 3 to 30 s | 720p, 1080p, 4K | 21:9, 16:9, 1:1, 9:16, Auto | not verified |
| Grok Imagine (base) | Per Vercel docs: edit, output matches input, capped at 720p. Input cap about 8.7 s (third-party). Runway doc: not verified | not verified for edit | not verified | 720p cap | Matches input | not verified |
| Grok Imagine 1.5 / 1.5 Lite | No (T2V and I2V only per Runway doc) | Up to 7 | up to 15 s | 480p to 1080p | 7 ratios | n/a |
| Veo 3.1 | No v2v tag in picker (Keyframes, Audio) | not verified | not verified | not verified | not verified | n/a |

Credit costs (from Runway help center pages, verify in app):
- Aleph 2.0 / Edit Studio: 28 credits/s (56 minimum). A 5 s clip is about 140.
- Seedance 2.5: 1080p 68/s + 34 per input-video second. 720p 30/s + 15/s. 480p or Draft 20/s + 10/s. A 5 s clip at 720p is about 225. Draft is about 150.
- Gemini Omni Flash Edit: 10/s + 1 per input second + 1 per extra reference. A 5 s clip is about 56.

## 3. Runway-native confirmation
- Current name: **Aleph 2.0**, launched May 21, 2026 with Edit Studio. Runway calls it "in-context video editing model": edit one frame and the rest of the video follows. It edits clips up to 30 s at 1080p and is on all paid plans (desktop web).
- Workflow: upload video, pick a keyframe (the widest shot for scene or material changes), prompt plus optional reference image, preview the keyframe, then generate. The keyframe image model is selectable (Nano Banana Pro, GPT Image 2, Gen-4 Image). Optional "Extra motion" prompt. Ranged edit available. Explore mode supported.
- Gen-4.5, Gen-4 and Gen-4 Turbo are I2V/T2V only, and Ruby and Enhance Frame Rate are post-processing, so none of them fit as the v2v candidate.

## 4. Stated limits
- **Popular editing models not in the picker (as seen):** Wan 3.0 (#1 on both editing boards), MiniMax H3 (#3 Arena, #5 AA), Hyperflow H3, HappyHorse-1.0. Alibaba and MiniMax tabs exist but their models were not seen. **Check the Alibaba tab for Wan 3.0 and the MiniMax tab for H3 before freezing.** If either has edit support in Runway, it outranks Gemini Omni Flash on the evidence.
- Kling 4.0 is too new (GA mid to late Oct 2026, per third-party sources) for leaderboard placement. Its Runway edit specs are not verified.
- The AA leaderboard pages show no update date (accessed 2026-11-03). Arena's board is dated Aug 26, 2026 and predates Kling 4.0 and Gemini Omni 1.1 entries.
- Runway's "Available Models" article was last updated 2026-03-13 and is stale versus the picker.
- Leaderboard prompts are general edits, not 3D-render-to-photoreal. Treat ranks as priors, not task results.

## Sources (opened)
1. Artificial Analysis, Video Editing leaderboard v1.1. https://artificialanalysis.ai/video/leaderboard/video-editing (no page date, accessed 2026-11-03)
2. Artificial Analysis, Image-to-Video leaderboard. https://artificialanalysis.ai/video/leaderboard/image-to-video (no page date, accessed 2026-11-03)
3. Artificial Analysis, Text-to-Video leaderboard. https://artificialanalysis.ai/video/leaderboard/text-to-video (no page date, accessed 2026-11-03)
4. Arena (formerly LMArena), Video Edit leaderboard. https://arena.ai/leaderboard/video-edit (dated Aug 26, 2026)
5. muapi.ai, Video Model Rankings (7-day API requests). https://muapi.ai/rankings/video (rolling, accessed 2026-11-03)
6. Runway, "Introducing Aleph 2.0 and Edit Studio". https://runway.com/news/introducing-aleph-2-and-edit-studio (May 21, 2026)
7. Runway Help, "Creating with Edit Studio". https://help.runwayml.com/hc/en-us/articles/51683104370451 (updated 2026-08-24)
8. Runway Help, "Aleph 2.0 Prompting Guide". https://help.runwayml.com/hc/en-us/articles/52150503729171 (updated 2026-06-30)
9. Runway Help, "Creating with Seedance 2.5". https://help.runwayml.com/hc/en-us/articles/53542207042323 (updated 2026-11-01)
10. Runway Help, "Creating with Gemini Omni Flash". https://help.runwayml.com/hc/en-us/articles/53031657806611 (updated 2026-08-24)
11. Runway Help, "Creating with Grok Imagine 1.5". https://help.runwayml.com/hc/en-us/articles/53995376768147 (updated 2026-11-01)
12. Runway Help, "Available Models on Runway". https://help.runwayml.com/hc/en-us/articles/48649877897107 (updated 2026-03-13)
13. Runway, Gemini Omni model page. https://runway.com/product/models/gemini-omni (no date)
14. Google AI Studio docs, Gemini Omni Flash. https://aistudio.google.com/docs/omni (no date shown)
15. fal, "What is Kling 4.0?" https://fal.ai/learn/tools/what-is-kling-4-0 (Sep 30, 2026; says it draws on Kling release notes)
16. Vercel AI Gateway, Video Editing (Grok Imagine Video). https://vercel.com/docs/ai-gateway/capabilities/video-generation/video-editing (last updated 2026-09-08)

Not verified: Runway help docs for Kling 4.0, Gemini Omni 1.1 Flash, base Grok Imagine edit, and Veo 3.1. Runway help pages were read via the Zendesk article JSON because the HTML returned 403.
