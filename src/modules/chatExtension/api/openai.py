import aiohttp

def _openai_response(url: str):
    async def openai_response(json: dict, api_key: str = "", timeout: float = 300) -> str:
        async with aiohttp.ClientSession() as session:
            headers = {}
            if api_key == "":
                headers={"content_type": "application/json"}
            else:
                headers={"content_type": "application/json", "Authorization": f"Bearer {api_key}"}

            async with session.post(
                url,
                json=json,
                headers=headers,
                timeout=timeout,
            ) as r:
                return await r.json()
            
    return openai_response

completion = _openai_response(url="https://api.openai.com/v1/completions")
chat_completion = _openai_response(url="https://api.openai.com/v1/chat/completions")