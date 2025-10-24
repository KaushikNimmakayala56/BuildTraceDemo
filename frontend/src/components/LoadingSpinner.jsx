/**
 * Loading spinner component
 */
import PropTypes from 'prop-types';
import './LoadingSpinner.css';

const LoadingSpinner = ({ message }) => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p className="loading-message">{message}</p>
    </div>
  );
};

LoadingSpinner.propTypes = {
  message: PropTypes.string
};

LoadingSpinner.defaultProps = {
  message: 'Processing...'
};

export default LoadingSpinner;

