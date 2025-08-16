# Visual Memory Search

A fast visual memory search tool that indexes screenshots and enables natural language queries for both text content and visual elements using Claude 3 vision. Users can search "error message about auth" or "screenshot with blue button" and get ranked results with confidence scores.

## Live Demo

**Deployment URL**: https://1-visual-memory-search.streamlit.app

## Features

- **OCR Text Extraction**: Automatically extracts text from screenshots using Tesseract
- **AI Vision Descriptions**: Uses Claude 3 Haiku to understand visual content and UI elements
- **Semantic Search**: Find images by meaning, not just keywords
- **Natural Language Queries**: Search like "error message about authentication" or "blue button interface"
- **Confidence Scores**: See how well each result matches your query
- **Fast Processing**: Optimized for quick indexing and search
- **Demo Ready**: Includes sample screenshots for immediate testing

## Tech Stack

- **Framework**: Streamlit (Community Cloud deployment)
- **Vision AI**: Anthropic Claude 3 Haiku
- **OCR**: pytesseract + Pillow
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (in-memory)
- **Deployment**: Streamlit Community Cloud

## Project Structure

```
1-visual-memory-search/
├── streamlit_app.py       # Main Streamlit application
├── processor.py           # Image processing, OCR & Claude vision
├── search_engine.py       # Vector search and ranking
├── requirements.txt       # Python dependencies
├── packages.txt          # System packages (tesseract)
├── sample_screenshots/   # Demo images
├── .streamlit/
│   ├── config.toml       # Streamlit configuration
│   └── secrets.toml.example  # API key template
├── architecture.md       # System architecture documentation
├── CLAUDE.md            # Development notes and context
└── README.md
```

## Quick Start

### Option 1: Streamlit Community Cloud (Recommended)

1. **Fork this repository** to your GitHub account
2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from your forked repository
3. **Add API Key** (optional but recommended):
   - In Streamlit Cloud dashboard, go to your app settings
   - Add secrets: `ANTHROPIC_API_KEY = "your-api-key-here"`
   - Without API key, the tool runs in OCR-only mode

### Option 2: Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jamestyack/1-visual-memory-search.git
   cd 1-visual-memory-search
   ```

2. **Install system dependencies** (macOS with Homebrew):
   ```bash
   brew install tesseract
   ```
   
   **On Ubuntu/Debian**:
   ```bash
   sudo apt-get install tesseract-ocr tesseract-ocr-eng
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key** (optional):
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   # Or create .env file with: ANTHROPIC_API_KEY=your-api-key-here
   ```

5. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Open in browser**: Navigate to `http://localhost:8501`

## How to Use

### 1. Get Started with Demo Data
- Click **"Load Sample Screenshots"** to try the tool with included demo images
- Sample screenshots include error dialogs, login forms, dashboards, and more

### 2. Upload Your Screenshots
- Use the file uploader to add your own PNG, JPG, JPEG, GIF, or BMP files
- Or enter a folder path to process entire directories of screenshots
- The tool will process them automatically with OCR and AI vision

### 3. Search Your Images
Try these example queries:
- **Text-based**: "error message", "login form", "authentication failed"
- **Visual-based**: "blue button", "dark theme", "mobile interface"
- **Combined**: "error dialog with red text", "dashboard with charts"

### 4. View Results
- Results are ranked by confidence score
- Click on results to see extracted text and visual descriptions
- Green scores (>70%) indicate high confidence matches

## Configuration

### API Key Setup

The tool works in two modes:

1. **Enhanced Mode** (with Anthropic API key):
   - Rich visual descriptions using Claude 3 Haiku
   - Better search results for visual queries
   - Understands UI elements, colors, themes

2. **Basic Mode** (without API key):
   - OCR text extraction only
   - Still functional for text-based searches
   - No visual understanding

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude 3

### Streamlit Configuration

The app includes optimized settings in `.streamlit/config.toml`:
- 10MB max upload size
- Custom theme colors
- Performance optimizations

## Example Queries That Work Well

**Text Content Queries**:
- "error message"
- "authentication failed"
- "success notification"
- "data table"
- "user management"

**Visual Element Queries**:
- "blue button"
- "dark theme interface"
- "mobile app screen"
- "calendar view"
- "graph or chart"

**Combined Queries**:
- "login form with blue button"
- "error dialog with red text"
- "dark dashboard with charts"
- "mobile interface with notifications"

## Deployment

### Streamlit Community Cloud

1. **Requirements**:
   - GitHub repository (public or private)
   - Streamlit Cloud account (free)

2. **Deployment Steps**:
   - Push code to GitHub
   - Connect repository to Streamlit Cloud
   - Add secrets in app settings if using API key
   - App deploys automatically

3. **Configuration**:
   - App name: `1-visual-memory-search`
   - Python version: 3.9+
   - Requirements: automatically detected

### Performance Notes

- **Cold start**: ~45 seconds (model loading)
- **Processing**: ~3 seconds per image with Claude API
- **Search**: <1 second for queries
- **Memory**: Optimized for 512MB Streamlit Cloud limit

## How It Works

1. **Image Processing**:
   - Uploads are processed with OCR (pytesseract)
   - Claude 3 Haiku generates visual descriptions
   - Text is combined for comprehensive indexing

2. **Vector Search**:
   - sentence-transformers creates embeddings
   - ChromaDB stores vectors for fast retrieval
   - Semantic similarity matching finds relevant images

3. **Results Ranking**:
   - Cosine similarity determines relevance
   - Confidence scores help evaluate match quality
   - Top-K results returned with metadata

## Sample Screenshots Included

The repository includes 10 diverse sample screenshots:
- Error dialogs and notifications
- Login forms and authentication screens
- Dashboards with dark/light themes
- Code editors with syntax highlighting
- Mobile app interfaces
- Data tables and calendars
- File browsers and settings pages

## Troubleshooting

### Common Issues

1. **"Tesseract not found"**:
   - Install tesseract-ocr system package
   - On macOS: `brew install tesseract`
   - On Ubuntu: `sudo apt-get install tesseract-ocr`

2. **API Rate Limits**:
   - Claude 3 Haiku has generous rate limits
   - Tool includes response caching to minimize API calls
   - Falls back gracefully if API fails

3. **Memory Issues**:
   - Large images are automatically resized
   - ChromaDB uses in-memory storage for simplicity
   - Consider reducing batch sizes for large datasets

4. **Slow Processing**:
   - First run downloads sentence-transformers model (~90MB)
   - Subsequent runs are much faster
   - Processing time scales with image count

### Getting Help

- **Issues**: Report bugs in GitHub Issues
- **Feature Requests**: Use GitHub Discussions
- **API Questions**: Check Anthropic documentation

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- **Anthropic** for Claude 3 Haiku API
- **Streamlit** for the amazing web framework
- **sentence-transformers** for semantic embeddings
- **ChromaDB** for vector database
- **pytesseract** for OCR capabilities

---

**Built for the Buildathon** - A production-ready demo showcasing AI-powered screenshot search.