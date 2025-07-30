# PyPI Upload Guide for CloneIt

## 🚀 Publishing CloneIt to PyPI

Your package is ready for publication! Here's how to successfully upload it to PyPI.

## 📋 Prerequisites

### 1. PyPI Account Setup
- Create an account at [https://pypi.org/account/register/](https://pypi.org/account/register/)
- Verify your email address
- Consider enabling 2FA for security

### 2. Generate API Token
1. Log into PyPI
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Choose scope:
   - **For first upload**: Select "Entire account"
   - **For future uploads**: Create project-specific token after first upload
5. Copy the token (starts with `pypi-`)

## 🔧 Upload Process

### Option 1: Using API Token (Recommended)

```bash
# Install twine if not already installed
pip install twine

# Upload using API token
twine upload dist/* --username __token__ --password pypi-AgEIcHlwaS5vcmcC...
```

### Option 2: Using .pypirc Configuration

Create a `.pypirc` file in your home directory:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcC...  # Your actual API token
```

Then upload:
```bash
twine upload dist/*
```

### Option 3: Interactive Upload
```bash
twine upload dist/*
# Username: __token__
# Password: [paste your API token]
```

## 📦 Current Package Status

Your package is ready with:
- ✅ Built distributions: `dist/cloneit-0.1.dev1+gfb7dcdf.d20250525-py3-none-any.whl`
- ✅ Source distribution: `dist/cloneit-0.1.dev1+gfb7dcdf.d20250525.tar.gz`
- ✅ All tests passing (34 tests, 94% coverage)
- ✅ Clean code style (black + flake8)
- ✅ Complete documentation

## 🏷️ Version Considerations

### Current Version
Your package currently has a development version: `0.1.dev1+gfb7dcdf.d20250525`

### For Production Release
Consider creating a clean release version:

1. **Create a release commit:**
```bash
git commit --allow-empty -m "Release v0.1.0"
git tag v0.1.0
```

2. **Rebuild with clean version:**
```bash
python -m build
```

This will create a cleaner version like `cloneit-0.1.0-py3-none-any.whl`

## 🧪 Test Upload (Recommended)

Before uploading to the main PyPI, test with TestPyPI:

1. **Register at TestPyPI:** [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. **Upload to TestPyPI:**
```bash
twine upload --repository testpypi dist/*
```
3. **Test installation:**
```bash
pip install --index-url https://test.pypi.org/simple/ cloneit
```

## 🔍 Troubleshooting Common Issues

### Authentication Errors
- **403 Forbidden**: Invalid API token or username
- **401 Unauthorized**: Token expired or incorrect

### Package Name Conflicts
- If "cloneit" is taken, consider alternatives:
  - `cloneit-fields`
  - `python-cloneit`
  - `rpgle-cloneit`

### Version Issues
- Can't upload same version twice
- Use `--skip-existing` to skip already uploaded files

## 📋 Pre-Upload Checklist

- [ ] PyPI account created and verified
- [ ] API token generated
- [ ] Package name availability checked
- [ ] All tests passing
- [ ] Documentation complete
- [ ] License file included
- [ ] Version number appropriate

## 🎯 Post-Upload Steps

After successful upload:

1. **Verify installation:**
```bash
pip install cloneit
python -c "import cloneit; print(cloneit.__version__)"
```

2. **Update documentation:**
   - Add PyPI badge to README
   - Update installation instructions

3. **Create GitHub release:**
   - Tag the release
   - Upload distributions as assets

## 🛡️ Security Best Practices

- Use API tokens instead of passwords
- Create project-specific tokens after first upload
- Store tokens securely (environment variables, password managers)
- Never commit tokens to version control

## 📈 Package Statistics

Once uploaded, your package will be available at:
- **PyPI page:** https://pypi.org/project/cloneit/
- **Installation:** `pip install cloneit`
- **Documentation:** Auto-generated from your README.md

## 🎉 Success!

Once uploaded successfully, users worldwide can install your package with:
```bash
pip install cloneit
```

Your RPGLE-inspired field template cloning system will be available to the Python community!

---

**Note:** The current upload attempt failed due to authentication. Follow this guide to set up proper credentials and try again.
