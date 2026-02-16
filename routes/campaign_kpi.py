from fastapi import APIRouter, HTTPException
from core.supabase_client import get_supabase

router = APIRouter()


@router.get("/campaign-kpis/{user_id}")
def get_campaign_kpis(user_id: str):
    try:
        supabase = get_supabase()

        result = supabase.schema("analytics") \
            .table("campaign_cards") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        return {
            "campaign_kpis": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
