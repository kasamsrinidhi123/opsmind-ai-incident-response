import os
import asyncio

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "opsmind"


# ============================================================
# VALIDATE ENVIRONMENT
# ============================================================

if not HINDSIGHT_BASE_URL:
    raise ValueError("HINDSIGHT_BASE_URL is missing from .env")

if not HINDSIGHT_API_KEY:
    raise ValueError("HINDSIGHT_API_KEY is missing from .env")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")


# ============================================================
# GROQ CLIENT
# ============================================================

groq = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# HINDSIGHT RECALL
# ============================================================

async def _recall_memories(incident):
    """
    Retrieve previous incident memories from Hindsight.

    A new Hindsight client is created inside the async function
    so that its HTTP session belongs to the correct event loop.
    """

    client = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )

    try:

        result = await client.arecall(
            bank_id=BANK_ID,
            query=f"""
Find previous production incidents that are similar
to the following incident.

CURRENT INCIDENT:
{incident}

Return relevant information including:

- Previous incident descriptions
- Root causes
- Previous solutions
- Successful fixes
- Failed fixes
- Lessons learned
- Relevant operational patterns

Only return memories that are relevant to the current incident.
"""
        )

        return result

    finally:

        await client.aclose()


# ============================================================
# HINDSIGHT RETAIN
# ============================================================

async def _retain_memory(memory):
    """
    Save a resolved incident and its outcome into Hindsight.
    """

    client = Hindsight(
        base_url=HINDSIGHT_BASE_URL,
        api_key=HINDSIGHT_API_KEY
    )

    try:

        await client.aretain(
            bank_id=BANK_ID,
            content=memory,
            context="OpsMind production incident learning"
        )

    finally:

        await client.aclose()


# ============================================================
# ANALYZE INCIDENT
# ============================================================

def analyze_incident(incident):
    """
    Analyze a production incident using:

    1. Hindsight memory
    2. Groq LLM
    """

    # --------------------------------------------------------
    # STEP 1: Retrieve previous incidents from Hindsight
    # --------------------------------------------------------

    memory_result = asyncio.run(
        _recall_memories(incident)
    )

    memories = []

    if memory_result and memory_result.results:

        for memory in memory_result.results:

            if hasattr(memory, "text") and memory.text:
                memories.append(memory.text)

    # --------------------------------------------------------
    # Prepare previous memory
    # --------------------------------------------------------

    if memories:

        previous_memory = "\n\n".join(memories)

    else:

        previous_memory = (
            "No previous similar incidents were found "
            "in Hindsight memory."
        )


    # --------------------------------------------------------
    # STEP 2: Build Groq prompt
    # --------------------------------------------------------

    prompt = f"""
You are OpsMind, an AI Incident Response Agent.

Your job is to help software engineering teams investigate
and resolve production incidents using previous incident
knowledge stored in Hindsight.

==================================================
CURRENT INCIDENT
==================================================

{incident}


==================================================
PREVIOUS INCIDENT MEMORY
==================================================

{previous_memory}


==================================================
ANALYSIS REQUIREMENTS
==================================================

Analyze the current production incident.

Provide the response using the following sections:

1. Incident Summary

2. Possible Root Cause

3. Similar Previous Incidents

4. Recommended Action

5. Risk Level

6. Why This Recommendation Makes Sense

7. What Information Is Missing


==================================================
IMPORTANT RULES
==================================================

- Do not pretend that a root cause is certain.
- Clearly separate evidence from assumptions.
- Use previous incidents when they are genuinely relevant.
- Mention when Hindsight memory supports a recommendation.
- Do not invent previous incidents.
- If there is not enough information, say what is missing.
- Give practical production troubleshooting steps.
- Prioritize safe actions before destructive actions.
- If rollback is recommended, explain why.
- Keep the response clear and useful for an SRE/DevOps engineer.
"""


    # --------------------------------------------------------
    # STEP 3: Ask Groq
    # --------------------------------------------------------

    response = groq.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful production incident "
                    "response assistant. "
                    "You provide evidence-based troubleshooting "
                    "recommendations and clearly communicate uncertainty."
                )
            },

            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )


    # --------------------------------------------------------
    # STEP 4: Extract response
    # --------------------------------------------------------

    analysis = response.choices[0].message.content


    # --------------------------------------------------------
    # STEP 5: Return result to Streamlit
    # --------------------------------------------------------

    return {
        "analysis": analysis,
        "memories": memories
    }


# ============================================================
# LEARN FROM INCIDENT
# ============================================================

def learn_from_incident(
    incident,
    resolution,
    outcome
):
    """
    Store the incident, resolution and outcome
    in Hindsight so future incidents can benefit
    from the experience.
    """

    memory = f"""
Production Incident Learning

==================================================
INCIDENT
==================================================

{incident}


==================================================
RESOLUTION
==================================================

{resolution}


==================================================
OUTCOME
==================================================

{outcome}


==================================================
LESSON LEARNED
==================================================

This incident, its resolution, and its outcome should
be considered when analyzing similar production incidents
in the future.

OpsMind should use this experience to improve future
incident investigation and recommendations.
"""


    # --------------------------------------------------------
    # Save memory to Hindsight
    # --------------------------------------------------------

    asyncio.run(
        _retain_memory(memory)
    )

    return True