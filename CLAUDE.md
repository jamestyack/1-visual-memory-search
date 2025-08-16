# Visual Memory Search - Claude AI Development Notes

This file contains development context and instructions for Claude AI when working on this Visual Memory Search project.

## Project Overview

A production-ready Visual Memory Search tool built for the buildathon that indexes screenshots and enables natural language queries using Claude 3 vision. Users can search for both text content ("error message about auth") and visual elements ("screenshot with blue button") with confidence-scored results.

## Development Context

### Key Technologies
- **Streamlit**: Web framework optimized for Community Cloud deployment
- **Claude 3 Haiku**: Vision API for understanding visual UI elements
- **pytesseract**: OCR text extraction from screenshots
- **sentence-transformers**: Semantic embeddings (all-MiniLM-L6-v2 model)
- **ChromaDB**: In-memory vector database for similarity search

### Critical Architecture Decisions

1. **In-Memory Storage**: ChromaDB configured for ephemeral storage to work within Streamlit Cloud 512MB limits
2. **Lazy Loading**: Models initialized on-demand to avoid PyTorch meta tensor issues
3. **Graceful Degradation**: Falls back to OCR-only mode if Claude API unavailable
4. **Session State Management**: Prevents infinite loops and manages processing state

### Development Standards

#### Code Organization
- `streamlit_app.py`: Main UI with tabbed interface (Upload, Search, Help)
- `processor.py`: Image processing with OCR + Claude vision integration
- `search_engine.py`: Vector search with lazy model loading and error handling
- `architecture.md`: Comprehensive system documentation with mermaid diagrams

#### Key Patterns
- **Error Handling**: Multiple fallback strategies for API failures and model loading
- **State Management**: Session state flags prevent re-processing and infinite loops
- **Performance**: Batch processing, caching, and optimized image handling
- **Security**: Environment-based API key management, no persistent storage

#### Testing Approach
- Sample screenshots included for immediate testing (10 diverse UI mockups)
- Local development with `streamlit run streamlit_app.py`
- Streamlit Community Cloud deployment for production testing

### Recent Fixes & Issues Resolved

1. **Infinite Loading Loop**: Fixed sample screenshots button with proper session state management
2. **PyTorch Meta Tensor Errors**: Resolved with lazy loading and explicit CPU device handling
3. **SQLite Compatibility**: Added pysqlite3-binary for Streamlit Cloud deployment
4. **Button Responsiveness**: Ensured single-click processing with st.rerun() calls

### Deployment Configuration

#### Streamlit Cloud Requirements
- `requirements.txt`: Python dependencies including pysqlite3-binary
- `packages.txt`: System packages (tesseract-ocr, tesseract-ocr-eng)
- `.streamlit/config.toml`: Performance and UI optimizations
- API key via Streamlit secrets: `ANTHROPIC_API_KEY = "your-key"`

#### Local Development
- Environment variable: `ANTHROPIC_API_KEY=your-key`
- Or `.env` file with same variable
- System requirement: tesseract-ocr installed

### Development Guidelines

#### When Making Changes
1. **Test Locally First**: Always run `streamlit run streamlit_app.py` before pushing
2. **Check All Buttons**: Verify upload, folder processing, and sample screenshots work
3. **Test Both Modes**: With and without API key (enhanced vs basic mode)
4. **Verify Session State**: Ensure no infinite loops or duplicate processing

#### Common Development Tasks
- **Adding Features**: Follow existing session state patterns
- **UI Changes**: Maintain responsive grid layouts and error handling
- **Performance**: Consider 512MB memory limit and model loading times
- **Security**: Never commit API keys, use environment variables

#### File Access Patterns
- **Read files first**: Always use Read tool before editing
- **Batch operations**: Use MultiEdit for multiple changes to same file
- **Error handling**: Implement fallbacks for all external dependencies

### Current Status

✅ **Production Ready**: Deployed at https://1-visual-memory-search.streamlit.app
✅ **Bug-Free**: Infinite loading loop fixed, all buttons working
✅ **Well Documented**: README.md and architecture.md complete
✅ **Properly Tested**: Works in both enhanced and basic modes

### Future Enhancement Areas

1. **Persistent Storage**: Database backend for larger deployments
2. **Batch Upload**: Directory processing improvements
3. **Search Filters**: Confidence threshold and result type filtering
4. **Model Options**: Support for different embedding models
5. **Export Features**: Save search results and indexed data

### API Integration Notes

#### Claude 3 Haiku Usage
- **Purpose**: Generate rich visual descriptions of UI elements
- **Fallback**: OCR-only mode if API fails or key missing
- **Rate Limits**: Generous for buildathon usage (~1000 requests/minute)
- **Error Handling**: Graceful degradation with user feedback

#### Tesseract OCR
- **Always Available**: Runs regardless of API key status
- **System Dependency**: Requires tesseract-ocr package installation
- **Performance**: ~1 second per image for text extraction

### Development Environment Setup

```bash
# Clone and setup
git clone https://github.com/jamestyack/1-visual-memory-search.git
cd 1-visual-memory-search

# Install dependencies
pip install -r requirements.txt
brew install tesseract  # macOS

# Set API key (optional)
export ANTHROPIC_API_KEY="your-key"

# Run locally
streamlit run streamlit_app.py
```

### Commit Standards

Follow established pattern with co-authorship:
```
feat: Add new feature description

- Bullet point details
- Include technical specifics
- Mention any breaking changes

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

This project represents a complete, production-ready implementation suitable for buildathon demonstration and real-world usage.