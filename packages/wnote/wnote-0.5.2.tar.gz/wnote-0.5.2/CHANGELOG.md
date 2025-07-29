# Changelog

All notable changes to the WNote project will be documented in this file.

## [0.5.2] - 2025-05-24

### Fixed
- **Critical**: Fixed attachment inheritance bug where new notes with reused IDs would inherit attachments from deleted notes
- **Critical**: Fixed timezone issue - all timestamps now use local system time instead of UTC
- Enabled SQLite foreign key constraints to ensure proper cascade deletion
- Improved attachment deletion to explicitly remove records from database before deleting note
- Enhanced datetime parsing to support both standard and ISO formats for backward compatibility
- Added better error handling for attachment file deletion from disk

### Changed
- All datetime operations now use local system timezone
- Database connections now enforce foreign key constraints
- Improved robustness of attachment management system

## [0.5.1] - 2024-03-19

### Changed
- Updated README with bilingual support (English and Vietnamese)
- Improved documentation with development setup instructions
- Removed unnecessary files (PYPI_UPLOAD_GUIDE.md, build_and_test.sh, install.sh)
- Synchronized setup.py with pyproject.toml
- Added development dependencies configuration

## [0.5.0] - 2024-03-19

### Added
- Reminders functionality: Add, view, complete, and delete reminders for notes
- Deattach command: Remove attachments from notes with detailed management options
- Comprehensive stats command: Display detailed statistics about notes, tags, attachments, and reminders
- Enhanced README: Removed unimplemented features and updated documentation

### Fixed
- Updated README to match actual implemented features
- Improved documentation with accurate feature descriptions

## [0.4.0] - 2024-03-19

### Added
- Search functionality to find notes by content or title
- Export feature to export notes in text, markdown, or HTML formats
- Ability to delete tags with `delete --tag` command
- Reuse of note IDs after deletion for better ID management
- Improved help text for all commands with detailed examples

### Fixed
- Fixed attach command to better handle files from different drives
- Enhanced file path handling with expansion of relative paths
- Better error handling for attachments and file operations
- Fixed ID allocation to reuse deleted note IDs

## [0.3.1] - 2024-03-19

### Fixed
- Database lock issue with improved retry mechanism and connection timeout
- JSON serialization error in config command
- Enhanced error handling in configuration loading and saving
- Improved robustness against non-serializable objects in configuration

## [0.3.0] - 2024-03-19

### Added
- Support for file and directory attachments
- Attachment preview and opening
- Custom tag colors
- Color configuration system
- Note filtering by tags
- Enhanced UI with Rich library

### Changed
- Improved database schema for attachments
- Better error handling
- Updated documentation

## [0.2.0] - 2024-03-19

### Added
- Basic note taking functionality
- Tag support
- Editor integration
- SQLite database backend 