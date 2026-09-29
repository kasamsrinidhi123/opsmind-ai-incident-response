import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = "opsmind"

try:
    client.create_bank(
        bank_id=BANK_ID,
        name="OpsMind Incident Memory"
    )
    print("Memory bank created!")
except Exception as e:
    print("Bank may already exist. Continuing...")

client.retain(
    bank_id=BANK_ID,
    content="""
    Production Incident:
    PostgreSQL connection timeout occurred.

    Root Cause:
    The database connection pool was exhausted.

    Resolution:
    The team increased the connection pool size and
    restarted the affected service.

    Result:
    The application recovered successfully.
    """,
    context="Production incident"
)

print("Incident stored in Hindsight!")

result = client.recall(
    bank_id=BANK_ID,
    query="Have we seen a PostgreSQL connection failure before? What was the root cause and solution?"
)

print("\n===== HINDSIGHT MEMORY =====")

for memory in result.results:
    print("-", memory.text)

client.close()