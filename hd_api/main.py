"""Entry point for the Human Design API server."""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 18090))
    uvicorn.run("hd_api.app:app", host="0.0.0.0", port=port, reload=False)
