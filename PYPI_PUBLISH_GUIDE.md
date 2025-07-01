# 📦 Publishing UniLLM to PyPI

## Prerequisites

1. **PyPI Account**: Create account at https://pypi.org
2. **TestPyPI Account**: Create account at https://test.pypi.org
3. **Build Tools**: Install build tools

```bash
pip install build twine
```

## Step 1: Prepare Your Package

Your package is already well-structured with:
- ✅ `setup.py` - Package configuration
- ✅ `pyproject.toml` - Modern Python packaging
- ✅ `src/unillm/` - Source code
- ✅ `README.md` - Documentation

## Step 2: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ src/*.egg-info/

# Build the package
python -m build

# This creates:
# - dist/unillm-0.1.0.tar.gz (source distribution)
# - dist/unillm-0.1.0-py3-none-any.whl (wheel distribution)
```

## Step 3: Test on TestPyPI First

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ unillm
```

## Step 4: Publish to PyPI

```bash
# Upload to real PyPI
twine upload dist/*

# Your friend can now install with:
pip install unillm
```

## Step 5: Verify Installation

Your friend can test:

```python
# Test the client library
from unillm import UniLLMClient

client = UniLLMClient(
    api_key="unillm_qLopXrSn3A6VUhHP1Plw2tz2ERMoouY0",
    base_url="https://your-server.railway.app"
)

# Test a simple call
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.response)
```

## Version Management

To update the package:

1. **Update version** in `setup.py` and `pyproject.toml`
2. **Build new package**: `python -m build`
3. **Upload**: `twine upload dist/*`

## Package Configuration

Your current `setup.py` looks good, but you might want to add:

```python
setup(
    name="unillm",
    version="0.1.0",
    description="Unified API gateway for multiple LLM providers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/unillm",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "all": [
            "fastapi>=0.100.0",
            "uvicorn>=0.20.0",
            "sqlalchemy>=2.0.0",
        ]
    }
)
```

## Benefits of PyPI Publishing

✅ **Easy Installation**: `pip install unillm`  
✅ **Version Management**: Automatic updates  
✅ **Professional**: Looks like a real library  
✅ **Discoverable**: Others can find your project  
✅ **Dependencies**: Automatic dependency resolution  

## Next Steps

1. **Deploy your server** (Railway/Render/Heroku)
2. **Publish to PyPI**
3. **Share with friend**: `pip install unillm`
4. **Give them your server URL**
5. **They can start using immediately!**

## Quick Commands Summary

```bash
# Build package
python -m build

# Test on TestPyPI
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*

# Your friend installs
pip install unillm
``` 