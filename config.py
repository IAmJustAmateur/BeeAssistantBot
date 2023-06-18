from dotenv import load_dotenv
import os

load_dotenv()

admin_id = os.environ["admin_id"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_TABLE = os.environ.get("SUPABASE_TABLE")
