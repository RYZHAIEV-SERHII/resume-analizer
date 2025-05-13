# 📃 AI Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red?style=flat-square&logo=streamlit)
![Google](https://img.shields.io/badge/Google-Gemini--2.0--Flash-green?style=flat-square&logo=google)

An innovative AI-powered tool crafted to evaluate resumes and provide tailored, actionable insights, empowering job seekers to refine their applications.

## ✨ Features

- **Smart Document Processing**: Upload resumes in PDF, DOCX, or TXT format
- **Job-Specific Analysis**: Customize feedback for specific job roles and industries
- **Comprehensive Feedback**: Get detailed AI analysis on:
  - Content clarity and impact
  - Skills presentation and relevance
  - Experience descriptions and achievements
  - ATS (Applicant Tracking System) optimization
  - Targeted improvements for specific roles
- **Clean, Modern UI**: User-friendly interface built with Streamlit
- **Privacy-Focused**: Your resume data is not stored or shared

## 🖼️ Screenshot

![AI Resume Analyzer Screenshot](https://via.placeholder.com/800x450.png?text=AI+Resume+Analyzer+Screenshot)

## 🚀 Installation

### Prerequisites

- Python 3.13+
- OpenRouter API key

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/RYZHAIEV-SERHII/resume-analyzer.git
   cd resume-analyzer
   ```

2. Install uv if not installed:

   ```bash
   pip install uv
   ```

3. Install dependencies and setup virtual environment using UV:

   ```bash
   uv sync
   ```

4. Create a `.env` file with your OpenRouter API key:

   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

## 💻 Usage

Run the application:

```bash
uv run streamlit run main.py
```

Then open your browser at <http://localhost:8501>

## 🏗️ Project Structure

```plaintext
resume-analyzer/
├── main.py                 # Entry point for the application
├── src/                    # Source code
│   ├── utils/              # Utility functions
│   │   └── text_extractor.py  # Text extraction from different file formats
│   └── services/           # Core services
│       └── ai_analyzer.py  # AI analysis functionality
├── .env                    # Environment variables (not in repo)
├── .python-version         # Python version file
├── pyproject.toml          # Project dependencies
├── uv.lock                 # UV lock file
└── README.md               # Project documentation
```

## 🛠️ Technologies Used

- **Streamlit**: For the web interface
- **Google Gemini 2.0 Flash**: For AI-powered resume analysis (via OpenRouter)
- **OpenRouter**: For accessing various AI models
- **PyPDF2**: For PDF text extraction
- **python-docx**: For DOCX file processing
- **UV**: For dependency management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or suggestions,
feel free to reach out to me at [Email](mailto:rsp89@gmail.com) or [Telegram](https://t.me/CTAJIKEP)

### Happy coding!
