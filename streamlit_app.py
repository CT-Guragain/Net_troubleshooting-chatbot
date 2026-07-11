"""
Network Troubleshooting Chatbot — Streamlit UI

Dark, terminal-themed chat interface for network troubleshooting help.
Tries the live Anthropic API first; falls back to a small demo dataset
of canned scenarios if no API key is set or the API call fails.
"""

import os
import streamlit as st
from dotenv import load_dotenv

from demo_data import find_demo_response, GENERIC_FALLBACK

load_dotenv()

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "").strip()

try:
    import anthropic
    CLIENT = anthropic.Anthropic(api_key=API_KEY) if API_KEY else None
except ImportError:
    CLIENT = None

SYSTEM_PROMPT = (
    "You are a senior network engineer helping troubleshoot networking "
    "issues — firewalls, VPNs, SD-WAN, DNS, NAT, and Active Directory. "
    "Give clear, step-by-step diagnostic guidance grounded in real "
    "enterprise practice."
)

TOPIC_SHORTCUTS = {
    "🔥 Firewall": "Help me troubleshoot a firewall policy that's blocking traffic it shouldn't.",
    "🔒 VPN": "My IPsec VPN tunnel won't establish, help me troubleshoot it real.",
    "🌐 SD-WAN": "An SD-WAN link is flapping between active and standby, how do I diagnose it now?",
    "🗂️ Active Directory": "AD replication is failing between two domain controllers, help me troubleshoot.",
}


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_started" not in st.session_state:
        import datetime
        st.session_state.session_started = datetime.datetime.now()


def inject_custom_css():
    st.markdown(
        """
        <style>
        .stChatMessage { font-family: 'Courier New', monospace; }
        .stChatMessage code {
            background-color: #161b22;
            color: #00d9a5;
            padding: 2px 4px;
            border-radius: 4px;
        }
        section[data-testid="stSidebar"] {
            border-right: 1px solid #2a2f38;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_bot_response(user_message: str) -> str:
    """
    Try the live Anthropic API first. On any failure (no key, rate limit,
    connection issue, or other API error), fall back to the demo dataset
    so the app never just crashes or shows a blank response.
    """
    if CLIENT is not None:
        try:
            response = CLIENT.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.content[0].text

        except anthropic.RateLimitError:
            st.warning(
                "⚠️ API rate limit hit — showing a demo response instead.",
                icon="⚠️",
            )
        except anthropic.APIConnectionError:
            st.warning(
                "⚠️ Couldn't reach the API (connection issue) — showing a "
                "demo response instead.",
                icon="⚠️",
            )
        except anthropic.APIError:
            st.warning(
                "⚠️ The API returned an error — showing a demo response "
                "instead.",
                icon="⚠️",
            )
        except Exception:
            st.warning(
                "⚠️ Something unexpected went wrong calling the API — "
                "showing a demo response instead.",
                icon="⚠️",
            )

    demo_reply = find_demo_response(user_message)
    return demo_reply if demo_reply else GENERIC_FALLBACK


def main():
    st.set_page_config(
        page_title="Net Troubleshooter",
        page_icon="🛠️",
        layout="centered",
    )

    init_session_state()
    inject_custom_css()

    st.title("🛠️ Network Troubleshooting Chatbot")

    with st.sidebar:
        st.header("Quick Topics")
        for label, prompt in TOPIC_SHORTCUTS.items():
            if st.button(label, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("Thinking..."):
                    reply = get_bot_response(prompt)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

        st.divider()

        if CLIENT is not None:
            st.success("🟢 Connected — live API mode", icon="🟢")
        else:
            st.info("🟡 Demo mode — no API key set", icon="🟡")

        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_input := st.chat_input("Describe your network issue..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = get_bot_response(user_input)
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
