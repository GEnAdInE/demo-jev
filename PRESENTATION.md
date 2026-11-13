# Jev vs a traditional LLM

Talk track for the demo. Each section maps to a tab of the app. No benchmark numbers here: run the demo and read the timings it displays.

---

## 1. The problem

Software needs **decisions**, not prose.

> "Should a human look at this claim?"  ->  `if needs_review: route_to_adjuster()`

A traditional LLM answers with generated text. To branch on it you must prompt for JSON, parse it, handle malformed output, and guess how sure the model was.

---

## 2. What Jev is

A **decision model** (TypeSafe AI). You send:

1. a **state**: text, JSON or an image
2. **typed questions**: yes/no, choice, score, box...

It returns **typed answers with probabilities**, not generated text.

```
State (text / JSON / image) -> Typed questions -> Typed answers + probabilities
```

---

## 3. Side by side

| | Traditional LLM | Jev |
|---|---|---|
| Output | Free text (JSON if you ask nicely) | Typed answers: yes/no, one-of-N, score, box |
| Uncertainty | Verbalised ("I think...") or logprobs you must interpret | A probability on every answer |
| Parsing | Regex / JSON repair / retries | None: the schema is the contract |
| Invalid output | Possible: wrong key, extra prose, off-list label | Not possible for a choice: answers come from your options |
| Branching in code | Compare strings | Compare a number or an enum |
| Same input twice | Can differ: wording, label, format | Same question types, comparable probabilities (see Consistency tab) |
| Images | Describe, then parse the description | Ask typed questions directly on the photo |
| Fit | Writing, chat, summarising, open-ended reasoning | Triage, routing, classification, moderation, scoring |

Jev is **not** a chatbot replacement: it does not write the claim letter. It decides what to do with the claim.

---

## 4. The demo, tab by tab

| Tab | Route | What to show |
|---|---|---|
| Primitives | `/api/primitive/{kind}` | One question type at a time: yes/no as a probability of yes, choice with a probability per option |
| Hotline | `/api/hotline` | One call, several questions on a claim. "Split" runs one call per question to compare |
| Tsunami | `/api/tsunami` | 300 claims, parallel, each with category, severity, fraud probability, "needs a human" |
| Consistency | `/api/consistency` | The same claim asked N times: how stable are the answers |
| Sushi | `/api/sushi/{i}` | Typed questions on a photo (food probabilities, apparent health score) |

Every result has a **raw HTTP** panel: the exact request and response, so nothing is hidden.

---

## 5. The pitch in three lines

- **Typed in, typed out**: no prompt-and-parse layer to maintain.
- **Probabilities, not vibes**: set thresholds ("auto-approve above 0.9, else human").
- **Built for volume**: independent small calls, easy to parallelise (Tsunami tab).

---

## 6. Honest limits

- Jev answers the questions you define; it does not do open-ended generation.
- Images must be 280-1568 px per side (the demo resizes them) and need an explicit images header.
- A probability is only as useful as your threshold: calibrate on your own data before automating.
- This is a demo with fake claims, not an insurance product.

---

## 7. Try it

See the [README](README.md) for setup. You need your own `TYPESAFE_API_KEY`.
