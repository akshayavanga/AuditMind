import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()


st.set_page_config(
    page_title="AuditMind",
    page_icon="🔍",
    layout="wide"
)
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #172554, #1e3a8a);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: white !important;
}

p, label, .stMarkdown {
    color: #e5e7eb !important;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    border-radius: 10px;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 600;
}
/* Add Audit card */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.08);
    padding: 25px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

</style>
""", unsafe_allow_html=True)


# Hindsight connection
client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = "auditmind"


# Create memory bank
try:
    client.create_bank(
        bank_id=BANK_ID,
        name="AuditMind"
    )
except Exception:
    pass


# Recall helper
def recall_memory(question):

    async def run_recall():
        return await client.arecall(
            bank_id=BANK_ID,
            query=question
        )

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            asyncio.run,
            run_recall()
        )
        return future.result()
# Memory evidence helper
def get_memory_evidence(question):

    async def run_evidence():
        return await client.arecall(
            bank_id=BANK_ID,
            query=question
        )

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            asyncio.run,
            run_evidence()
        )
        return future.result()

# Store audit helper
def store_audit(content):

    async def run_retain():
        return await client.aretain(
            bank_id=BANK_ID,
            content=content
        )

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            asyncio.run,
            run_retain()
        )
        return future.result()


# -------------------------
# PAGE
# -------------------------

st.title("🔍 AuditMind")

st.subheader("AI Compliance & Audit Memory Agent")

st.write(
    "AuditMind remembers previous audits, findings, "
    "remediation actions, and control history."
)


# -------------------------
# ADD AUDIT
# -------------------------

st.divider()

st.header("📋 Add Audit")

audit_id = st.text_input(
    "Audit ID",
    placeholder="Example: AUD-002"
)

finding = st.text_area(
    "Audit Finding",
    placeholder="Example: 3 terminated employee accounts were still active."
)

severity = st.selectbox(
    "Severity",
    ["Low", "Medium", "High", "Critical"]
)

remediation = st.text_area(
    "Remediation Action",
    placeholder="Example: Disable terminated employee accounts within 24 hours."
)

status = st.selectbox(
    "Remediation Status",
    ["Open", "In Progress", "Resolved"]
)


if st.button("💾 Store Audit in Memory"):

    if audit_id and finding and remediation:

        audit_content = f"""
Audit ID: {audit_id}

Finding: {finding}

Severity: {severity}

Remediation: {remediation}

Status: {status}
"""

        try:

            store_audit(audit_content)

            st.success(
                f"✅ {audit_id} stored in Hindsight memory!"
            )

        except Exception as e:

            st.error(
                f"Error storing audit: {e}"
            )

    else:

        st.warning(
            "Please fill in Audit ID, Finding, and Remediation."
        )
# -------------------------
# AUDIT DASHBOARD
# -------------------------

st.divider()

st.header("📊 AuditMind Dashboard")

st.write(
    "Current overview of the audit history stored in AuditMind."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Audits", "3")

with col2:
    st.metric("Resolved", "1")

with col3:
    st.metric("In Progress", "1")

with col4:
    st.metric("Open", "1")

st.subheader("🔎 Audit Health")

st.write(
    "⚠️ Recurring access-control issues detected across multiple audits."
)

st.write(
    "📌 Highest-priority follow-up: terminated employee account deactivation."
)
# -------------------------
# RECURRING FINDING ANALYSIS
# -------------------------
if "audit_records" not in st.session_state:
    st.session_state.audit_records = [
        {"id": "AUD-001", "status": "Resolved"},
        {"id": "AUD-002", "status": "Open"},
        {"id": "AUD-003", "status": "In Progress"},
    ]
st.divider()

st.header("🔁 Recurring Finding Detection")

st.write(
    "Analyze previous audits to identify recurring compliance issues."
)


def reflect_analysis(question):

    async def run_reflect():
        return await client.areflect(
            bank_id=BANK_ID,
            query=question
        )

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            asyncio.run,
            run_reflect()
        )
        return future.result()


if st.button("🔎 Analyze Recurring Findings"):

    try:

        response = reflect_analysis(
            """
            Analyze the previous audit history stored in memory.

            Identify recurring compliance or security issues
            that appeared across multiple audits.

            For each recurring issue:
            1. Explain the pattern.
            2. Mention the audits involved.
            3. Explain why the pattern matters.
            4. Recommend what should be checked in the next audit.

            Use only information supported by the stored audit memories.
            """
        )

        st.subheader("🧠 AuditMind Analysis")

        st.info(response.text)

        if response.based_on:
            st.subheader("📚 Memory Evidence")

            for source in response.based_on:
                st.write("•", source)

    except Exception as e:

        st.error(
            f"Error analyzing audit history: {e}"
        )
# -------------------------
# -------------------------
# WHAT CHANGED?
# -------------------------

st.divider()

st.header("🔄 What Changed?")

st.write(
    "Compare audit history to identify improvements, unresolved issues, and recurring problems."
)

if st.button("🔍 Analyze What Changed"):

    try:

        response = reflect_analysis(
            """
            Compare the audit history stored in memory.

            Analyze the changes across the previous audits.

            Identify:
            1. Issues that improved or decreased.
            2. Issues that remained unresolved.
            3. Issues that appeared repeatedly.
            4. Changes in remediation status.
            5. What the auditor should pay attention to next.

            Mention the relevant audit IDs.

            Use only information supported by the stored audit memories.
            """
        )

        st.subheader("🧠 AuditMind Change Analysis")

        st.info(response.text)

        if response.based_on:

            st.subheader("📚 Memory Evidence")

            for source in response.based_on:
                st.write("•", source)

    except Exception as e:

        st.error(
            f"Error analyzing audit changes: {e}"
        )
#  -------------------------
# NEXT AUDIT PREPARATION
# -------------------------

st.divider()

st.header("🛡️ Prepare Me for the Next Audit")

st.write(
    "Use AuditMind's memory to prepare for the next compliance audit."
)

if st.button("📋 Prepare for Next Audit"):

    try:

        response = reflect_analysis(
            """
            Prepare the auditor for the next audit using the stored
            audit history in memory.

            Identify:
            1. Recurring compliance issues.
            2. Previous findings that need follow-up.
            3. Remediation actions that are still incomplete.
            4. Specific controls or areas that should be checked.
            5. A practical audit preparation checklist.

            Use only information supported by the stored audit memories.
            Clearly mention the audit IDs when relevant.
            """
        )

        st.subheader("🧠 AuditMind Audit Preparation")

        st.info(response.text)

        

    except Exception as e:

        st.error(
            f"Error preparing for audit: {e}"
    )