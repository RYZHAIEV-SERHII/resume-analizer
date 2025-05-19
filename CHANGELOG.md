# CHANGELOG

## v0.1.0 (2025-05-19)

### Features

- Add Codecov configuration, GitHub Actions workflows for release and tests
  ([`d0e601c`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/d0e601cb22cfbd34c6c6b67b67703eecc5cb062c))

- Add commit message validation script and pre-commit configuration
  ([`e43895f`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/e43895fdf788b84169cc76da5c439eb65ef28b93))

- Enhance error handling and PDF processing robustness
  ([`50b6c97`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/50b6c970580728d0b28b8db3d5bb38d23bd7faab))

Improves application reliability and user experience through:

- Adds comprehensive error handling for API and configuration issues - Provides fallback analysis
  when AI service is unavailable - Upgrades PDF processing library for better text extraction -
  Improves file content validation with early checks - Restructures analysis flow for better error
  recovery

The changes ensure users receive meaningful feedback even when errors occur, while maintaining core
  functionality through graceful degradation.

Technical improvements: - Upgrades PyPDF2 to PyPDF for better PDF handling - Implements proper file
  pointer management - Adds validation for empty content early in the process - Strengthens API
  client initialization with better error checks

- Enhance UI with custom styling and improved layout
  ([`ffcbb86`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/ffcbb867240e150da469cfee25968d4769c15e39))

Add UI utilities and styling to improve user experience. Updates include custom CSS, better page
  structure, progress indicators, and expanded information sections. Also adds additional badges to
  README for project documentation.

### Refactoring

- Changed code structure for improved readability and maintainability
  ([`94b1fb7`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/94b1fb716170a282345ecdc08a3c7781a718694c))

- Moved styles.css into src/static dir and optimize it.
  ([`887bf50`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/887bf506cfd25ab2c4be6c0186ed2c1952000444))

- Remove unused styles for main container and file uploader
  ([`9abe4a0`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/9abe4a0be3eee11d063a29c57dad3b52a6ea2b8d))

### Testing

- Add comprehensive test suite for resume analysis and UI utilities
  ([`c5337cb`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/c5337cbab7599bf2c79a978e298abd2ad8bca710))

- Streamline test setups and improve mock usage in UI and text extraction tests
  ([`8f1389d`](https://github.com/RYZHAIEV-SERHII/resume-analyzer/commit/8f1389dc3444281cd06a9da9e2471dd2d2243ba9))
