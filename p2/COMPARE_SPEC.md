# Compare-across-models: problem, market read, prototype shape (T38 / HEL-104)

Status: DRAFT for Helen's review, 2026-11-04. No code yet. Nothing here changes the frozen P1 protocol (1e24e9e) or how P2 clips are scored.

## 1. The user problem

**Who:** someone who needs a video or image result for a real job and has more than one Runway model that could do it. Runway's own model router pitch says teams should not have to "act as model researchers". Today they still do, at least while deciding.

**The pain, from my own P2 work:**
- I ran the same start frame through three models (Gen-4.5, Seedance, Gemini Omni 1.1 Flash) and had to track the differences by hand: build log rows, a four-criterion rubric, side-by-side clips, my own notes.
- The models did not lose on one axis. Gemini looked most like real footage but invented a side table (H1). Gen-4.5 got the stools wrong where Gemini got them right. Seedance cost 150 credits against 51 for Gemini and I would have picked Gemini (H2).
- So "which model is best" has no single answer. It depends on which dimension matters for this shot: matching the plan 1:1, looking real, holding the room, or cost. A single quality number hides exactly the trade-off I needed to see.
- I only found the trade-off after spending credits on all three. A user who has not run all three has no way to know it before committing.

**Job to be done:** "Before I commit a shot, let me see what each eligible model would do to it, in terms of the things I care about, and remember my choice."

## 2. What Runway already ships (sources fetched 2026-11-04)

| Existing piece | What it does | What it does not do |
|---|---|---|
| Media Router (Runway Dev, launched July 2026) | One call routes across Runway and third-party models. Three dials: cost, latency, quality. Allow and deny lists, per-generation price cap. Response reports which model ran, why and the cost. | Does not show outputs from competing models. Quality is Runway's own ranking data, not the user's criteria. Per its own docs there is no feedback loop from the user's verdicts. |
| Router dry run | Reports which model a config would pick and why, with nothing generated and no cost. | Validates the routing decision, not output quality. |
| "Evaluate" step on dev.runway.com | One line: run the same prompt across models, score by quality, speed and cost before committing. | Landing page gives no screens or steps. I could not confirm whether it is UI or API, or whether it has side-by-side clips or a diff. **Needs a check in the dev portal.** |
| Router evaluation post | 250 image-to-video prompts, 10 categories, double-blinded. Quality-optimized router 77% usable vs 78% baseline at 29% lower cost per clip. | "Usable" is not defined and the judge is not named. Aggregate across a benchmark, not your shot. Vendor-authored, one baseline. |
| In-app Agent "Optimize generations" (Quality / Cost) | The setting I used in P1. | Model chosen is not shown to the user (P1 finding, `model_shown` = not shown). |

Sources: [Introducing Runway Media Router](https://runway.com/news/company-news/introducing-runway-media-router), [Model Routers docs](https://docs.dev.runwayml.com/model-routers/), [Evaluating the router](https://runway.com/news/developers/evaluating-runway-model-router), [Runway Dev MCP](https://runway.com/news/company-news/runway-dev-mcp), [dev.runway.com](https://dev.runway.com/). A third-party summary of the router is at [digitalapplied](https://www.digitalapplied.com/blog/runway-media-router-generative-media-model-routing); treat its criticisms as opinion.

## 3. The gap

1. **Router is a developer API.** The in-app creator who is "still learning which model to use" is the person in my story, and the router surface I found is not built for them.
2. **Quality is one dial, and the dimensions trade off.** My data shows realism and plan fidelity pulling apart on one shot. The dial cannot express "keep my furniture 1:1, I do not care if it looks a bit CG".
3. **No per-shot, per-criterion diff.** Even if Evaluate exists, I could not find it showing why two clips differ.
4. **No learning from the user's verdict.** The router metadata is an audit trail. My verdict ("Gemini was close enough") goes nowhere.

## 4. Improve or net-new?

**Recommendation: improve, framed as an extension of the router, not a new product.** A net-new standalone "model comparison tool" duplicates the Evaluate pillar, and competing with something I have not seen is weak. An extension is something a research PM could actually propose:

> **Preview before you route.** For one shot, run it on 2 to 3 eligible models, show a structured diff on the dimensions the user cares about, let them set what matters, and save the verdict as the router's preference for that kind of shot.

Two net-new ideas inside it, in order of how much I believe in them:
- **User-defined dimensions replace the quality dial.** Plan fidelity, realism, room consistency, cost, each weightable. Grounded in my H1.
- **Verdicts calibrate the router.** "Acceptable / not acceptable" per clip, which is my gut-call field, becomes the signal. Grounded in my H2.

Not proposed: a new model, a new benchmark, anything needing live generation.

## 5. Prototype shape (zero new credits)

Static page over data I already have. No Runway calls.

- **Input:** P2 outputs for b01 to b03 on three models, `build_log.csv`, rubric criteria, credits and minutes per clip.
- **View 1, side-by-side:** three clips synced to one scrubber.
- **View 2, diff chips:** per model, per criterion, a pass or flag with the reason ("invented side table", "stools wrong"), taken from my logged notes. Computed from the log, not guessed by a model.
- **View 3, weights:** sliders for plan fidelity, realism, room consistency, cost. Recommended model updates live. Shows what a one-dial router would have picked next to it.
- **View 4, save verdict:** acceptable yes or no, written to a local file, shown as "the router would remember this".

Cut line: Views 1 and 3 are the minimum that tells the story. 2 and 4 only if time allows.

## 6. Risks and honest limits

- n is 2 clips per model. The prototype demonstrates the interface idea; it does not prove which model is better.
- I have not seen Evaluate. If it already does view 2 and 3, the pitch becomes "extend it to user-defined dimensions and verdict learning", which is a smaller but still defensible claim. Check it before the spec is final.
- Sources are public pages plus search summaries, some third-party. Router launch dates and numbers come from Runway's own posts.
- Not tested with a user other than me. One interview with a friend who makes AI video would help.

## 7. Decisions needed from Helen

1. Improve-the-router framing (recommended), or a standalone tool?
2. Is the target user the in-app creator, or the developer on Runway Dev?
3. Are View 1 and 3 enough for the first cut?
4. Who checks Evaluate in the dev portal, and when? (Needs your login, so it is yours.)
