import streamlit as st
import dotenv
dotenv.load_dotenv()

from langchain_groq import ChatGroq

# ───────────────────────────────────
# Setup
# ───────────────────────────────────
st.set_page_config(layout="wide")
st.title("AI - Custom UI Generator")

# Initialize session variables
for key, default in {
    "html": "",
    "prompt": "",
    "mode": None,
    "groq_api_key": "",
    "alert_message": None,
    "alert_level": "error"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ───────────────────────────────────
# Alert System (top of page)
# ───────────────────────────────────
def set_alert(message: str, level: str = "error"):
    st.session_state["alert_message"] = message
    st.session_state["alert_level"] = level

if st.session_state["alert_message"]:
    if st.session_state["alert_level"] == "error":
        st.error(st.session_state["alert_message"])
    elif st.session_state["alert_level"] == "warning":
        st.warning(st.session_state["alert_message"])
    elif st.session_state["alert_level"] == "success":
        st.success(st.session_state["alert_message"])


# ───────────────────────────────────
# Helper to ensure API key
# ───────────────────────────────────
def ensure_api_key() -> bool:
    if not st.session_state["groq_api_key"]:
        set_alert(" Please enter your Groq API key in the sidebar before generating or updating UI.", "warning")
        return False
    return True


# ───────────────────────────────────
# LLM: GENERATE NEW UI
# ───────────────────────────────────
def generate_new_html(prompt: str):
    try:
        llm = ChatGroq(
            model="openai/gpt-oss-safeguard-20b",
            temperature=0.2,
            api_key=st.session_state["groq_api_key"],
        )

        response = llm.invoke(
            f"""
You are an AI reasoning agent.

Your output must follow this format:
Question: {{prompt}}
Thought: (think step-by-step silently and DO NOT show this to the user)
Final Answer: (output ONLY valid HTML with TailwindCSS)

RULES:
- MUST include <script src="https://cdn.tailwindcss.com"></script>
- NO markdown, NO explanation, NO comments
- NO headings like "Final Answer:", output ONLY the HTML

Question: {prompt}
"""
        )
        return response.content

    except Exception as e:
        if "api key" in str(e).lower():
            set_alert(" Invalid Groq API key. Please check and try again.", "error")
        else:
            set_alert(f" Error generating UI: {e}", "error")
        return None


# ───────────────────────────────────
# LLM: MODIFY EXISTING UI
# ───────────────────────────────────
def modify_existing_html(current_html: str, prompt: str):
    try:
        llm = ChatGroq(
            model="openai/gpt-oss-safeguard-20b",
            temperature=0.2,
            api_key=st.session_state["groq_api_key"],
        )

        response = llm.invoke(
            f"""
You are an AI reasoning agent.

Thought: (think silently and DO NOT show this to the user)
Final Answer: (output ONLY updated HTML)

RULES:
- Keep existing UI unless change is requested
- MUST retain <script src="https://cdn.tailwindcss.com"></script>
- NO markdown, NO comments, NO explanation
- NO headings like "Final Answer:", output ONLY the updated HTML

Existing HTML:
{current_html}

Modify based on:
{prompt}
"""
        )
        return response.content

    except Exception as e:
        if "api key" in str(e).lower():
            set_alert("Invalid Groq API key. Please check and try again.", "error")
        else:
            set_alert(f"Error updating UI: {e}", "error")
        return None


# ───────────────────────────────────
# UI LAYOUT
# ───────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.sidebar.subheader(" Enter your Groq API Key (required)")
    user_key = st.sidebar.text_input("Groq API Key", type="password")
    if user_key:
        st.session_state["groq_api_key"] = user_key.strip()

    st.subheader("Prompt")
    prompt = st.text_area("Describe your UI:", height=150)

    if st.button("Generate New"):
        if ensure_api_key():
            st.session_state["mode"] = "new"
            st.session_state["prompt"] = prompt

    if st.button("Update Current"):
        if ensure_api_key():
            st.session_state["mode"] = "update"
            st.session_state["prompt"] = prompt

    st.subheader("HTML Code")
    new_html = st.text_area(
        "HTML Output",
        st.session_state.get("html", ""),
        height=400
    )

    if new_html != st.session_state["html"]:
        st.session_state["html"] = new_html

    if st.session_state.get("html"):
        st.download_button(
            label="Download HTML File",
            data=st.session_state["html"],
            file_name="generated_ui.html",
            mime="text/html"
        )


with right:
    st.subheader("Preview")
    view_mode = st.radio("Preview mode", ["Desktop", "Mobile"], horizontal=True)

    if st.session_state.get("html"):

        # Disable <a> link navigation inside preview
        disable_links_script = """
        <script>
        document.addEventListener("DOMContentLoaded", () => {
            document.querySelectorAll("a").forEach(a => {
                a.addEventListener("click", event => event.preventDefault());
            });
        });
        </script>
        """

        rendered_html = st.session_state["html"] + disable_links_script

        if view_mode == "Desktop":
            st.components.v1.html(rendered_html, height=700, scrolling=True)
        else:
            mobile_template = f"""
            <div style="
                width: 390px;
                margin: auto;
                border: 1px solid #444;
                border-radius: 14px;
                overflow: hidden;
                box-shadow: 0 0 10px rgba(0,0,0,.35);
            ">
                {rendered_html}
            </div>
            """
            st.components.v1.html(mobile_template, height=700, scrolling=True)
    else:
        st.info("Generate a design to preview it here.")


# ───────────────────────────────────
# TRIGGER LLM OPERATIONS
# ───────────────────────────────────
if st.session_state["mode"] == "new":
    html = generate_new_html(st.session_state["prompt"])
    st.session_state["mode"] = None

    if html:  # success
        st.session_state["alert_message"] = None
        st.session_state["html"] = html

    st.rerun()  # rerun always → alert will show immediately


if st.session_state["mode"] == "update":
    if st.session_state["html"]:
        html = modify_existing_html(st.session_state["html"], st.session_state["prompt"])
        st.session_state["mode"] = None

        if html:  # success
            st.session_state["alert_message"] = None
            st.session_state["html"] = html

        st.rerun()
    else:
        set_alert("No design to update. Generate one first.", "warning")
        st.session_state["mode"] = None
        st.rerun()
