"""
Visual Memory Search - Main Streamlit Application
A fast visual memory search tool that indexes screenshots and enables natural language queries.
"""

import os
import time
import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from typing import List, Optional
from processor import ScreenshotProcessor
from search_engine import SearchEngine

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not available, skip


# Page configuration
st.set_page_config(
    page_title="Visual Memory Search",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .result-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .confidence-high { color: #22c55e; font-weight: bold; }
    .confidence-medium { color: #f59e0b; font-weight: bold; }
    .confidence-low { color: #ef4444; font-weight: bold; }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'processor' not in st.session_state:
        st.session_state.processor = None
    if 'search_engine' not in st.session_state:
        st.session_state.search_engine = SearchEngine()
    if 'processed_images' not in st.session_state:
        st.session_state.processed_images = []
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'total_processing_time' not in st.session_state:
        st.session_state.total_processing_time = 0


def get_api_key() -> Optional[str]:
    """
    Get API key from various sources in order of preference.
    
    Returns:
        API key string or None
    """
    # 1. Check Streamlit secrets
    try:
        if 'ANTHROPIC_API_KEY' in st.secrets:
            return st.secrets['ANTHROPIC_API_KEY']
    except:
        pass
    
    # 2. Check environment variable
    if 'ANTHROPIC_API_KEY' in os.environ:
        return os.environ['ANTHROPIC_API_KEY']
    
    # 3. Use session state (from UI input)
    return st.session_state.api_key


def image_to_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string for display."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def load_sample_screenshots():
    """Load sample screenshots from the repository."""
    sample_dir = "sample_screenshots"
    if os.path.exists(sample_dir):
        sample_files = []
        for file in os.listdir(sample_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                sample_files.append(os.path.join(sample_dir, file))
        return sample_files
    return []


def load_folder_screenshots(folder_path: str):
    """Load screenshots from a specified folder."""
    if not os.path.exists(folder_path):
        return []
    
    screenshot_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                screenshot_files.append(os.path.join(root, file))
    
    return screenshot_files


def process_images(image_files: List, processor: ScreenshotProcessor) -> List:
    """Process uploaded or sample images."""
    processed = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, file in enumerate(image_files):
        # Update progress
        progress = (idx + 1) / len(image_files)
        progress_bar.progress(progress)
        
        # Handle different file types
        if hasattr(file, 'read'):  # Uploaded file
            # Save temporary file
            temp_path = f"temp_{file.name}"
            with open(temp_path, 'wb') as f:
                f.write(file.read())
            status_text.text(f"Processing {file.name}...")
            result = processor.process_image(temp_path)
            result['image'] = Image.open(temp_path)
            os.remove(temp_path)  # Clean up
        else:  # File path (sample)
            status_text.text(f"Processing {os.path.basename(file)}...")
            result = processor.process_image(file)
            result['image'] = Image.open(file)
        
        processed.append(result)
    
    progress_bar.empty()
    status_text.empty()
    return processed


def display_search_results(results: List):
    """Display search results in a grid layout."""
    if not results:
        st.warning("No results found. Try a different query.")
        return
    
    st.subheader(f"Found {len(results)} results")
    
    # Create columns for grid layout
    cols = st.columns(2)
    
    for idx, (metadata, confidence) in enumerate(results):
        col = cols[idx % 2]
        
        with col:
            # Determine confidence level for styling
            if confidence > 0.7:
                conf_class = "confidence-high"
            elif confidence > 0.4:
                conf_class = "confidence-medium"
            else:
                conf_class = "confidence-low"
            
            # Create result card
            with st.container():
                st.markdown(f"""
                    <div class="result-card">
                        <h4>{metadata['filename']}</h4>
                        <p class="{conf_class}">Confidence: {confidence:.2%}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display image thumbnail
                for img_data in st.session_state.processed_images:
                    if img_data['path'] == metadata['path']:
                        st.image(img_data['image'], use_column_width=True)
                        break
                
                # Show text previews in expander
                with st.expander("View extracted content"):
                    if metadata.get('ocr_text_preview'):
                        st.text("OCR Text:")
                        st.text(metadata['ocr_text_preview'][:300] + "...")
                    if metadata.get('vision_preview'):
                        st.text("\nVision Description:")
                        st.text(metadata['vision_preview'][:300] + "...")


def main():
    """Main application flow."""
    init_session_state()
    
    # Title and description
    st.title("🔍 Visual Memory Search")
    st.markdown("**Search your screenshots using natural language - find text content or visual elements instantly!**")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key management
        st.subheader("API Configuration")
        api_key = get_api_key()
        
        if not api_key:
            st.error("⚠️ **No API key detected**")
            st.markdown("**For better visual search results:**")
            
            with st.expander("🌐 **Streamlit Cloud Setup** (Recommended)", expanded=True):
                st.markdown("""
                1. Click the **⚙️ icon** (app settings)
                2. Go to **"Secrets"** tab
                3. Add: `ANTHROPIC_API_KEY = "your-key"`
                4. **Save** (app will restart)
                """)
            
            with st.expander("💻 **Local Development**"):
                st.markdown("""
                Create `.env` file:
                ```
                ANTHROPIC_API_KEY=your-key-here
                ```
                """)
            
            st.markdown("**Or enter temporarily:**")
            user_key = st.text_input(
                "Anthropic API Key",
                type="password",
                help="Temporary - not saved between sessions"
            )
            if user_key:
                st.session_state.api_key = user_key
                api_key = user_key
                st.rerun()
        else:
            st.success("✅ **Enhanced Search Mode Active**")
            st.markdown("🚀 Using OCR + AI Vision Descriptions")
            if st.button("Clear API Key"):
                st.session_state.api_key = None
                st.rerun()
        
        # Initialize processor with API key
        if st.session_state.processor is None or \
           (api_key and st.session_state.processor.api_key != api_key):
            st.session_state.processor = ScreenshotProcessor(api_key)
        
        # Stats
        st.subheader("📊 Statistics")
        stats = st.session_state.search_engine.get_stats()
        st.metric("Indexed Images", stats['total_documents'])
        if st.session_state.total_processing_time > 0:
            st.metric("Processing Time", f"{st.session_state.total_processing_time:.1f}s")
        
        # Mode indicator
        st.subheader("🔧 Mode")
        if api_key:
            st.info("Enhanced mode with AI vision")
        else:
            st.warning("Basic mode (OCR only)")
        
        # Clear index button
        if st.button("🗑️ Clear All Data"):
            st.session_state.search_engine.clear_index()
            st.session_state.processed_images = []
            st.session_state.total_processing_time = 0
            st.rerun()
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "🔍 Search", "📚 Help"])
    
    with tab1:
        st.header("Upload Screenshots")
        
        # Create three columns for different input methods
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # File upload
            uploaded_files = st.file_uploader(
                "Choose screenshot files",
                type=['png', '.jpg', 'jpeg', 'gif', 'bmp'],
                accept_multiple_files=True,
                help="Upload multiple screenshots to index for searching"
            )
        
        with col2:
            # Folder input
            folder_path = st.text_input(
                "Or enter folder path",
                placeholder="/path/to/screenshots/folder",
                help="Enter the full path to a folder containing screenshots"
            )
        
        # Processing buttons
        button_col1, button_col2, button_col3 = st.columns(3)
        
        with button_col1:
            if st.button("📁 Load Sample Screenshots", type="primary"):
                # Ensure processor is initialized
                api_key = get_api_key()
                if st.session_state.processor is None or \
                   (api_key and st.session_state.processor.api_key != api_key):
                    st.session_state.processor = ScreenshotProcessor(api_key)
                
                sample_files = load_sample_screenshots()
                if sample_files:
                    with st.spinner(f"Processing {len(sample_files)} sample images..."):
                        start_time = time.time()
                        processed = process_images(sample_files, st.session_state.processor)
                        
                        # Index in search engine
                        indexed = st.session_state.search_engine.index_batch(processed)
                        
                        # Update session state
                        st.session_state.processed_images.extend(processed)
                        st.session_state.total_processing_time += time.time() - start_time
                        
                        st.success(f"✅ Processed and indexed {indexed} sample images!")
                        st.rerun()  # Force refresh to show results immediately
                else:
                    st.error("No sample screenshots found in repository")
        
        with button_col2:
            if uploaded_files and st.button("🚀 Process Uploaded Files", type="primary"):
                # Ensure processor is initialized
                api_key = get_api_key()
                if st.session_state.processor is None or \
                   (api_key and st.session_state.processor.api_key != api_key):
                    st.session_state.processor = ScreenshotProcessor(api_key)
                
                with st.spinner(f"Processing {len(uploaded_files)} images..."):
                    start_time = time.time()
                    processed = process_images(uploaded_files, st.session_state.processor)
                    
                    # Index in search engine
                    indexed = st.session_state.search_engine.index_batch(processed)
                    
                    # Update session state
                    st.session_state.processed_images.extend(processed)
                    st.session_state.total_processing_time += time.time() - start_time
                    
                    st.success(f"✅ Processed and indexed {indexed} images!")
                    st.rerun()  # Force refresh to show results immediately
        
        with button_col3:
            if folder_path and st.button("📂 Process Folder", type="primary"):
                # Ensure processor is initialized
                api_key = get_api_key()
                if st.session_state.processor is None or \
                   (api_key and st.session_state.processor.api_key != api_key):
                    st.session_state.processor = ScreenshotProcessor(api_key)
                
                folder_files = load_folder_screenshots(folder_path)
                if folder_files:
                    with st.spinner(f"Processing {len(folder_files)} images from folder..."):
                        start_time = time.time()
                        processed = process_images(folder_files, st.session_state.processor)
                        
                        # Index in search engine
                        indexed = st.session_state.search_engine.index_batch(processed)
                        
                        # Update session state
                        st.session_state.processed_images.extend(processed)
                        st.session_state.total_processing_time += time.time() - start_time
                        
                        st.success(f"✅ Processed and indexed {indexed} images from folder!")
                        st.rerun()  # Force refresh to show results immediately
                else:
                    st.error(f"No screenshots found in folder: {folder_path}")
        
        # Display processed images
        if st.session_state.processed_images:
            st.subheader("Processed Images")
            
            # Create grid of thumbnails
            cols = st.columns(4)
            for idx, img_data in enumerate(st.session_state.processed_images):
                col = cols[idx % 4]
                with col:
                    st.image(img_data['image'], caption=img_data['filename'], use_column_width=True)
    
    with tab2:
        st.header("Search Your Screenshots")
        
        if st.session_state.search_engine.get_stats()['total_documents'] == 0:
            st.warning("⚠️ No images indexed yet. Please upload and process some screenshots first.")
        else:
            # Search interface
            search_query = st.text_input(
                "Enter your search query",
                placeholder="e.g., 'error message about authentication' or 'screenshot with blue button'",
                help="Search for text content or visual elements in your screenshots"
            )
            
            # Example queries
            st.subheader("Example Queries")
            example_cols = st.columns(3)
            
            examples = [
                "error message",
                "blue button",
                "login form",
                "dark theme",
                "code editor",
                "warning notification",
                "menu bar",
                "graph chart",
                "mobile interface"
            ]
            
            for idx, example in enumerate(examples):
                col = example_cols[idx % 3]
                with col:
                    if st.button(example, key=f"example_{idx}"):
                        search_query = example
            
            # Perform search
            if search_query:
                # Make the search query highly visible
                st.markdown("---")
                st.markdown(f"### 🔍 **Searching for:** \"{search_query}\"")
                
                # Show search mode status
                api_key = get_api_key()
                if api_key:
                    st.success("🚀 **Enhanced Search Mode** - Using OCR + AI Vision Descriptions")
                else:
                    st.warning("⚠️ **Basic Search Mode** - Using OCR Only (Add API key for better visual search)")
                
                with st.spinner("Searching..."):
                    results = st.session_state.search_engine.search(search_query, top_k=5)
                    
                # Show search stats
                if results:
                    st.info(f"📊 Found **{len(results)}** results (sorted by relevance)")
                else:
                    st.error("😔 No results found. Try a different search term or process more images.")
                
                display_search_results(results)
    
    with tab3:
        st.header("📚 How to Use")
        
        st.markdown("""
        ### Getting Started
        
        1. **Configure API Key** (Optional but recommended for better results)
           
           **🌐 For Streamlit Cloud (Recommended):**
           - Go to your app settings (⚙️ icon in Streamlit Cloud)
           - Click **"Secrets"** 
           - Add: `ANTHROPIC_API_KEY = "your-actual-api-key-here"`
           - Save and the app will restart with enhanced search
           
           **💻 For Local Development:**
           - **Option A**: Create `.env` file with `ANTHROPIC_API_KEY=your-key`
           - **Option B**: Set environment variable: `export ANTHROPIC_API_KEY="your-key"`
           - **Option C**: Add API key in sidebar (not recommended for production)
           
           **🔍 Search Modes:**
           - **With API Key**: OCR + AI Visual Descriptions (much better for visual queries)
           - **Without API Key**: OCR text only (basic mode)
        
        2. **Add Screenshots** (Choose any method)
           - **Demo**: Click "Load Sample Screenshots" for demo data
           - **Individual Files**: Use the file uploader for specific images
           - **Folder Processing**: Enter a folder path to process entire directories
           - Supports PNG, JPG, JPEG, GIF, and BMP formats
        
        3. **Search Your Images**
           - Use natural language queries to find screenshots
           - Search for text content: "error message about auth"
           - Search for visual elements: "screenshot with blue button"
           - Try the example queries for inspiration
        
        ### Features
        
        - **OCR Text Extraction**: Automatically extracts text from images
        - **AI Vision Descriptions**: Uses Claude 3 to understand visual content
        - **Semantic Search**: Find images by meaning, not just keywords
        - **Confidence Scores**: See how well each result matches your query
        - **Fast Processing**: Optimized for quick indexing and search
        
        ### Tips
        
        - Be specific in your queries for better results
        - Combine text and visual descriptions in queries
        - Process multiple images at once for efficiency
        - Use the sample screenshots to test the system
        """)
        
        st.info("💡 **Pro Tip**: The more descriptive your query, the better the results!")


if __name__ == "__main__":
    main()