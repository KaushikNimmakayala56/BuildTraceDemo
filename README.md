# 🎓 Engineering Drawing Mentor AI

An intelligent educational tool that helps students learn engineering drawing by providing step-by-step guidance on solving problems from N.D. Bhatt's Engineering Drawing textbook (Chapter 12: Projections of Planes).

## 🌟 Features

- **Smart Problem Recognition**: Upload a drawing problem image, and the AI automatically identifies which problem it is
- **Targeted Context Retrieval**: Uses only relevant textbook sections (85% token reduction vs. full PDF)
- **Step-by-Step Guidance**: Provides 4-6 clear construction steps with explanations
- **Educational Focus**: Explains concepts, warns about common mistakes, and references textbook content
- **Modern UI**: Clean, responsive interface with real-time analysis

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **PDF Service**: Parses 12-page textbook into individual problem sections at startup
- **Gemini Service**: Two-step AI analysis
  1. Extract problem number from uploaded image
  2. Retrieve specific problem section and analyze with Gemini 2.0 Flash
- **Smart Context Strategy**: Sends only 500-800 tokens (specific section) vs. 7,500 tokens (full PDF)

### Frontend (React + Vite)
- Drag-and-drop file upload
- Auto-analysis on file selection
- Structured result display with color-coded sections
- Fully responsive design

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Google Gemini API key

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "GEMINI_MODEL=gemini-2.0-flash-exp" >> .env

# Run server
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on `http://localhost:5173`

## 📁 Project Structure

```
pdf-reader/
├── backend/
│   ├── main.py              # FastAPI app & endpoints
│   ├── pdf_service.py       # PDF parsing & section retrieval
│   ├── gemini_service.py    # AI analysis logic
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # API keys (not in git)
├── frontend/
│   ├── src/
│   │   ├── DrawingAnalyzer.jsx    # Main component
│   │   ├── DrawingAnalyzer.css    # Styles
│   │   └── components/            # Reusable components
│   ├── package.json
│   └── vite.config.js       # Proxy configuration
├── TEXTBOOK.pdf             # N.D. Bhatt Chapter 12
└── README.md
```

## 🔧 API Endpoints

### `GET /api/health`
Health check - returns textbook loading status and available problems

### `POST /api/analyze`
Analyze uploaded drawing problem
- **Input**: Image file (PNG, JPG) or PDF
- **Output**: JSON with problem identification, steps, and guidance

## 🎯 How It Works

1. **Student uploads** incomplete drawing problem (e.g., Problem 12-12)
2. **Backend receives** image and asks Gemini: "What problem number is this?"
3. **Gemini responds** with problem number (e.g., "12-12")
4. **Backend retrieves** only Problem 12-12 section from pre-parsed PDF
5. **Backend sends** image + targeted section to Gemini for analysis
6. **Gemini returns** structured JSON with 4-6 construction steps
7. **Frontend displays** results in clean, educational format

## 💡 Key Innovation: Smart Context Retrieval

Instead of sending the entire 12-page PDF (≈7,500 tokens) with every request:
- Parse PDF into problem sections at startup
- Extract problem number from image (quick Gemini call)
- Send only relevant section (≈500-800 tokens)
- **Result**: 85% token reduction, faster responses, lower costs

## 🛠️ Technologies

**Backend:**
- FastAPI - Modern Python web framework
- Google Gemini 2.0 Flash - Multimodal AI
- PyPDF2 - PDF text extraction
- Pydantic - Data validation

**Frontend:**
- React 18 - UI library
- Vite - Fast build tool
- Custom CSS - Clean, modern styling

## 📝 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

**⚠️ Never commit your `.env` file to git!**

## 🎨 Demo

Upload any problem from N.D. Bhatt Chapter 12 (Problems 12-1, 12-2, 12-3, 12-5, 12-7, 12-9, 12-10, 12-11, 12-12) and get instant step-by-step guidance!

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

Built by Kaushik Nimmakayala for BuildTrace founding engineer interview.

## 🙏 Acknowledgments

- N.D. Bhatt's Engineering Drawing textbook
- Google Gemini AI
- BuildTrace for the opportunity

