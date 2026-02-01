# Contributor Guide

## Installation

If you are planning to contribute to this project, please make sure to install it under developer mode. Clone the repo, create and activate an environment and run

```bash
pip install -e ".[dev]"
```

The "-e" flag will install the package in editable mode, which means you can edit the source code without having to re-install. The ".[dev]" will install the package in the repo, and the extra dependencies needed for development.

## Things to do before pushing to GitHub

### Using pre-commit hooks for code formatting and linting

When you install in developer mode with `".[dev]` you will install the [pre-commit](https://pre-commit.com/) package. To set up this package simply run

```bash
pre-commit install
```

Then, everytime before doing a commit (that is before `git add` and `git commit`) run the following command:

```bash
pre-commit run --all-files
```

Once you have fixed everything, you will be able to run `git add` and `git commit` without issue.


### Make sure tests run

```bash
python -m pytest tests/
```

## Best practices for contributing

* Fork the repository and perform changes in your fork.
* After your fork is updated, you can open a [Pull Request](https://github.com/Xplosion-Team/greensdigitalsimulator/pulls).

## Documentation Contributions

We highly value documentation improvements! When contributing documentation:

### Documentation Standards

* **Clarity**: Write clear, concise explanations
* **Examples**: Include code examples where relevant
* **Formatting**: Use proper Markdown formatting
* **Links**: Cross-reference related documentation
* **Accuracy**: Verify all technical details

### Documentation Structure

Our documentation follows this organization:

* **README.md** - Main overview and quick start
* **QUICKSTART.md** - 5-minute getting started guide
* **API.md** - Complete API reference
* **ARCHITECTURE.md** - Technical architecture details
* **EXAMPLES.md** - Step-by-step tutorials
* **TROUBLESHOOTING.md** - Common issues and solutions
* **FAQ.md** - Frequently asked questions

### How to Contribute Documentation

1. **Identify the gap**: What's missing or unclear?
2. **Choose the right file**: Where should this content go?
3. **Follow the style**: Match existing formatting and tone
4. **Add examples**: Show, don't just tell
5. **Test your changes**: Verify links work, code runs
6. **Submit PR**: Clearly describe what you've improved

### Documentation Checklist

Before submitting documentation changes:

- [ ] Spell-check and grammar-check
- [ ] Code examples are tested and work
- [ ] Links are valid and point to correct locations
- [ ] Formatting is consistent with existing docs
- [ ] Changes are in the appropriate file(s)
- [ ] Table of contents updated if needed

## Code Contributions

When contributing code:

* Write clean, readable code
* Add docstrings to functions and classes
* Include type hints where appropriate
* Write unit tests for new features
* Ensure existing tests still pass
* Update documentation to reflect changes

## Community Guidelines

* Be respectful and constructive
* Welcome newcomers
* Help others learn
* Share knowledge
* Give credit where due
