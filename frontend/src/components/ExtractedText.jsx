/**
 * Component to display extracted text
 */
import PropTypes from 'prop-types';
import './ExtractedText.css';

const ExtractedText = ({ text, filename }) => {
  if (!text) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    alert('Text copied to clipboard!');
  };

  return (
    <div className="result-section">
      <div className="result-header">
        <h2>Extracted Text:</h2>
        <button onClick={handleCopy} className="copy-button">
          📋 Copy Text
        </button>
      </div>
      {filename && (
        <p className="result-filename">From: {filename}</p>
      )}
      <div className="text-display">
        {text}
      </div>
    </div>
  );
};

ExtractedText.propTypes = {
  text: PropTypes.string,
  filename: PropTypes.string
};

ExtractedText.defaultProps = {
  text: '',
  filename: ''
};

export default ExtractedText;

