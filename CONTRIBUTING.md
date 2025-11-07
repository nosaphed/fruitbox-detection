# Contributing to Fruit Detection System

Thank you for considering contributing to this project! 🎉

## How to Contribute

### 1. Fork the Repository
```bash
# Click "Fork" button on GitHub
# Clone your fork
git clone https://github.com/nosaphed/fruit-detection.git
cd fruit-detection
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes
- Write clean, readable code
- Follow existing code style
- Add comments where necessary
- Test your changes

### 4. Commit Changes
```bash
git add .
git commit -m "feat: add new feature"
# or
git commit -m "fix: resolve issue with detection"
```

### Commit Message Format
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 5. Push to GitHub
```bash
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Go to your fork on GitHub
- Click "New Pull Request"
- Describe your changes
- Submit!

## Development Setup

```bash
# Clone repository
git clone https://github.com/nosaphed/fruit-detection.git
cd fruit-detection/src

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python main.py
```

## Code Style

### Python
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused

### Example
```python
def detect_fruits(self, frame):
    """
    Detect fruits in frame using YOLO model
    
    Args:
        frame: Input image frame
        
    Returns:
        Detection results
    """
    results = self.model(frame, conf=self.conf_threshold)
    return results[0]
```

## Areas for Contribution

### 🐛 Bug Fixes
- Fix detection issues
- Resolve training errors
- Improve error handling

### ✨ New Features
- Add new fruit classes
- Implement batch processing
- Add video file support
- Create web interface

### 📚 Documentation
- Improve README
- Add tutorials
- Translate documentation
- Add code examples

### 🧪 Testing
- Add unit tests
- Add integration tests
- Test on different platforms

### 🎨 UI/UX
- Improve detection display
- Add configuration GUI
- Better error messages

## Testing Guidelines

### Before Submitting
1. Test on your local machine
2. Verify no errors in console
3. Check detection accuracy
4. Test with different images

### Test Checklist
- [ ] Code runs without errors
- [ ] Detection works correctly
- [ ] No breaking changes
- [ ] Documentation updated
- [ ] Comments added

## Reporting Issues

### Bug Reports
Include:
- Python version
- OS (Linux/Mac/Windows)
- Error message
- Steps to reproduce
- Expected vs actual behavior

### Feature Requests
Include:
- Clear description
- Use case
- Expected behavior
- Mockups (if applicable)

## Questions?

- Open an issue on GitHub
- Check existing documentation
- Review closed issues

## Code of Conduct

### Be Respectful
- Be kind and courteous
- Respect different viewpoints
- Accept constructive criticism

### Be Collaborative
- Help others
- Share knowledge
- Give credit

### Be Professional
- Stay on topic
- No spam or self-promotion
- Follow GitHub guidelines

## Recognition

Contributors will be:
- Listed in README
- Credited in release notes
- Appreciated by the community! 🙏

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🚀**
