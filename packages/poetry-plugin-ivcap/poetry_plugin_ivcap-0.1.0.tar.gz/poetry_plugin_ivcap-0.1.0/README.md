# poetry-plugin-ivcap

A custom Poetry plugin that adds a `poetry ivcap` command for local and Docker-based deployments.

## Example Configuration

Add to your `pyproject.toml`:

```toml
[tool.poetry-plugin-ivcap]
default_target = "docker"
docker_tag = "myapp:dev"
```

## Installation

```bash
poetry self add poetry-plugin-ivcap
```

## Usage

```bash
poetry ivcap
poetry ivcap docker
```

## Development

### Build the Plugin Package

```bash
poetry build
```

This creates .whl and .tar.gz files in the dist/ directory.

### Publish to PyPI

Create an account at https://pypi.org/account/register/

Add your credentials:
```bash
poetry config pypi-token.pypi <your-token>
```

Publish:
```bash
poetry publish --build
```

### Optional: Test on TestPyPI First

To verify your setup without publishing to the real PyPI:

```bash
poetry config repositories.test-pypi https://test.pypi.org/legacy/
poetry publish -r test-pypi --build
```

Then test installing via:

```bash
poetry self add --source test-pypi poetry-plugin-deploy
```
