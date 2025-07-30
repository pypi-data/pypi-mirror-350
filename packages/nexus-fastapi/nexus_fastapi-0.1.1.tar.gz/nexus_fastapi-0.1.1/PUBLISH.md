# Publishing to PyPI

This guide outlines the steps to publish updates to the Nexus-FastAPI package on PyPI.

## Prerequisites

1. PyPI Account

   - Create an account on [PyPI](https://pypi.org/account/register/) if you haven't already
   - Enable two-factor authentication for security

2. Required Tools
   ```bash
   pip install --upgrade build twine
   ```

## Publishing Steps

### 1. Update Version

1. Update version in `pyproject.toml`:

   ```toml
   [project]
   version = "0.1.1"  # Increment version number
   ```

2. Update version in `setup.py`:
   ```python
   setup(
       name="nexus-fastapi",
       version="0.1.1",  # Increment version number
       ...
   )
   ```

### 2. Clean Build Artifacts

```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 3. Build Distribution

```bash
# Build the package
python -m build
```

### 4. Check Distribution

```bash
# Verify the distribution
twine check dist/*
```

### 5. Upload to TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ nexus-fastapi
```

### 6. Upload to PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

### 7. Verify Installation

```bash
# Install the package
pip install nexus-fastapi

# Verify installation
python -c "import nexus_fastapi; print(nexus_fastapi.__version__)"
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality
- PATCH version for backwards-compatible bug fixes

Example: `1.2.3`

- 1: Major version
- 2: Minor version
- 3: Patch version

## Troubleshooting

### Common Issues

1. **Authentication Failed**

   - Ensure you're using the correct PyPI credentials
   - If using 2FA, use an API token instead of password

2. **Version Already Exists**

   - PyPI doesn't allow overwriting existing versions
   - Increment the version number and try again

3. **Build Errors**
   - Check for syntax errors in your code
   - Ensure all dependencies are properly listed in `pyproject.toml`

### Creating a PyPI API Token

1. Go to your PyPI account settings
2. Navigate to "API tokens"
3. Click "Add API token"
4. Give it a name (e.g., "Nexus-FastAPI Upload")
5. Select the scope (entire account or specific project)
6. Copy the token and store it securely

Use the token with twine:

```bash
twine upload -u __token__ -p YOUR_API_TOKEN dist/*
```

## Best Practices

1. **Always Test First**

   - Test locally before publishing
   - Use TestPyPI for pre-release testing

2. **Keep Changelog**

   - Document changes in `CHANGELOG.md`
   - Update documentation for new features

3. **Tag Releases**

   ```bash
   git tag -a v0.1.1 -m "Version 0.1.1"
   git push origin v0.1.1
   ```

4. **Update Documentation**
   - Update README.md if needed
   - Update any relevant documentation

## Automated Publishing (Optional)

Consider setting up GitHub Actions for automated publishing:

1. Create `.github/workflows/publish.yml`
2. Add PyPI token to GitHub Secrets
3. Configure the workflow to run on release tags

Example workflow:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          python -m build
          twine upload dist/*
```

## Need Help?

- [PyPI Documentation](https://packaging.python.org/guides/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/tutorials/packaging-projects/)
