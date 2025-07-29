# Changelog

All notable changes to the WNote project will be documented in this file.

## [0.4.0] - 2025-05-23

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

## [0.3.1] - 2023-10-20

### Fixed
- Database lock issue with improved retry mechanism and connection timeout
- JSON serialization error in config command
- Enhanced error handling in configuration loading and saving
- Improved robustness against non-serializable objects in configuration

## [0.3.0]
- Just a test version

## [0.2.0] - 2023-10-15

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

## [0.1.0] - 2023-09-01

### Added
- Initial release
- Basic note taking functionality
- Tag support
- Editor integration
- SQLite database backend 