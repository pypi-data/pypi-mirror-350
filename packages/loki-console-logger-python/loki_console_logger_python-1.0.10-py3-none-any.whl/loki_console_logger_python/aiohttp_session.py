import aiohttp

from .utils import get_labels


async def post_to_loki(log_buffer, options):
    payload = {
        "streams": [
            {
                "stream": get_labels(options),
                "values": log_buffer,
            }
        ]
    }
    headers = {
        "X-Scope-OrgID": options.tenant_id,
    }
    if options.auth_token:
        headers["Authorization"] = f"Bearer {options.auth_token}"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3)) as session:
            async with session.post(options.url, json=payload, headers=headers) as response:
                if response.status != 204:
                    body = await response.text()
                    print(f"[LokiLogger] Failed to push logs: {response.status} {body}")
    except Exception:
        pass
