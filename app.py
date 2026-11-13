import asyncio
import io
import json
import time
from typing import Literal
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response, StreamingResponse
from PIL import Image as PILImage
from PIL import ImageOps
from pydantic import BaseModel
from typesafe_sdk import AsyncTypeSafeClient, Image, TypeSafeAPIError

import claims

ROOT = Path(__file__).parent
Lang = Literal["en", "fr"]
load_dotenv(ROOT / ".env")

client: AsyncTypeSafeClient


@asynccontextmanager
async def lifespan(_: FastAPI):
    global client
    async with AsyncTypeSafeClient() as client:
        yield


app = FastAPI(lifespan=lifespan)


def dump(response) -> dict:
    return {name: answer.model_dump() for name, answer in response.answers.items()}


def raw(response) -> dict:
    """The actual HTTP exchange with Jev, as sent and received by the SDK."""
    http = response.raw_http_response
    body = http.request.content
    out = {"endpoint": f"{http.request.method} {http.request.url}"}
    if http.request.headers["content-type"].startswith("multipart"):
        # Image requests are multipart: a JSON part named "request", then the JPEG bytes.
        head, _, rest = body.partition(b"\r\n\r\n")
        json_part, _, image_part = rest.partition(b"\r\n--")
        body = json_part
        out["note"] = f"multipart/form-data: this JSON part, plus the JPEG as part asset-0 ({len(image_part) // 1024} KB)"
    return out | {"request": json.loads(body), "response": http.json()}


def ms_since(start: float) -> int:
    return round((time.perf_counter() - start) * 1000)


def sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


async def stream_jobs(jobs, extra: dict | None = None):
    start = time.perf_counter()
    if extra:
        yield sse(extra)
    for finished in asyncio.as_completed([asyncio.create_task(job) for job in jobs]):
        yield sse(await finished)
    yield sse({"done": True, "seconds": round(time.perf_counter() - start, 2)})


async def judge(sem: asyncio.Semaphore, state: dict, questions: dict, tag: dict) -> dict:
    async with sem:
        start = time.perf_counter()
        try:
            r = await client.system_one(state=state, questions=questions)
        except TypeSafeAPIError as e:
            return tag | {"error": str(e)}
        return tag | {"answers": dump(r), "ms": ms_since(start), "tokens": r.usage.input_tokens, "raw": raw(r)}


@app.get("/")
async def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/tsunami")
async def tsunami(n: int = 300, concurrency: int = 20, lang: Lang = "en"):
    sem = asyncio.Semaphore(concurrency)
    jobs = [
        judge(sem, {"claim": text}, claims.TRIAGE[lang], {"i": i, "claim": text})
        for i, text in enumerate(claims.make_claims(n, lang))
    ]
    return StreamingResponse(stream_jobs(jobs), media_type="text/event-stream")


class HotlineIn(BaseModel):
    text: str
    split: bool = False
    lang: Lang = "en"


@app.post("/api/hotline")
async def hotline(body: HotlineIn):
    state = {"claim": body.text}
    questions = claims.HOTLINE[body.lang]
    batches = [{k: q} for k, q in questions.items()] if body.split else [questions]
    start = time.perf_counter()
    responses = [await client.system_one(state=state, questions=batch) for batch in batches]
    elapsed = ms_since(start)
    answers = {}
    for r in responses:
        answers |= dump(r)
    return {
        "answers": answers,
        "ms": elapsed,
        "tokens": sum(r.usage.input_tokens for r in responses),
        "calls": len(responses),
        "raw": raw(responses[0]),
    }


@app.get("/api/consistency")
async def consistency(n: int = 50, concurrency: int = 20, lang: Lang = "en"):
    sem = asyncio.Semaphore(concurrency)
    jobs = [
        judge(sem, {"claim": text}, claims.VERDICT[lang], {"case": case})
        for case, text in claims.CONSISTENCY_CASES[lang].items()
        for _ in range(n)
    ]
    return StreamingResponse(
        stream_jobs(jobs, {"cases": claims.CONSISTENCY_CASES[lang]}), media_type="text/event-stream"
    )


def photos() -> list[Path]:
    return [p for p in sorted(ROOT.iterdir()) if p.suffix.lower() in (".jpg", ".jpeg", ".png")]


def photo_bytes(i: int) -> bytes:
    paths = photos()
    if not 0 <= i < len(paths):
        raise HTTPException(404, "No such photo in the project folder.")
    # Jev rejects images outside 280-1568 px per side instead of resizing them.
    img = ImageOps.exif_transpose(PILImage.open(paths[i])).convert("RGB")
    img.thumbnail((1568, 1568))
    if min(img.size) < 280:
        img = ImageOps.scale(img, 280 / min(img.size))
    out = io.BytesIO()
    img.save(out, "JPEG", quality=90)
    return out.getvalue()


@app.get("/api/primitives")
async def primitives(lang: Lang = "en"):
    return [
        {"kind": kind, "claim": p.get("claim"), "photo": p.get("photo"), "question": p["question"].model_dump(exclude_none=True)}
        for kind, p in claims.PRIMITIVES[lang].items()
    ]


@app.get("/api/primitive/{kind}")
async def primitive(kind: str, lang: Lang = "en"):
    p = claims.PRIMITIVES[lang].get(kind)
    if p is None:
        raise HTTPException(404, "Unknown question type.")
    is_image = "photo" in p
    state = {"photo": Image(photo_bytes(p["photo"]))} if is_image else {"claim": p["claim"]}
    start = time.perf_counter()
    r = await client.system_one(
        state=state,
        questions={"answer": p["question"]},
        extra_headers={"TypeSafe-Danger-Zone-Images": "true"} if is_image else None,
    )
    return {"answer": dump(r)["answer"], "ms": ms_since(start), "tokens": r.usage.input_tokens, "raw": raw(r)}


@app.get("/api/sushi/photos")
async def sushi_photos():
    return {"count": len(photos())}


@app.get("/api/sushi/photo/{i}")
async def sushi_photo(i: int):
    return Response(photo_bytes(i), media_type="image/jpeg")


@app.get("/api/sushi/{i}")
async def sushi(i: int, lang: Lang = "en"):
    image = Image(photo_bytes(i))
    start = time.perf_counter()
    r = await client.system_one(
        state={"photo": image},
        questions=claims.SUSHI[lang],
        extra_headers={"TypeSafe-Danger-Zone-Images": "true"},
    )
    return {"answers": dump(r), "ms": ms_since(start), "tokens": r.usage.input_tokens, "raw": raw(r)}
