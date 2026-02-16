from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from core.supabase_client import get_supabase
from routes.activity_log import insert_activity_log
from datetime import datetime
import uuid

router = APIRouter()


# Request model for campaign creation
class CampaignCreate(BaseModel):
    name: str
    campaign_type: str
    industry: str
    area: str
    city: str
    state: str
    country: str
    job_titles: List[str]
    requested_leads: int
    status: str


@router.post("/campaigns/{user_id}")
def create_campaign(user_id: str, payload: CampaignCreate):
    try:
        supabase = get_supabase()

        # 1️⃣ Generate campaign ID
        campaign_id = str(uuid.uuid4())

        # 2️⃣ Prepare campaign data from user
        campaign_data = payload.dict()
        campaign_data["id"] = campaign_id
        campaign_data["user_id"] = user_id
        campaign_data["created_at"] = datetime.utcnow().isoformat()

        # 3️⃣ Insert campaign into table
        result = (
            supabase
            .schema("public")  # change schema if needed
            .table("campaigns")
            .insert(campaign_data)
            .execute()
        )

        inserted_campaign = result.data[0]

        # 4️⃣ Safety check
        if inserted_campaign["user_id"] != user_id:
            raise HTTPException(status_code=400, detail="User ID mismatch")

        # 5️⃣ Insert activity log (reusable function)
        activity_log = insert_activity_log(
            user_id=user_id,
            campaign_id=campaign_id,
            action="Started lead scraping",
            metadata=campaign_data
        )

        # 6️⃣ Return response
        return {
            "user_id": activity_log["user_id"],
            "campaign_id": activity_log["campaign_id"],
            "action": activity_log["action"],
            "created_at": activity_log["created_at"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
