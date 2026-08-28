
import streamlit as st

from rag import agent_answer


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Obsidian AI Knowledge Assistant",
    page_icon="🧠",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 Obsidian AI Knowledge Assistant")

st.markdown(
    "Ask questions about your **Obsidian knowledge base**. "
    "The assistant retrieves relevant notes and generates "
    "answers using the retrieved context."
)


st.divider()


# --------------------------------------------------
# Question input
# --------------------------------------------------

st.subheader("💬 Ask your knowledge base")

question = st.text_input(
    "Question",
    placeholder="Example: How does RAG work?",
    label_visibility="collapsed"
)


ask_button = st.button(
    "🔍 Ask AI",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# RAG Pipeline
# --------------------------------------------------

if ask_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner(
            "🔎 Searching your Obsidian knowledge base..."
        ):

            answer, metadatas, documents, distances = agent_answer(
                question
            )


        # --------------------------------------------------
        # Answer
        # --------------------------------------------------

        st.subheader("💡 Answer")

        st.markdown(answer)


        st.divider()


        # --------------------------------------------------
        # Sources
        # --------------------------------------------------

        st.subheader("📚 Sources")

        if not documents:

            st.info("No relevant sources were retrieved.")

        else:

            shown_sources = set()

            for document, metadata, distance in zip(
                documents,
                metadatas,
                distances
            ):

                source = metadata["source"]

                if source not in shown_sources:

                    source_display = (
                        source
                        .replace("data\\vault\\", "")
                        .replace("data/vault/", "")
                    )

                    with st.expander(
                        f"📄 {source_display}"
                    ):

                        col1, col2 = st.columns(2)

                        with col1:

                            st.markdown(
                                f"**Chunk:** "
                                f"{metadata['chunk_id']}"
                            )

                        with col2:

                            st.markdown(
                                f"**Retrieval distance:** "
                                f"{distance:.4f}"
                            )


                        st.markdown(
                            "**Retrieved content**"
                        )

                        st.code(
                            document,
                            language="markdown"
                        )

                    shown_sources.add(source)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "Powered by Retrieval-Augmented Generation (RAG) • "
    "Obsidian Knowledge Base"
)

