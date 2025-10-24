/**
 * Application configuration constants
 */

// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

// File Upload Configuration
export const ALLOWED_FILE_TYPES = {
  PDF: 'application/pdf',
  IMAGE: 'image/*'
};

export const FILE_ACCEPT_STRING = '.pdf,image/*';

export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// UI Messages
export const MESSAGES = {
  INVALID_FILE_TYPE: 'Please select a valid PDF or image file',
  PROCESSING: 'Processing file...',
  UPLOAD_SUCCESS: 'File processed successfully',
  UPLOAD_ERROR: 'Failed to process file',
  NO_FILE_SELECTED: 'No file selected'
};

