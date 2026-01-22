import streamlit as st
from retrieve import BlockchainRAG

# 1. Page Configuration
st.set_page_config(page_title="BLOCKBOT | Mihika", page_icon="⛓️", layout="centered")

# 2. Branding
st.title("BLOCKBOT")
st.markdown("### **by Mihika**")
st.markdown("*Technical Blockchain Assistant*")
st.divider()

# 3. Initialize Engine & History
if "rag_engine" not in st.session_state:
    with st.spinner("🔧 Calibrating Blockchain Engine..."):
        try:
            st.session_state.rag_engine = BlockchainRAG()
        except Exception as e:
            st.error(f"Connection Error: {e}")
            st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. User Input
if prompt := st.chat_input("Ask a technical question..."):
    # Add user message to UI and history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Logic
    with st.chat_message("assistant"):
        with st.status("🔍 Analyzing Whitepapers...", expanded=False) as status:
            # FIX: Only call the function ONCE
            result = st.session_state.rag_engine.ask(prompt)
            
            # Safe Unpacking: Ensure response is a string and sources is a list
            response = str(result[0])
            sources = result[1] if len(result) > 1 else []
            
            status.update(label="Analysis Complete!", state="complete")
        
        # Display the whole response at once
        st.markdown(response)

        # 6. Improved Reference Logic
        if sources:
            st.divider()
            st.caption("📑 **Referenced below:**")
            source_names = []
            for doc in sources:
                if hasattr(doc, 'metadata'):
                    raw_path = doc.metadata.get('source', 'Unknown Paper')
                    filename = raw_path.split('\\')[-1].split('/')[-1]
                    source_names.append(filename)
            
            if source_names:
                unique_sources = sorted(list(set(source_names)))
                # Show sources as a clean comma-separated list
                st.info(f"Source Material: {', '.join(unique_sources)}")
        else:
            st.warning("⚠️ No relevant sections found in the whitepapers.")

        # Save assistant message to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        