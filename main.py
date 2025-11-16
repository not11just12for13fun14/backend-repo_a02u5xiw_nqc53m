import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Booking, TrophyOrder

app = FastAPI(title="QED Express – WeWork Trivia Night API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "QED Express API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or "unknown"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# --- Booking Endpoints ---

@app.post("/api/bookings", response_model=dict)
def create_booking(payload: Booking):
    try:
        booking_id = create_document("booking", payload)
        # Simulate auto-response email payload (would be sent by a worker in production)
        auto_email = {
            "subject": "QED Express – Your Trivia Event is Confirmed",
            "host_panel_link": "https://qed.example.com/host-panel",
            "quiz_edition": "Auto-generated for your date",
            "printable_poster_url": "https://qed.example.com/poster.pdf",
            "wework_app_text": "Join us for QED Express Trivia!"
        }
        return {"ok": True, "id": booking_id, "auto_email": auto_email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bookings", response_model=List[dict])
def list_bookings(limit: Optional[int] = 50):
    try:
        docs = get_documents("booking", {}, limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Trophy Orders ---

@app.post("/api/trophy-orders", response_model=dict)
def create_trophy_order(payload: TrophyOrder):
    try:
        order_id = create_document("trophyorder", payload)
        # Basic total calculation — example unit price
        UNIT_PRICE = 9.0
        total = round(UNIT_PRICE * payload.quantity, 2)
        return {"ok": True, "id": order_id, "unit_price": UNIT_PRICE, "total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trophy-orders", response_model=List[dict])
def list_trophy_orders(limit: Optional[int] = 50):
    try:
        docs = get_documents("trophyorder", {}, limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
