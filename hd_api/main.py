"""Entry point for the Human Design API server."""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("hd_api.app:app", host="0.0.0.0", port=18090, reload=False)
