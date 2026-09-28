import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = "auditmind"

client.create_bank(
    bank_id=bank_id,
    name="AuditMind"
)

print("Memory bank created!")

client.retain(
    bank_id=bank_id,
    content="Audit 001 found an access control issue. The company had 5 inactive employee accounts that were not disabled. The remediation was to review and disable inactive accounts."
)

print("Audit memory stored!")

result = client.recall(
    bank_id=bank_id,
    query="access control inactive employee accounts"
)

print("\nRecalled memory:")

for memory in result.results:
    print("-", memory.text)

client.close()