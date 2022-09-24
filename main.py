import os

import uvicorn

PORT = int(os.environ.get("PORT", 8000))
uvicorn.run(
    "srandom.asgi:application",
    host="0.0.0.0",
    port=PORT,
    log_level="info",
    proxy_headers=True,
)
