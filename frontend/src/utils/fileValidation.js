/**
 * File validation utilities
 */
import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE } from '../constants/config';

/**
 * Validate if file type is supported
 * @param {File} file - File to validate
 * @returns {boolean} True if file type is valid
 */
export const isValidFileType = (file) => {
  if (!file) return false;
  
  return (
    file.type === ALLOWED_FILE_TYPES.PDF ||
    file.type.startsWith('image/')
  );
};

/**
 * Validate file size
 * @param {File} file - File to validate
 * @returns {boolean} True if file size is within limit
 */
export const isValidFileSize = (file) => {
  if (!file) return false;
  return file.size <= MAX_FILE_SIZE;
};

/**
 * Get human-readable file size
 * @param {number} bytes - File size in bytes
 * @returns {string} Formatted file size
 */
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

