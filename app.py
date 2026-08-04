import uuid
import streamlit as st
from langchain_core.messages import HumanMessage

from test import (
    workflow,
    retrieve_all_threads,
    ingest_pdf,
    thread_has_document,
    thread_document_metadata,
)


# =============================================================================
# Page config & styling
# =============================================================================
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container {padding-top: 2rem; max-width: 900px;}
        [data-testid="stChatMessage"] {padding: 0.15rem 0;}
        .thread-btn button {
            text-align: left !important;
            border-radius: 8px !important;
        }
        .doc-badge {
            background: #10b98122;
            border: 1px solid #10b98155;
            color: #10b981;
            padding: 0.4rem 0.6rem;
            border-radius: 8px;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# Utility functions
# =============================================================================
def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():
    """Start a brand-new conversation thread."""
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []
    st.session_state["processed_upload"] = None


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    """Pull the saved message list for a thread out of the checkpointer."""
    state = workflow.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])


def thread_label(thread_id):
    messages = load_conversation(thread_id)
    for m in messages:
        if m.type == "human":
            text = m.content.strip().replace("\n", " ")
            return text[:30] + ("…" if len(text) > 30 else "")
    return "New Chat"


# =============================================================================
# Session state initialization
# =============================================================================
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "thread_id" not in st.session_state:
    reset_chat()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "processed_upload" not in st.session_state:
    st.session_state["processed_upload"] = None  # tracks last file name ingested for current thread


# =============================================================================
# Sidebar — New Chat, Resume Chat, Upload Document
# =============================================================================
with st.sidebar:
    st.markdown("## 💬 AI ChatBot")

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        reset_chat()
        st.rerun()

    st.divider()

    # -------- Document upload (RAG) --------
    st.caption("KNOWLEDGE BASE")

    current_thread = st.session_state["thread_id"]

    if thread_has_document(current_thread):
        meta = thread_document_metadata(current_thread)
        st.markdown(
            f'<div class="doc-badge">📄 <b>{meta.get("filename","document.pdf")}</b><br>'
            f'{meta.get("documents",0)} pages · {meta.get("chunks",0)} chunks indexed</div>',
            unsafe_allow_html=True,
        )
    else:
        st.caption("No document uploaded for this chat yet.")

    uploaded_file = st.file_uploader(
        "Upload a PDF to chat with it",
        type=["pdf"],
        key=f"uploader_{current_thread}",
    )

    if uploaded_file is not None and st.session_state["processed_upload"] != uploaded_file.name:
        with st.spinner(f"Indexing '{uploaded_file.name}'…"):
            try:
                summary = ingest_pdf(
                    uploaded_file.getvalue(),
                    thread_id=current_thread,
                    filename=uploaded_file.name,
                )
                st.session_state["processed_upload"] = uploaded_file.name
                st.success(
                    f"Indexed {summary['documents']} pages "
                    f"({summary['chunks']} chunks). Ask away!"
                )
                st.rerun()
            except Exception as e:
                st.error(f"Failed to index PDF: {e}")

    st.divider()
    st.caption("YOUR CONVERSATIONS")

    # Most recent thread first — "Resume Chat"
    for tid in reversed(st.session_state["chat_threads"]):
        is_active = tid == st.session_state["thread_id"]
        icon = "🟢" if is_active else ("📄" if thread_has_document(tid) else "💭")
        label = f"{icon} {thread_label(tid)}"

        st.markdown('<div class="thread-btn">', unsafe_allow_html=True)
        if st.button(label, key=f"thread_{tid}", use_container_width=True):
            st.session_state["thread_id"] = tid
            messages = load_conversation(tid)

            temp_history = []
            for msg in messages:
                role = "user" if msg.type == "human" else "assistant"
                if msg.type in ("human", "ai") and msg.content:
                    temp_history.append({"role": role, "content": msg.content})

            st.session_state["message_history"] = temp_history
            st.session_state["processed_upload"] = (
                thread_document_metadata(tid).get("filename")
                if thread_has_document(tid)
                else None
            )
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    if not st.session_state["chat_threads"]:
        st.caption("No saved conversations yet.")


# =============================================================================
# Main chat area
# =============================================================================
st.markdown("## AI Assistant")
st.caption(f"Thread ID: `{st.session_state['thread_id']}`")

# Render existing history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask a question, or ask about your uploaded PDF…")

if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    def stream_response():
        """
        Stream only the final assistant text back to the UI.
        Tool-call chunks (empty content, since the model is requesting a tool
        rather than answering) are skipped automatically because we only
        yield chunks that have non-empty .content.
        """
        for message_chunk, metadata in workflow.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        ):
            if message_chunk.content:
                yield message_chunk.content

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            full_response = st.write_stream(stream_response())

    st.session_state["message_history"].append(
        {"role": "assistant", "content": full_response}
    )