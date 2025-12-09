# Contributing to Facebook Job Crawler

Thank you for your interest in contributing to the Facebook Job Crawler project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists in the GitHub issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (if it's a bug)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Submitting Changes

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit with clear, descriptive messages
6. Push to your fork
7. Submit a pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Include type hints where appropriate
- Keep functions focused and single-purpose

### Testing

Before submitting a pull request:

1. Test your changes manually
2. Ensure all imports work correctly
3. Verify the crawler functionality
4. Test data export features

### Areas for Contribution

We welcome contributions in these areas:

1. **Improved Selectors**: Update HTML selectors to match Facebook's current structure
2. **Additional Features**: 
   - Support for more job search filters
   - Job deduplication
   - Database storage options
   - API integration
3. **Error Handling**: Enhanced error recovery and logging
4. **Documentation**: Improvements to README, code comments, or examples
5. **Performance**: Optimization of crawling speed and efficiency
6. **Testing**: Unit tests and integration tests

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/JobCrawling-.git
cd JobCrawling-

# Install dependencies
pip install -r requirements.txt

# Make your changes and test
python main.py --help
python example_usage.py
```

### Commit Messages

Use clear and descriptive commit messages:

- Start with a verb (Add, Fix, Update, Remove, etc.)
- Be concise but descriptive
- Reference issue numbers when applicable

Examples:
- `Add support for remote job filtering`
- `Fix CSV export encoding issue`
- `Update README with new examples`

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the project
- Show empathy towards others

## Questions?

Feel free to open an issue for questions or discussions about contributing.

Thank you for contributing! 🎉
