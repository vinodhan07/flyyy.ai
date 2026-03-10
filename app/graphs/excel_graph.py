import os
import time
import ssl
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.boq_schema import BOQList, BOQItem

# Fix SSL issues on corporate/school networks
os.environ["REQUESTS_CA_BUNDLE"] = ""
os.environ["CURL_CA_BUNDLE"] = ""
ssl._create_default_https_context = ssl._create_unverified_context


def extract_with_ai(raw_text: str, industry: str = "construction"):
    print(f"🚀 Starting Extraction for {industry}...")
    print(f"📄 Total text length: {len(raw_text)} chars")

    my_key = os.getenv("GOOGLE_API_KEY")
    if not my_key:
        print("❌ GOOGLE_API_KEY not set in .env file!")
        return {"items": []}

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        api_key=my_key,
        temperature=0,
    )
    smart_ai = llm.with_structured_output(BOQList)

    all_extracted_items = []
    chunk_size = 8000
    overlap = 500
    total_chunks = (len(raw_text) // (chunk_size - overlap)) + 1
    consecutive_failures = 0

    for chunk_num, i in enumerate(range(0, len(raw_text), chunk_size - overlap), 1):
        current_chunk = raw_text[i : i + chunk_size]

        prompt = f"""
You are a BOQ (Bill of Quantities) data extraction expert for the {industry} industry.

Extract EVERY line item from the text below.

RULES:
- Extract EVERY row that describes a material, equipment, or work item.
- Use 0 for unknown quantity, '-' for unknown unit, 'Generic' for unknown brand.
- DO NOT merge or summarize items. Extract each one separately.
- Skip section headings, serial numbers, and Total/Subtotal rows.

TEXT:
{current_chunk}
"""

        try:
            result = smart_ai.invoke(prompt)
            if result and result.items:
                all_extracted_items.extend(result.items)
                print(f"✅ Chunk {chunk_num}/{total_chunks}: found {len(result.items)} items")
                consecutive_failures = 0
            else:
                print(f"📭 Chunk {chunk_num}/{total_chunks}: no items found")

        except Exception as e:
            error_msg = str(e)
            consecutive_failures += 1

            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                print(f"⛔ Chunk {chunk_num}: API quota exhausted!")
                if consecutive_failures >= 2:
                    print("🔄 Quota fully exhausted — stopping AI, will use heuristic fallback.")
                    break  # Stop immediately, let the route fallback handle it
                # First failure: wait briefly and try one more time
                time.sleep(5)
            else:
                print(f"⚠️ Chunk {chunk_num} error: {error_msg[:100]}")
                if consecutive_failures >= 3:
                    print("🔄 Too many errors — stopping AI, will use heuristic fallback.")
                    break

        # Small delay between chunks to stay under rate limits
        time.sleep(1)

    # Deduplicate
    seen = set()
    unique_items = []
    for item in all_extracted_items:
        key = item.description.strip().lower()
        if key not in seen:
            seen.add(key)
            unique_items.append(item)

    print(f"🎯 DONE! Total unique items: {len(unique_items)} (from {len(all_extracted_items)} raw)")
    return {"items": [item.dict() for item in unique_items]}
