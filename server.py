from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.post("/webhook")
async def webhook(info):
    try:
        print("info: ", info)
        return {"info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))