# Contributing to Clouds Detangler

Thank you for your interest in contributing to Clouds Detangler! This project helps people manage their cloud storage more effectively.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:

- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, rclone version)
- Any relevant error messages or logs

### Suggesting Features

Feature suggestions are welcome! Please open an issue describing:

- The problem you're trying to solve
- Your proposed solution
- Any alternative approaches you've considered
- How this would benefit other users

### Code Contributions

1. **Fork the repository** and create a branch for your feature
2. **Write tests** if applicable
3. **Follow the existing code style**
4. **Update documentation** if needed
5. **Submit a pull request** with a clear description

### Code Style

- Use Python 3.10+ features
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Keep functions focused and well-named
- Add comments for complex logic

### Testing

Before submitting:

1. Test your changes locally
2. Verify existing functionality still works
3. Test with different cloud providers if applicable

### Documentation

When adding features:

- Update README.md if needed
- Add usage examples
- Update relevant documentation in docs/
- Add comments for complex code

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/clouds-detangler.git
cd clouds-detangler
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a branch:
```bash
git checkout -b feature/my-feature
```

4. Make your changes

5. Test your changes:
```bash
python scripts/validate_setup.py
```

6. Commit and push:
```bash
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

7. Open a pull request on GitHub

## Areas for Contribution

Current areas where help is needed:

- **Deduplication index**: Implement the build_index.py functionality using DuckDB
- **Action planning**: Enhance plan_actions.py to suggest optimal deduplication strategies
- **Execute plan**: Implement execute_plan.py to safely perform rclone moves
- **Testing**: Add unit tests for utility functions
- **Documentation**: Improve setup guides and add video tutorials
- **Platform support**: Test and improve Windows compatibility
- **Cloud providers**: Add support for additional providers (iCloud, Box, etc.)

## Code Review

All contributions will be reviewed for:

- Code quality and style
- Security (no credentials in code!)
- User safety (confirmation before destructive operations)
- Documentation completeness
- Test coverage

## Questions?

Open an issue or reach out to the maintainers. We're happy to help!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
