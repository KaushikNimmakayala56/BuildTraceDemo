/**
 * File upload component
 */
import PropTypes from 'prop-types';
import { FILE_ACCEPT_STRING } from '../constants/config';
import './FileUpload.css';

const FileUpload = ({ onFileSelect, selectedFile, disabled }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileSelect(file);
    }
  };

  return (
    <div className="upload-section">
      <input 
        type="file" 
        accept={FILE_ACCEPT_STRING}
        onChange={handleFileChange}
        id="file-input"
        disabled={disabled}
      />
      <label 
        htmlFor="file-input" 
        className={`upload-button ${disabled ? 'disabled' : ''}`}
      >
        Choose PDF or Image File
      </label>
      {selectedFile && (
        <p className="file-name">
          Selected: {selectedFile.name}
        </p>
      )}
    </div>
  );
};

FileUpload.propTypes = {
  onFileSelect: PropTypes.func.isRequired,
  selectedFile: PropTypes.object,
  disabled: PropTypes.bool
};

FileUpload.defaultProps = {
  selectedFile: null,
  disabled: false
};

export default FileUpload;

