/**
 * Error message component
 */
import PropTypes from 'prop-types';
import './ErrorMessage.css';

const ErrorMessage = ({ message, onDismiss }) => {
  if (!message) return null;

  return (
    <div className="error-container">
      <div className="error-content">
        <span className="error-icon">⚠️</span>
        <span className="error-text">{message}</span>
        {onDismiss && (
          <button onClick={onDismiss} className="error-dismiss">
            ✕
          </button>
        )}
      </div>
    </div>
  );
};

ErrorMessage.propTypes = {
  message: PropTypes.string,
  onDismiss: PropTypes.func
};

ErrorMessage.defaultProps = {
  message: '',
  onDismiss: null
};

export default ErrorMessage;

