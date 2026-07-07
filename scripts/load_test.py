import asyncio, time, httpx

URL = "http://localhost:8000/chat"
CONCURRENCY = 5
TOTAL_REQUESTS = 20

async def one_request(client):
    start = time.perf_counter()
    r = await client.post(URL, json={"text": "how to make a coffee?"})
    print("Reply",r.content)
    return time.perf_counter() - start, r.status_code

async def main():
    async with httpx.AsyncClient(timeout=60) as client:
        sem = asyncio.Semaphore(CONCURRENCY)
        async def bound():
            async with sem:
                return await one_request(client)
        results = await asyncio.gather(*[bound() for _ in range(TOTAL_REQUESTS)])

    times = sorted(t for t, _ in results)
    errors = sum(1 for _, c in results if c != 200)
    pct = lambda p: times[max(int(len(times) * p) - 1, 0)]
    print(f"requests={len(times)} errors={errors}")
    print(f"min={times[0]:.2f}s p50={pct(0.5):.2f}s p95={pct(0.95):.2f}s max={times[-1]:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())