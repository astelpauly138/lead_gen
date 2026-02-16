from fastapi import APIRouter, HTTPException
from core.supabase_client import get_supabase

router = APIRouter()


@router.get("/lead-analytics/{user_id}")
def get_lead_list(user_id: str):
    try:
        supabase = get_supabase()

        result = (
            supabase.schema("analytics")
            .table("lead_analytics")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return {
            "lead_list": result.data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
