/**
 * Drawing Analyzer - Main component for engineering drawing analysis
 */
import { useState } from 'react';
import FileUpload from './components/FileUpload';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import './DrawingAnalyzer.css';

function DrawingAnalyzer() {
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = async (selectedFile) => {
    if (!selectedFile) {
      setError('No file selected');
      return;
    }

    // Validate file type (image or PDF)
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf'];
    if (!validTypes.includes(selectedFile.type)) {
      setError('Please select an image (PNG, JPG) or PDF file');
      return;
    }

    setFile(selectedFile);
    setError('');
    setAnalysis(null);
    
    // Auto-analyze immediately after file selection
    await analyzeFile(selectedFile);
  };

  const analyzeFile = async (fileToAnalyze) => {
    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('file', fileToAnalyze);

      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const data = await response.json();
      
      // Check if AI rejected the image as not a drawing
      if (data.error === 'not_a_drawing') {
        throw new Error(data.message || 'This does not appear to be an engineering drawing problem. Please upload a valid drawing.');
      }
      
      setAnalysis(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setAnalysis(null);
    setError('');
  };

  return (
    <div className="drawing-analyzer">
      <header>
        <h1>🎓 Engineering Drawing Mentor</h1>
        <p className="subtitle">Upload your drawing problem, get step-by-step guidance</p>
      </header>

      <main>
        {!analysis && !loading && (
          <div className="upload-section">
            <FileUpload 
              onFileSelect={handleFileChange}
              selectedFile={file}
            />
          </div>
        )}

        {loading && (
          <div className="loading-section">
            <LoadingSpinner />
            <p className="loading-text">AI Tutor is analyzing your drawing...</p>
          </div>
        )}

        {error && (
          <ErrorMessage 
            message={error} 
            onDismiss={() => setError('')}
          />
        )}

        {analysis && !loading && (
          <div className="results-section">
            <div className="results-header">
              <h2>📋 Solution Guide</h2>
              <button className="reset-btn" onClick={handleReset}>
                Try Another
              </button>
            </div>

            {analysis.detected_problem && (
              <div className="problem-badge">
                Problem {analysis.detected_problem}
              </div>
            )}

            <div className="result-card">
              <h3>Problem:</h3>
              <p>{analysis.problem_identification || 'Not specified'}</p>
            </div>

            {analysis.given_information && analysis.given_information.length > 0 && (
              <div className="result-card">
                <h3>Given Information:</h3>
                <ul>
                  {analysis.given_information.map((info, i) => (
                    <li key={i}>{info}</li>
                  ))}
                </ul>
              </div>
            )}

            {analysis.required_output && (
              <div className="result-card">
                <h3>What to Draw:</h3>
                <p>{analysis.required_output}</p>
              </div>
            )}

            {analysis.key_concept && (
              <div className="result-card concept">
                <h3>💡 Key Concept:</h3>
                <p>{analysis.key_concept}</p>
              </div>
            )}

            {analysis.construction_steps && analysis.construction_steps.length > 0 && (
              <div className="result-card steps">
                <h3>🔨 Construction Steps:</h3>
                <div className="steps-list">
                  {analysis.construction_steps.map((step, i) => (
                    <div key={i} className="step-item">
                      <div className="step-number">{step.step || i + 1}</div>
                      <div className="step-content">
                        <strong>{step.instruction}</strong>
                        <p>{step.explanation}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {analysis.common_mistakes && analysis.common_mistakes.length > 0 && (
              <div className="result-card warnings">
                <h3>⚠️ Common Mistakes to Avoid:</h3>
                <ul>
                  {analysis.common_mistakes.map((mistake, i) => (
                    <li key={i}>{mistake}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>

      <footer>
        <p>Powered by Gemini AI · Engineering Drawing Textbook</p>
      </footer>
    </div>
  );
}

export default DrawingAnalyzer;

