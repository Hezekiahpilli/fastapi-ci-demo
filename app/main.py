"""FastAPI application configured to run on AWS Lambda."""

from datetime import datetime, timezone

from fastapi import FastAPI
from mangum import Mangum


app = FastAPI()


@app.on_event("startup")
async def record_start_time() -> None:
    """Record when the application started so uptime can be reported."""

    app.state.start_time = datetime.now(timezone.utc)


@app.get("/")
def root() -> dict[str, str]:
    """Return a simple welcome message for the root endpoint."""

    return {"message": "FastAPI running on Lambda!"}


@app.get("/status")
def status() -> dict[str, object]:
    """Report simple health information about the service."""

    start_time: datetime | None = getattr(app.state, "start_time", None)
    current_time = datetime.now(timezone.utc)

    if start_time is None:
        # The startup event may not have fired yet (e.g., in certain tests).
        start_time = current_time

    uptime = (current_time - start_time).total_seconds()

    return {
        "status": "ok",
        "current_time": current_time.isoformat(),
        "started": start_time.isoformat(),
        "uptime_seconds": uptime,
    }


# 👇 Add this at the end
handler = Mangum(app)
