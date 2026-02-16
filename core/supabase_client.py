from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError("Supabase environment variables not set")

_supabase: Client | None = None


def get_supabase() -> Client:
    """
    Singleton Supabase client.
    """
    global _supabase

    if _supabase is None:
        _supabase = create_client(
            SUPABASE_URL,
            SUPABASE_SERVICE_KEY
        )

    return _supabase
