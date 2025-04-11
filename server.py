from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request, validationToken: str | None = None):
    """
    Handle POST requests for validation and notifications.
    """
    try:
        if validationToken:
            logger.info(f"Validation token (query): {validationToken}")
            return PlainTextResponse(content=validationToken, status_code=200)

        body = await request.json()
        logger.info(f"Received: {body}")

        if "validationToken" in body:
            token = body["validationToken"]
            logger.info(f"Validation token (JSON): {token}")
            return PlainTextResponse(content=token, status_code=200)

        for event in body.get("value", []):
            logger.info(f"Event: {event}")

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"status": "accepted"}, 202


@app.get("/webhook")
async def verify_subscription(validationToken):
    try:
        print("validationToken: ", validationToken)
        return PlainTextResponse(content=validationToken, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


