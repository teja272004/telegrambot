import aiohttp

async def perform_web_search(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.duckduckgo.com/?q={query}&format=json") as response:
            data = await response.json()
            results = data.get("RelatedTopics", [])
            if results:
                return "\n".join([r["Text"] + ": " + r["FirstURL"] for r in results[:5]])
            return "No results found."
