# How ChatGPT & Claude Actually Work — The System Design Behind the Blinking Cursor

*YouTube script · ~16–18 min · @codewithmuh · explainer, beginner→intermediate developers*

---

## [0:00] HOOK (0:00–0:18)

[B-ROLL: Screen recording of typing "Explain quicksort" into a chat box, hitting Enter, and the answer typing out word by word. Slow it down slightly.]

**Talk track:**
"Watch this cursor. You hit Enter, and the words come out one... at... a... time. Like the machine is typing live.

That's not a loading animation. It's not your wifi. Those words appear one at a time because — and I mean this literally — **they don't exist yet.** Each word is computed on the spot, and the machine can physically only make one at a time.

And here's the wild part: almost everything weird about ChatGPT and Claude — why they're slow, why they forget your conversation, why they make stuff up, why they cost a fortune to run — all of it comes from that one fact."

[ON SCREEN: "They literally do not exist yet."]

---

## [0:18] INTRO + WHAT YOU'LL GET (0:18–0:45)

**Talk track:**
"So in this video we're going to build the actual machine behind that blinking cursor. From the moment you press Enter, all the way down to the chip doing the math.

No PhD required. I'll start dead simple and we'll go deeper as we go. By the end you'll understand the real system-design that powers ChatGPT, Claude, and basically every big AI chat product — because honestly, they're all the same blueprint.

This is a great one for system-design interviews too. The full architecture diagram and notes are in the GitHub repo, link in the description."

[ON SCREEN: lower-third "github.com/codewithmuh — link in description"]

**Talk track (CTA seed):**
"If you like engineering explained properly and not dumbed into mush — subscribe. Let's go."

---

## [0:45] THE ONE WORD YOU NEED: TOKENS (0:45–1:30)

[B-ROLL: Text "Explain quicksort" splitting into chunks: "Explain" / "quick" / "sort" — roughly 3 tokens highlighted.]

**Talk track:**
"One piece of vocab first, because everything else hangs off it. A **token**.

A token is just a chunk of text. Roughly three-quarters of a word, or about four characters. 'Explain quicksort' is about three tokens. The model doesn't read letters or words — it reads and writes in these little fragments.

Here's the analogy: think of tokens like LEGO bricks for text. The model snaps them together one brick at a time. And — this matters — **everything** in this system is measured in tokens. Your rate limits, your memory, your bill, how many GPUs they need. All tokens."

[ON SCREEN: "token ≈ ¾ of a word ≈ 4 characters"]

---

## [1:30] THE BIG PICTURE: TWO FLEETS IN TENSION (1:30–3:00)

[ON SCREEN / DIAGRAM REVEAL — Step 1: Two boxes side by side. Left = big green "Web Tier". Right = small red "GPU Tier".]

**Talk track:**
"Okay, the big picture. When you talk to ChatGPT or Claude, you're really talking to two completely different systems bolted together.

On one side: a huge, cheap, basically-infinite **web tier**. Edge servers, gateways, auth, billing. This stuff scales up in seconds and costs pennies.

On the other side: a small, brutally expensive, painfully scarce **GPU tier**. Racks of accelerator chips running the actual model. This stuff scales in *minutes*, costs a fortune, and is the bottleneck for literally everything."

[B-ROLL: Animate the web tier ballooning huge and cheap; the GPU tier staying small with a "$$$" stamp.]

**Talk track:**
"Here's the analogy I want you to hold the whole video. The web tier is like the front of a restaurant — waiters, the host, the menus. You can hire ten more waiters in a minute, easy. The GPU tier is the kitchen, and there's exactly one chef who can only cook one dish at a time, and hiring another chef takes weeks and costs a million dollars.

Everything interesting in this design comes from that tension. The front is fast and unlimited. The back is slow, sticky, and capital-intensive."

[ON SCREEN: table — "Web tier: stateless / seconds / cheap / unlimited" vs "GPU tier: stateful / minutes / fortune / hard-capped"]

**Talk track:**
"And quick note — when I say 'the assistant,' I mean ChatGPT *and* Claude *and* any large LLM chat product. The model is different, but the serving architecture is basically identical. Same blueprint."

---

## [3:00] THE 3 SECONDS AFTER YOU PRESS ENTER (3:00–4:00)

[B-ROLL: Fast montage following a glowing packet: keyboard → globe icon (edge) → lock (auth) → meter (rate limit) → GPU rack → back to browser.]

**Talk track:**
"Let's speed-run what happens in the three seconds after you hit Enter. Don't worry about the details yet — this is the trailer, we'll watch the full movie after.

Your keystrokes fly to an edge server near you. You get authenticated. You get checked against a *token* budget — not just 'how many requests,' but 'how much work.' Then you get routed to a pool of GPUs that might already be holding your conversation. You get slotted into a batch **next to dozens of total strangers' chats.** Your whole prompt gets processed in one big parallel burst — that's called **prefill**. And then it drops into a slow, one-token-at-a-time grind called **decode**, and each token gets shipped to your screen the instant it's born."

[ON SCREEN: "prefill = read the prompt (fast, parallel)   |   decode = write the answer (slow, one token at a time)"]

**Talk track:**
"That's the whole story. Now let's actually build it."

---

## [4:00] THE FULL ARCHITECTURE — REVEALED PIECE BY PIECE (4:00–6:30)

[ON SCREEN / DIAGRAM REVEAL — start with ONLY the User box. We'll add one box at a time as I say it.]

**Talk track:**
"Here's the full system. I'm going to reveal it one box at a time so it never feels like a wall of arrows. Start with you — the user."

[DIAGRAM REVEAL — Step 2: add "Global Edge / CDN".]

"First stop: a **global edge server**. This terminates your secure connection close to you, so things feel snappy. Think of it as the closest door into the building."

[DIAGRAM REVEAL — Step 3: add "Regional API Gateway".]

"Then a **regional API gateway**. This is the policy checkpoint — the bouncer. Everything that decides 'are you allowed in, and how much' lives here."

[DIAGRAM REVEAL — Step 4: add "Auth" box.]

"**Auth.** It checks your API key — and by the way, those keys are stored *hashed*, never in plain text. It also figures out *which org or project* you are, because that's what gets billed."

[DIAGRAM REVEAL — Step 5: add "Rate Limiter (Redis)" with a "429" arrow back to user.]

"**The rate limiter** — and this is where an AI API is different from a normal web API. A normal API counts *requests*. But a 50-token request and a 50,000-token request are wildly different amounts of work. So this thing meters **tokens per minute**, not just requests per minute. Over budget? You get a **429, try again later**. It uses Redis as the shared source of truth so two servers can't both spend the same budget."

[ON SCREEN: "Normal API = count requests · LLM API = count *work* (tokens)"]

[DIAGRAM REVEAL — Step 6: add "Router".]

"**The router** picks which pool of GPUs you go to — based on the model you asked for, how big a context window you need, and even which kind of chip. Fun fact: Claude runs across AWS Trainium, NVIDIA GPUs, *and* Google TPUs."

[DIAGRAM REVEAL — Step 7: add "Orchestrator" in the center, with side-boxes "Safety", "Memory store", "Vector DB (RAG)".]

"**The orchestrator** is the brain of the operation. It assembles your prompt, runs safety checks, pulls in your conversation history, fires off any tools or document lookups, and manages the streaming back to you. Hold these three side-helpers — safety, memory, retrieval — we'll come back to each."

[DIAGRAM REVEAL — Step 8: add "LLM-aware Load Balancer" → "Inference Queue" → "GPU Cluster".]

"Then the request hits a **smart load balancer**, drops into an **inference queue**, and finally lands on the **GPU cluster** — the kitchen — where the actual model runs.

[DIAGRAM REVEAL — Step 9: animate tokens flowing back GPU → Orchestrator → User as 'SSE stream'.]

And tokens flow *back* out, through the orchestrator, streamed to your browser, while a **metering** service counts every token for your bill."

[ON SCREEN: full diagram now complete — hold for 3 seconds.]

**Talk track:**
"That's the whole machine. Now let's open up the most important box — the kitchen."

---

## [6:30] DEEP DIVE: INSIDE THE GPU — PREFILL vs DECODE (6:30–9:00)

[B-ROLL: Zoom into the "GPU Cluster" box until it fills the screen.]

**Talk track:**
"Every other 'design ChatGPT' video draws the GPU as one black box and moves on. We're not doing that, because *this is the box the whole system exists to feed.*

Remember those two words — prefill and decode? They're two totally different kinds of work happening on the same chip."

[ON SCREEN: split screen. Left: "PREFILL". Right: "DECODE".]

**Talk track:**
"**Prefill** is reading your prompt. The model takes *all* your prompt tokens and shoves them through the network **in parallel**, all at once. The chip is screaming, fully busy. This is fast — a few hundred milliseconds even for a big prompt. Prefill is compute-bound: the math is the limit.

**Decode** is writing the answer. And here it can only do **one token at a time.** Predict a token, feed it back in, predict the next, feed it back in. A loop. One forward pass through billions of parameters... for one little token."

[B-ROLL: Animate a conveyor belt. Prefill = a whole pallet loaded at once. Decode = items coming out one... by... one.]

**Talk track:**
"Now here's the insight almost nobody explains, and it's the key to the whole video.

Decode is **not** limited by how fast the chip can do math. It's limited by **memory bandwidth.** For every single token, the GPU has to read *all the model's weights* out of its memory. The math part finishes in microseconds — and then the chip just *sits there waiting* for the next chunk of memory to arrive."

[ON SCREEN: "Decode bottleneck = the memory bus, NOT the math."]

**Talk track:**
"Analogy: imagine a genius chef who can chop anything in a millisecond, but every ingredient is in a warehouse a mile away and he has to drive there and back for each one. He's not slow because he's a bad chef. He's slow because of the *driving.* That's decode. That's the memory wall."

[B-ROLL: Gantt-style timeline — one tiny 'prefill' block at the start, then a long, long string of 'decode' blocks.]

**Talk track:**
"And decode dominates the clock. A 300-token answer? Prefill is maybe 200 milliseconds. Decode is *three to nine seconds.* So decode is ninety-plus percent of your wait — while only using a fraction of the GPU's power.

This is why 'just buy faster chips with more math' doesn't fix it. You don't need a faster chef. You need to drive less."

[ON SCREEN: "Decode ≈ 90% of the time, ≈ 30% of the chip."]

---

## [9:00] THE KV CACHE — THE MODEL'S SCRATCHPAD (9:00–10:15)

**Talk track:**
"So how do they make decode less terrible? First trick: the **KV cache.**

Quick context — the model's superpower is 'attention.' When it writes a token, it looks back at *every* token before it to decide what's relevant. Every previous token offers up two things: a **Key** and a **Value** — basically 'here's what I'm about' and 'here's my content.'"

[ON SCREEN: "K = what I offer · V = my content · cache them so we don't recompute"]

**Talk track:**
"Recomputing those for every single step would be insanely expensive. So we **cache** them. That's the KV cache — the model's scratchpad of every token so far.

The catch: this cache *grows* with every token, forever. And it eats GPU memory fast. At a 128K context, one single user's KV cache can be *forty gigabytes* — as big as the whole model. So a huge amount of engineering goes into shrinking it."

[B-ROLL: A notepad filling up line by line, then running off the bottom of the page.]

**Talk track:**
"That's what tricks like **Grouped-Query Attention** do — store way fewer of those Key/Value vectors per token. It can shrink the cache *eight times* with barely any quality loss. The whole point isn't to save model size — it's to fit *more users and longer chats* on one GPU."

---

## [10:15] PAGEDATTENTION + CONTINUOUS BATCHING (10:15–12:15)

**Talk track:**
"Two more tricks, and these are the load-bearing ones.

First — **PagedAttention.** The naive way to store that KV cache is one big contiguous block per user, sized for the worst case. Problem: real chats vary in length, so you waste *sixty to eighty percent* of that memory just sitting empty."

[B-ROLL: A parking lot where every car gets a whole oversized reserved zone, tons of empty asphalt.]

**Talk track:**
"PagedAttention steals an idea from your operating system — virtual memory paging. Instead of one big block, chop the cache into small fixed-size pages that can live *anywhere* in memory, with a little lookup table tracking them. Now waste drops to under four percent. Same hardware, way more users."

[ON SCREEN: "PagedAttention: KV cache → small pages, allocated on demand. Waste 60–80% → <4%."]

**Talk track:**
"Second — and this is my favorite — **continuous batching.** Here's the thing: because reading the weights from memory is the expensive part, you read them *once* and serve a whole *batch* of users with that one read. Batching isn't optional, it's the only way a GPU is economical.

The naive version, 'static batching,' groups, say, eight users and waits for *all eight* to finish before starting new ones. So if seven are done and one is writing a novel, seven slots sit there idle. Wasteful."

[B-ROLL: Bus that won't leave until every seat's passenger reaches their stop — empty seats riding around.]

**Talk track:**
"**Continuous batching** makes a fresh decision *every single token step.* The instant one user finishes, a new request grabs that empty slot on the very next step. No idle seats. Combine continuous batching with PagedAttention and you get up to **23 times** the throughput of the old way — *and* lower latency."

[ON SCREEN: "Static batching = bus waits for everyone. Continuous = new passenger boards the second a seat opens."]

**Talk track:**
"And here's the truth that surprises people: your 'private' chat is processed in the **same batch** as dozens of strangers' chats. That's not a privacy hole — they're kept separate by the math, by attention masks. It's just the *only* way a GPU becomes affordable. Running your chat alone would be ruinously expensive."

[ON SCREEN: "Your chat rides in a batch with strangers — isolated, but shared. That's why it's cheap."]

---

## [12:15] STREAMING — WHY IT TYPES AT YOU (12:15–13:00)

**Talk track:**
"Now we can finally answer the hook properly. *Why does it type the answer out?*

Because the tokens are *made* one at a time — so the answer is *already* a stream. The server just forwards each token the instant it's born instead of waiting for the whole thing. Streaming isn't a design choice to feel fancy. **It's forced. The tokens don't exist yet.**"

[B-ROLL: Show a `data: {"delta":"Quick"}` frame, then `"sort"`, then `" is"`, then `[DONE]`.]

**Talk track:**
"The tech behind it is **Server-Sent Events** — SSE. It's just a long-lived HTTP response where the server pushes little JSON chunks, each one a piece of text, and a final `[DONE]` to say it's over. One gotcha for you if you ever build this: if *any* proxy or CDN in the middle buffers the response, the live-typing effect dies and it all arrives in one clump. You have to disable buffering end to end."

[ON SCREEN: "SSE: server pushes 'delta' chunks over plain HTTP. Disable buffering everywhere."]

---

## [13:00] MEMORY & WHY IT "FORGETS" (13:00–14:00)

**Talk track:**
"Here's the one that breaks people's brains: **the model has no memory between turns.** Zero. It is completely stateless.

The 'conversation' is an illusion. Every single time you send a message, the orchestrator rebuilds the *entire* relevant history from a database and re-sends the whole thing. The model reads it all fresh, like it's seeing it for the first time, every turn."

[B-ROLL: A character with amnesia re-reading a notebook before every reply.]

**Talk track:**
"So all that history has to fit inside the **context window** — a hard token budget that holds the system prompt, your history, retrieved docs, *and* room reserved for the answer. Think of it as a fixed-width shelf."

[ON SCREEN: stacked bar — "[ system | memory | tools | docs | history | new msg | reserved output ]" under one fixed width.]

**Talk track:**
"As the chat grows, the history shoves against the edge of that shelf. Something falls off. That's *why* it 'forgets' early stuff — and it's not a bug, it's economics. Remember, every retained token gets re-billed *every single turn.* Picture it as a sliding glass tube: old messages fall off the back as new ones push in the front. Forgetting is a design constraint, not a failure."

[ON SCREEN: "It doesn't 'remember' — it re-reads everything every turn. Old tokens fall off the shelf."]

---

## [14:00] WHY IT HALLUCINATES (14:00–15:00)

**Talk track:**
"And the big one everyone actually wonders about: *why does it make stuff up?*

It falls right out of everything we just built. The model is **not looking anything up.** It has no database inside it. At its core it's a function: given everything so far, predict the most *plausible* next token. It was trained to be plausible, not to be *true.*"

[B-ROLL: An autocomplete bar suggesting a confident, totally-made-up citation.]

**Talk track:**
"Most of the time plausible and true line up, because the training data was mostly true. But when it hits a gap — a fact it never saw, a citation that doesn't exist — it doesn't stop and say 'I don't know.' It does the only thing it can: emit the most plausible-sounding next token anyway. A fake-but-perfectly-formatted citation is, statistically, *exactly* what should come after 'According to the paper...' That confident, fluent wrongness *is* the hallucination."

[ON SCREEN: "It predicts plausible tokens, not facts. Confident wrongness is built in."]

**Talk track:**
"And because it's autoregressive, once it commits to a wrong word, it conditions on its own mistake and keeps going, fluently. You can't make this zero by improving the servers. You reduce it three ways — and those three ways are *why the rest of the system exists.*"

---

## [15:00] RAG, TOOLS & SAFETY — THE GUARDRAILS (15:00–16:00)

[DIAGRAM CALLBACK: re-highlight the three side-boxes from the orchestrator — RAG, Tools, Safety.]

**Talk track:**
"Remember those three helpers hanging off the orchestrator? Here's their job.

**RAG** — retrieval-augmented generation — fights hallucination by *injecting real documents into the prompt.* It embeds your question, searches a vector database for the most relevant chunks, and pastes them in. Now the most plausible continuation is grounded in actual retrieved text instead of fuzzy memory.

**Tool calling** — the model doesn't run code, ever. It *emits a structured request* — 'please call this function with these arguments' — your backend runs it, hands the result back, and the model continues. That's how it defers to a calculator or a live search instead of guessing.

**Safety** — a classifier screens your input *before* the model, and screens the output *before* it reaches you. Two gates, one on each side."

[ON SCREEN: "RAG = ground it · Tools = defer it · Safety = filter it"]

---

## [16:00] THE PUNCHLINE: WHAT THIS COSTS (16:00–16:45)

**Talk track:**
"Quick reality check on the money, because it explains the whole business. If you size a fleet for a hundred million weekly users, the master metric is **generated tokens per second** — everything funnels into that, and you size GPUs against it.

Run the numbers and it lands around **one to two dollars per million generated tokens internally** — roughly eleven cents per user per month for text. Meanwhile the public API price for top models is ten to fifteen dollars per million. That ~10x gap is margin, research, safety, and the free tier. Which is exactly why a twenty-dollar subscription works."

[ON SCREEN: "~$1–2 / million tokens internal · ~11¢ per user/month · that's why $20/mo works"]

---

## [16:45] RECAP (16:45–17:20)

[B-ROLL: Quick rebuild of the architecture diagram, fast, all boxes lighting up in sequence.]

**Talk track:**
"Okay — lock it in. Three things to remember.

**One:** it's two fleets. A cheap, infinite web tier in front of a scarce, expensive GPU tier. All the tension lives there.

**Two:** the model makes **one token at a time**, and each token means reading billions of parameters out of memory. That single fact explains the streaming, the slowness, and the memory wall. Continuous batching, PagedAttention, the KV cache — every trick exists to hide that one inefficiency.

**Three:** the model has no memory and doesn't *know* facts — it rebuilds your history every turn and predicts plausible tokens. That's why it forgets, and why it hallucinates, and why RAG and tools exist.

Every weird thing about these assistants comes back to one line: *one token at a time.*"

[ON SCREEN: "One token at a time. That's the whole story."]

---

## [17:20] CTA (17:20–17:50)

**Talk track:**
"If this finally made the GPU side click for you, do me a favor and subscribe — I break down system design like this every week, no fluff, no hand-waving.

The **full architecture diagram, the capacity math, and all my notes** are in the GitHub repo — link's in the description. Grab it before your next system-design interview.

And drop a comment: which box do you want me to go *deeper* on next — the inference queue, speculative decoding, or the rate limiter? Tell me and I'll make it.

Thanks for watching. See you in the next one."

[ON SCREEN: "Subscribe · GitHub repo in description · Comment your pick: queue / speculative decoding / rate limiter"]

---

## Production notes

**Screen recordings to capture**
- The hero shot: typing "Explain quicksort", hitting Enter, the slow token-by-token reveal (for the hook). Capture clean, you'll reuse it.
- A real SSE stream in browser dev tools (Network tab) showing `data:` frames arriving — great B-roll for the streaming section.
- Optional: a terminal showing `429 Too Many Requests` for the rate-limiter beat.

**Diagrams to build (the spine of this video)**
- The **progressive architecture diagram** is the centerpiece. Build it in one file with 9 reveal states (User → Edge → Gateway → Auth → Rate limiter → Router → Orchestrator+helpers → LB/Queue/GPU → token stream back). Animate one box appearing per cue. Reuse the article's Mermaid graph as the source of truth.
- **Prefill vs Decode** split-screen panel.
- **Decode timeline / Gantt**: one tiny prefill block + a long row of decode blocks (sell "90% of the time").
- **KV cache** notepad-filling animation.
- **PagedAttention**: parking-lot-with-wasted-space → small pages.
- **Continuous vs static batching**: the bus analogy (waiting bus vs. seat-refills-instantly).
- **Context window** stacked bar under a fixed width + sliding-glass-tube visual.

**B-roll / analogy visuals**
- Restaurant: front-of-house (waiters, easy to add) vs kitchen (one chef, one dish at a time).
- Chef driving to a warehouse for each ingredient (memory wall).
- Amnesia character re-reading a notebook each turn (statelessness).
- Autocomplete confidently suggesting a fake citation (hallucination).

**Lower-thirds / on-screen text:** all `[ON SCREEN: ...]` callouts above — keep them short, one line, high contrast.

**Pre-film checklist**
- Confirm the GitHub repo link and pin it in the description + a pinned comment.
- Decide the comment-prompt poll wording (queue / speculative decoding / rate limiter) and add it as an end-screen card.
- Keep the demo/hook recording uncut — no jump cuts during the typing reveal, it's the proof.

**Numbers to keep honest (don't round away on screen):** token ≈ ¾ word; decode ≈ 90% of latency; KV cache up to ~40 GB at 128K context; GQA ~8× cache reduction; PagedAttention waste 60–80% → <4%; continuous batching + PagedAttention up to 23×; internal cost ~$1–2 / M tokens, ~11¢/user/month, list price ~$10–15 / M. These are from the source article — present as "roughly" / "illustrative," not vendor-exact.

**Estimated read time:** ~2,650 words of spoken track ÷ 150 ≈ **17.5 minutes** of talk. With diagram-reveal pauses and B-roll beats, lands comfortably in the **17–19 minute** target.
