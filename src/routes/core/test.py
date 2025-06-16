from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/webhook/test")
async def webhook_test_listener(request: Request):
    body = await request.body()
    print("[WEBHOOK TEST] Raw Body:", body)

    try:
        payload = await request.json()
        print("[WEBHOOK TEST] Parsed JSON:", payload)
        return {"status": "received", "payload": payload}
    except Exception as e:
        print("[WEBHOOK TEST] JSON parse error:", str(e))
        return JSONResponse(content={"error": "Invalid JSON", "detail": str(e)}, status_code=400)
