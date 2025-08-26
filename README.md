# SciSynth-AI: Agentic Research Assistant

[![Python Version](https://img.shields.io/badge/python-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-blue.svg)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-green.svg)](https://www.langchain.com/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

SciSynth-AI is an intelligent research assistant that leverages AI agents to search, analyze, and synthesize academic papers from arXiv. It can identify promising research directions, generate new research ideas, and even write complete research papers with mathematical equations in LaTeX format.

##  Features

- **Automated Paper Discovery**: Search and retrieve recent papers from arXiv across multiple scientific domains
- **Intelligent Paper Analysis**: Read and comprehend PDF papers to extract key insights and research directions
- **Research Synthesis**: Generate novel research ideas based on analyzed papers
- **LaTeX Paper Generation**: Create complete research papers with mathematical equations
- **PDF Rendering**: Convert LaTeX documents to professional PDF format using Tectonic
- **Interactive Chat Interface**: Streamlit-based web interface for seamless interaction
- **Conversational AI**: Guided research exploration through natural language conversation

##  Supported Research Domains

- Physics
- Mathematics
- Computer Science
- Quantitative Biology
- Quantitative Finance
- Statistics
- Electrical Engineering and Systems Science
- Economics

##  Prerequisites

### System Requirements

- Python 3.8 or higher
- [Tectonic](https://tectonic-typesetting.github.io/) LaTeX engine
- Google API key for Gemini 2.5 Pro


##  Dependencies

The project uses the following key libraries:

```python
streamlit>=1.28.0
langchain-google-genai>=1.0.0
langgraph>=0.2.0
requests>=2.31.0
PyPDF2>=3.0.0
python-dotenv>=1.0.0
xml-etree-elementtree  # Built-in Python module
```

##  Project Structure

```
SciSynth-AI/
├── arxiv_tool.py           # arXiv API integration and XML parsing
├── read_pdf.py             # PDF text extraction functionality
├── write_pdf.py            # LaTeX to PDF rendering
├── ai_researcher.py        # Basic ReAct agent implementation
├── ai_researcher_2.py      # Advanced LangGraph-based agent
├── frontend.py             # Streamlit web interface
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore file
├── output/                # Generated PDF output directory
└── README.md              # This file
```

##  Usage

### Web Interface (Recommended)

1. **Start the Streamlit application:**
   ```bash
   streamlit run frontend.py
   ```

2. **Open your browser and navigate to:** `http://localhost:8501`

3. **Interact with the AI agent:**
   - Describe your research interests
   - Review suggested papers
   - Select papers for detailed analysis
   - Generate new research ideas
   - Request paper writing and PDF generation


##  Workflow Example

1. **Topic Selection**: User specifies research area of interest
2. **Paper Discovery**: Agent searches arXiv for recent relevant papers
3. **Paper Presentation**: Agent summarizes found papers with metadata
4. **Paper Analysis**: User selects paper for detailed analysis
5. **Content Extraction**: Agent reads and analyzes the selected PDF
6. **Idea Generation**: Agent identifies research gaps and proposes new directions
7. **Paper Writing**: Agent creates a complete research paper in LaTeX
8. **PDF Generation**: System renders the LaTeX to a professional PDF


##  Error Handling

The system includes comprehensive error handling for:

- **Invalid arXiv queries**: Character validation and sanitization
- **PDF reading failures**: Network issues and malformed PDFs
- **LaTeX compilation errors**: Tectonic compilation issues
- **API failures**: Google AI API rate limits and errors
- **File system errors**: Permission and disk space issues

##  Performance Considerations

- **Concurrent Processing**: Streamlit interface supports real-time streaming
- **Memory Management**: State management with LangGraph checkpoints
- **API Rate Limits**: Built-in handling for arXiv and Google AI APIs
- **PDF Processing**: Optimized for large academic papers





**SciSynth-AI**: Accelerating scientific discovery through intelligent research synthesis.