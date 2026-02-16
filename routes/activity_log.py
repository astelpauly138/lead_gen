from core.supabase_client import get_supabase
from datetime import datetime
import uuid


def insert_activity_log(user_id: str, campaign_id: str, action: str, metadata: dict):
    supabase = get_supabase()

    activity_id = str(uuid.uuid4())

    activity_data = {
        "id": activity_id,
        "campaign_id": campaign_id,
        "user_id": user_id,
        "action": action,
        "metadata": metadata,
        "created_at": datetime.utcnow().isoformat()
    }

    supabase.schema("public") \
        .table("activity_logs") \
        .insert(activity_data) \
        .execute()

    result = (
        supabase.schema("analytics")
        .table("activity_logs_view")
        .select("*")
        .eq("id", activity_id)
        .single()
        .execute()
    )

    return result.data
