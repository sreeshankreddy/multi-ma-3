"""
Multimodal Document Analyzer - Main Streamlit Application
Intelligent AI-powered document analysis system supporting multiple file formats.
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
import pandas as pd
from pathlib import Path
from models.document_model import DocumentAnalyzer
from database.db import DatabaseManager
from utils.report_generator import ReportGenerator


# Configuration
st.set_page_config(
    page_title="Multimodal Document Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = DocumentAnalyzer()
    if 'db' not in st.session_state:
        st.session_state.db = DatabaseManager()
    if 'current_user_id' not in st.session_state:
        st.session_state.current_user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_document_id' not in st.session_state:
        st.session_state.current_document_id = None
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False


def show_login_page():
    """Display login and registration page."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🔐 Multimodal Document Analyzer")
        st.markdown("---")

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.subheader("Login to Your Account")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", use_container_width=True):
                user_id = st.session_state.db.authenticate_user(username, password)
                if user_id:
                    st.session_state.current_user_id = user_id
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            st.subheader("Create New Account")
            new_username = st.text_input("Username", key="register_username")
            new_email = st.text_input("Email", key="register_email")
            new_password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")

            if st.button("Register", use_container_width=True):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif not new_username or not new_email:
                    st.error("Please fill all fields")
                else:
                    if st.session_state.db.register_user(new_username, new_email, new_password):
                        st.success("Account created! Please log in.")
                    else:
                        st.error("Username or email already exists")


def show_document_upload():
    """Display document upload interface."""
    st.header("📤 Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "jpg", "jpeg", "png", "docx", "txt"],
        help="Supported formats: PDF, JPG, PNG, DOCX, TXT"
    )

    if uploaded_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            tmp_path = tmp_file.name

        # Show file info & Progress
        with st.status("Processing...", expanded=True) as status:
            st.write("Reading file...")
            progress_bar = st.progress(0)
            
            # Show file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                st.metric("File Size", f"{uploaded_file.size / 1024:.2f} KB")
            with col3:
                st.metric("File Type", Path(uploaded_file.name).suffix.upper())
            progress_bar.progress(30)
            
            # Analyze button
            if st.button("🔍 Analyze Document", use_container_width=True):
                st.write("Analyzing content with AI...")
                
                # Load document
                success, text = st.session_state.analyzer.load_document(tmp_path)
                progress_bar.progress(60)

                if success:
                    # Perform analysis
                    import asyncio
                    analyzer = st.session_state.analyzer
                    analyzer.analysis_results = asyncio.run(analyzer.analyze_text_async())
                    progress_bar.progress(90)

                    # Save to database
                    doc_id = st.session_state.db.save_document(
                        st.session_state.current_user_id,
                        uploaded_file.name,
                        tmp_path,
                        Path(uploaded_file.name).suffix.lower(),
                        uploaded_file.size
                    )
                    st.session_state.current_document_id = doc_id

                    # Save analysis results
                    st.session_state.db.save_analysis_result(
                        doc_id,
                        analyzer.analysis_results.get('summary', ''),
                        analyzer.analysis_results.get('keywords', []),
                        analyzer.analysis_results.get('entities', {}),
                        analyzer.analysis_results.get('topics', []),
                        str(analyzer.analysis_results.get('sentiment', {})),
                        text[:5000],
                        str(analyzer.tables)
                    )
                    
                    progress_bar.progress(100)
                    status.update(label="Analysis Complete!", state="complete")
                    
                    st.session_state.show_analysis = True
                    st.rerun()
                else:
                    status.update(label="Analysis Failed!", state="error")
                    st.error(f"Error: {text}")

        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def show_analysis_results():
    """Display document analysis results."""
    if not st.session_state.analyzer.extracted_text:
        st.info("Please upload and analyze a document first.")
        return

    st.header("📊 Analysis Results")

    analyzer = st.session_state.analyzer
    results = analyzer.analysis_results

    # Create tabs for different analysis views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Summary",
        "Keywords",
        "Entities",
        "Statistics",
        "Tables",
        "Chat"
    ])

    with tab1:
        st.subheader("Document Summary")
        if 'summary' in results:
            st.markdown(results['summary'])
        else:
            st.info("No summary available")

        # Bullet points
        if 'bullet_points' in results:
            st.subheader("Key Points")
            for point in results['bullet_points']:
                st.markdown(f"• {point}")

    with tab2:
        st.subheader("Keywords & Topics")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Top Keywords:**")
            keywords = results.get('keywords', [])
            if keywords:
                keyword_df = pd.DataFrame({
                    'Keyword': keywords[:10],
                    'Rank': range(1, len(keywords[:10]) + 1)
                })
                st.dataframe(keyword_df, use_container_width=True)
            else:
                st.info("No keywords extracted")

        with col2:
            st.markdown("**Main Topics:**")
            topics = results.get('topics', [])
            if topics:
                topic_df = pd.DataFrame({
                    'Topic': topics,
                    'Type': ['Main' if i == 0 else 'Related' for i, _ in enumerate(topics)]
                })
                st.dataframe(topic_df, use_container_width=True)
            else:
                st.info("No topics identified")

    with tab3:
        st.subheader("Extracted Entities")
        entities = results.get('entities', {})

        if entities:
            for entity_type, entity_list in entities.items():
                if entity_list:
                    st.markdown(f"**{entity_type}**")
                    entity_text = ", ".join(entity_list[:5])
                    st.text(entity_text)
        else:
            st.info("No entities extracted")

        # Sentiment
        if 'sentiment' in results:
            st.markdown("---")
            st.subheader("Sentiment Analysis")
            sentiment = results['sentiment']
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Sentiment",
                    sentiment.get('overall_sentiment', 'N/A'),
                    sentiment.get('confidence', 0)
                )

            with col2:
                st.metric(
                    "Positive Sentences",
                    sentiment.get('positive_sentences', 0)
                )

            with col3:
                st.metric(
                    "Negative Sentences",
                    sentiment.get('negative_sentences', 0)
                )

    with tab4:
        st.subheader("Document Statistics")
        stats = results.get('statistics', {})

        if stats:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Words", stats.get('total_words', 0))

            with col2:
                st.metric("Total Sentences", stats.get('total_sentences', 0))

            with col3:
                st.metric("Unique Words", stats.get('unique_words', 0))

            with col4:
                st.metric("Reading Time", f"{stats.get('reading_time_minutes', 0)} min")

            st.markdown("---")
            stats_df = pd.DataFrame({
                'Metric': list(stats.keys()),
                'Value': [str(v) for v in stats.values()]
            })
            st.dataframe(stats_df, use_container_width=True)

    with tab5:
        st.subheader("Extracted Tables")
        tables = analyzer.tables

        if tables:
            for i, table_info in enumerate(tables):
                st.markdown(f"**Table {i + 1}** (Page {table_info.get('page_number', 'N/A')})")

                # Display table
                table_data = table_info.get('data', [])
                if table_data:
                    df = pd.DataFrame(table_data)
                    st.dataframe(df, use_container_width=True)

                    # Download options
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label=f"Download Table {i + 1} as CSV",
                        data=csv_data,
                        file_name=f"table_{i + 1}.csv",
                        mime="text/csv"
                    )

                st.markdown("---")
        else:
            st.info("No tables found in document")

    with tab6:
        st.subheader("Chat with Document")
        show_document_chat()


def show_document_chat():
    """Display document Q&A interface."""
    st.markdown("Ask questions about the document and get intelligent answers.")

    # Chat history
    if st.session_state.chat_history:
        st.markdown("**Chat History:**")
        for i, (question, answer) in enumerate(st.session_state.chat_history[-5:]):
            with st.container():
                st.markdown(f"**Q{i + 1}:** {question}")
                st.info(f"**A:** {answer}")

    # Question input
    col1, col2 = st.columns([5, 1])

    with col1:
        question = st.text_input("Ask a question about the document:")

    with col2:
        if st.button("Send", use_container_width=True):
            if question:
                with st.spinner("Thinking..."):
                    result = st.session_state.analyzer.answer_question(question)

                    if 'error' not in result:
                        answer = result.get('answer', 'No answer found')
                        confidence = result.get('confidence', 0)

                        # Store in chat history
                        st.session_state.chat_history.append((question, answer))

                        # Save to database
                        if st.session_state.current_document_id:
                            st.session_state.db.save_chat_message(
                                st.session_state.current_document_id,
                                question,
                                answer
                            )

                        # Display answer
                        st.success(f"Confidence: {confidence:.2%}")
                        st.markdown(f"**Answer:** {answer}")
                    else:
                        st.error(result['error'])


def show_document_history():
    """Display user's document upload history."""
    st.header("📚 Document History")

    if not st.session_state.current_user_id:
        st.warning("Please log in first")
        return

    # Get user documents
    documents = st.session_state.db.get_user_documents(st.session_state.current_user_id)

    if documents:
        # Create DataFrame
        df = pd.DataFrame(documents)
        df['upload_date'] = pd.to_datetime(df['upload_date']).dt.strftime('%Y-%m-%d %H:%M')

        st.dataframe(
            df[['filename', 'file_type', 'file_size', 'upload_date']],
            use_container_width=True
        )

        # Search
        search_term = st.text_input("Search documents:")
        if search_term:
            results = st.session_state.db.search_documents(
                st.session_state.current_user_id,
                search_term
            )
            if results:
                st.markdown("**Search Results:**")
                for doc in results:
                    st.text(f"{doc['filename']} (uploaded: {doc['upload_date']})")
            else:
                st.info("No documents found")
    else:
        st.info("No documents uploaded yet")


def show_report_generation():
    """Display report generation interface."""
    st.header("📋 Generate Report")

    if not st.session_state.analyzer.extracted_text:
        st.info("Please analyze a document first")
        return

    st.markdown("Select report format(s) to generate:")

    col1, col2 = st.columns(2)

    with col1:
        generate_pdf = st.checkbox("📄 PDF Report")
        generate_txt = st.checkbox("📝 Text Report")

    with col2:
        generate_html = st.checkbox("🌐 HTML Report")
        generate_json = st.checkbox("📊 JSON Report")

    if st.button("Generate Reports", use_container_width=True):
        with st.spinner("Generating reports..."):
            output_dir = "reports"

            results = ReportGenerator.generate_all_reports(
                st.session_state.analyzer.analysis_results,
                output_dir,
                document_title="Multimodal Document Analysis Report"
            )

            # Display download buttons
            st.markdown("**Generated Reports:**")

            for format_type, filepath in results.items():
                if os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        file_data = f.read()

                    mime_types = {
                        'pdf': 'application/pdf',
                        'txt': 'text/plain',
                        'html': 'text/html',
                        'json': 'application/json'
                    }

                    st.download_button(
                        label=f"Download {format_type.upper()}",
                        data=file_data,
                        file_name=os.path.basename(filepath),
                        mime=mime_types.get(format_type, 'application/octet-stream')
                    )


def show_settings():
    """Display settings page."""
    st.header("⚙️ Settings")

    st.subheader("User Profile")
    if st.session_state.current_user_id:
        user = st.session_state.db.get_user(st.session_state.current_user_id)
        if user:
            st.text(f"Username: {user['username']}")
            st.text(f"Email: {user['email']}")
            st.text(f"Member Since: {user['created_at']}")

    st.markdown("---")

    st.subheader("Display Settings")
    dark_mode = st.checkbox("Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode

    st.markdown("---")

    if st.button("Logout", use_container_width=True, type="secondary"):
        st.session_state.current_user_id = None
        st.session_state.username = None
        st.session_state.chat_history = []
        st.success("Logged out successfully")
        st.rerun()


def main():
    """Main application function."""
    initialize_session_state()

    # Check if user is logged in
    if not st.session_state.current_user_id:
        show_login_page()
        return

    # Sidebar navigation
    st.sidebar.title("🗂️ Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Upload", "Analysis", "History", "Reports", "Settings"]
    )

    # Main content
    if page == "Upload":
        show_document_upload()

    elif page == "Analysis":
        show_analysis_results()

    elif page == "History":
        show_document_history()

    elif page == "Reports":
        show_report_generation()

    elif page == "Settings":
        show_settings()

    # Footer
    st.markdown("---")
    st.markdown(
        "Multimodal Document Analyzer v1.0 | "
        "Powered by AI | "
        "Built with Streamlit"
    )


if __name__ == "__main__":
    main()
