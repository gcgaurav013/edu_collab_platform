import streamlit as st
from core_engine import AIOrchestrator
from document_handler import extract_text  # Function to wrap PyPDF2
from validator import KnowledgeValidator
import PyPDF2

# --- Page Layout ---
st.set_page_config(page_title="EduCollab AI Prototype", layout="wide")

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* Ensure the report card has black text explicitly */
    .report-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #0e1117;
        color: #000000 !important;  /* Forces text to be black */
        line-height: 1.6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Fix for subheadings inside the report card if any */
    .report-card h1, .report-card h2, .report-card h3, .report-card p {
        color: #000000 !important;
    }
    
    .stCard { border-radius: 10px; padding: 20px; background: white; color: black; }
    </style>
    """, unsafe_allow_html=True)
# --- Sidebar Configuration ---
with st.sidebar:
    st.title("🌐 AI Edu-Collaborator")
    st.markdown("### ⚙️ System Configuration")
    
    selected_provider = st.selectbox("Select AI Model Provider", 
                                     ["Gemini", "Groq", "OpenRouter", "OpenAI"])
    api_key = st.text_input(f"Enter {selected_provider} API Key", type="password")
    
    st.divider()
    nav = st.radio("Navigation", ["Upload & Extract", "Summarization", "Multi-Format Study", "AI Tutor", "Validation Report", "Global Collaboration"])

# --- App Logic ---
if not api_key:
    st.warning(f"Please enter your {selected_provider} API Key to proceed.")
    st.stop()

orchestrator = AIOrchestrator(selected_provider, api_key)

# Initialize Session Data
if 'raw_text' not in st.session_state: st.session_state.raw_text = ""
if 'current_output' not in st.session_state: st.session_state.current_output = ""

# 1. UPLOAD SYSTEM
if nav == "Upload & Extract":
    st.header("📄 PDF Resource Extraction")
    file = st.file_uploader("Upload Lecture Notes / Textbooks", type=['pdf'])
    
    if file:
        with st.spinner("Extracting and cleaning text..."):
            # Call the function from document_handler.py
            extracted_data = extract_text(file)
            
            if "Error" in extracted_data:
                st.error(extracted_data)
            else:
                st.session_state.raw_text = extracted_data
                st.success("Resource successfully ingested into system memory.")
                
                # Show stats
                from document_handler import get_document_stats
                stats = get_document_stats(st.session_state.raw_text)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Word Count", stats["word_count"])
                col2.metric("Reading Time", f"{stats['estimated_reading_time']} min")
                col3.metric("Status", "Validated")
                
                st.text_area("Source Data Preview", st.session_state.raw_text[:1500], height=300)
# 2. SUMMARIZATION
elif nav == "Summarization":
    st.header("📝 Educational Summarization")
    mode = st.radio("Complexity Level", ["Short", "Detailed", "Beginner (ELI5)"])
    if st.button("Generate Summary"):
        with st.spinner("AI processing across global nodes..."):
            prompt = f"Generate a {mode} summary of this document."
            st.session_state.current_output = orchestrator.generate(prompt, st.session_state.raw_text)
            st.markdown(f"### {mode} Summary")
            st.write(st.session_state.current_output)

# 3. MULTI-FORMAT STUDY
elif nav == "Multi-Format Study":
    st.header("🔄 Multi-Format Transformation")
    fmt = st.selectbox("Target Format", ["MCQs", "Flashcards", "Presentation Outline", "Study Notes"])
    lang = st.selectbox("Language", ["English", "Hindi", "Spanish"])
    
    if st.button("Transform Content"):
        with st.spinner("Executing transformation..."):
            prompt = f"Transform this content into {fmt} in {lang} language."
            st.session_state.current_output = orchestrator.generate(prompt, st.session_state.raw_text)
            st.write(st.session_state.current_output)
# --- 4. AI TUTOR SECTION ---
elif nav == "AI Tutor":
    st.header("🤖 Research-Aligned AI Tutor")
    st.info("The tutor is currently grounded to your uploaded document. It will use the selected model to explain concepts and answer queries.")

    # Check if document exists
    if not st.session_state.raw_text:
        st.warning("Please upload a document in the 'Upload & Extract' section first.")
    else:
        # Initialize Chat History for this session
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "I have analyzed your document. How can I help you understand the material better today?"}
            ]

        # Display Chat History
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Ask a question about the study material..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate AI Response
            with st.chat_message("assistant"):
                with st.spinner("Consulting source material..."):
                    # We pass the last 3 exchanges for context + the document text
                    history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
                    
                    full_query = f"""
                    Conversation History:
                    {history_context}
                    
                    Current Question: {prompt}
                    
                    Instruction: Answer the question strictly using the provided document context. 
                    If the answer isn't there, say 'Based on the provided document, I cannot find specific information on that, but I can discuss related concepts like...'
                    """
                    
                    response = orchestrator.generate(full_query, st.session_state.raw_text)
                    
                    # Knowledge Validation Integration (Optional but recommended for research)
                    st.markdown(response)
                    
                    # Add simple validation badge
                    from validator import KnowledgeValidator
                    score, status = KnowledgeValidator.calculate_confidence(st.session_state.raw_text, response)
                    st.caption(f"🛡️ Context Alignment Score: {score}% | {status}")

            # Add AI response to history
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Clear Chat Button
        if st.button("Clear Tutor Conversation"):
            st.session_state.messages = []
            st.rerun()
# 5. KNOWLEDGE VALIDATION (CRITICAL FEATURE)
elif nav == "Validation Report":
    st.header("🛡️ Knowledge Validation System")
    if not st.session_state.current_output:
        st.error("No generated content found to validate.")
    else:
        score, status = KnowledgeValidator.calculate_confidence(st.session_state.raw_text, st.session_state.current_output)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("System Confidence Score", f"{score}%")
        with col2:
            st.info(f"Status: {status}")
            
        st.subheader("Factual Alignment Report")
        with st.spinner("Performing AI-based cross-check..."):
            ai_check = KnowledgeValidator.ai_fact_check(orchestrator, st.session_state.raw_text, st.session_state.current_output)
            st.markdown(f"<div class='report-card'>{ai_check}</div>", unsafe_allow_html=True)

# 6. GLOBAL COLLABORATION
import streamlit as st
from collaboration import CollabHub

# Initialize Hub
hub = CollabHub()

if nav == "Global Collaboration":
    st.title("🌐 Global Research & Collaboration Hub")
    st.markdown("---")

    # 1. SUBMISSION SECTION
    with st.expander("📤 Publish Your Validated Resource to the World"):
        col1, col2 = st.columns(2)
        with col1:
            res_title = st.text_input("Resource Title", placeholder="e.g. Neural Networks Intro")
            author_name = st.text_input("Contributor Name/ID", placeholder="Anonymous")
        with col2:
            st.info("Validation Requirement: Only resources with a Confidence Score > 80% are eligible for the Global Repository.")
            
        if st.button("🚀 Push to Global Cloud"):
            if 'current_output' in st.session_state and st.session_state.current_output:
                # Logic to fetch current validation score
                from validator import KnowledgeValidator
                score, _ = KnowledgeValidator.calculate_confidence(st.session_state.raw_text, st.session_state.current_output)
                
                if score >= 80:
                    hub.publish_resource(res_title, st.session_state.current_output, author_name, selected_provider, score, "English")
                    st.success("Resource successfully broadcast to the global network!")
                else:
                    st.error(f"Validation failed (Score: {score}%). Please refine the content before publishing.")
            else:
                st.error("No content generated to publish yet.")

    st.markdown("### 🛰️ Live Educational Feed")
    
    # 2. THE FEED
    search_q = st.text_input("🔍 Search global resources...", placeholder="Topic, Model, or Author")
    
    feed = hub.get_all()
    
    for item in feed:
        if search_q.lower() in item['title'].lower() or search_q.lower() in item['content'].lower():
            with st.container():
                # Design a "Card" for each resource
                st.markdown(f"""
                <div style="background-color: white; padding: 20px; border-radius: 10px; border-left: 10px solid #4CAF50; margin-bottom: 20px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="margin:0; color: #1E1E1E;">{item['title']}</h3>
                    <p style="color: grey; font-size: 0.8em;">Contributor: {item['author']} | AI Model: {item['model']} | Language: {item['language']}</p>
                    <div style="display: flex; align-items: center;">
                        <span style="background-color: #E8F5E9; color: #2E7D32; padding: 5px 10px; border-radius: 15px; font-weight: bold;">
                            Confidence Score: {item['score']}%
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns([1,1,2])
                with c1:
                    if st.button(f"👁️ View Content", key=f"view_{item['timestamp']}"):
                        st.info(item['content'])
                with c2:
                    if st.button(f"🔄 Adopt & Translate", key=f"trans_{item['timestamp']}"):
                        target_lang = st.selectbox("Select Target Language", ["Hindi", "Spanish", "French"], key=f"lang_{item['timestamp']}")
                        with st.spinner("Translating for your locale..."):
                            translation = orchestrator.generate(f"Translate this to {target_lang}: {item['content']}")
                            st.write(f"**Translated ({target_lang}):**")
                            st.success(translation)
                with c3:
                    if st.button(f"🛡️ Request AI Peer-Review", key=f"rev_{item['timestamp']}"):
                        with st.spinner("Cross-verifying with an independent AI agent..."):
                            # This uses the current model to verify another model's work (Realistic Peer Review)
                            review_prompt = f"Critically evaluate this educational content for accuracy. Is it reliable? Content: {item['content']}"
                            review = orchestrator.generate(review_prompt)
                            st.markdown(f"**Peer Review Report:**\n\n{review}")