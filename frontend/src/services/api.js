/**
 * API service for handling backend communication
 */
import { API_BASE_URL } from '../constants/config';

/**
 * Upload file to backend for text extraction
 * @param {File} file - File to upload
 * @returns {Promise<Object>} Response containing extracted text
 */
export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to process file');
  }

  return response.json();
};

/**
 * Check API health status
 * @returns {Promise<Object>} Health status
 */
export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error('API health check failed');
  }
  
  return response.json();
};

