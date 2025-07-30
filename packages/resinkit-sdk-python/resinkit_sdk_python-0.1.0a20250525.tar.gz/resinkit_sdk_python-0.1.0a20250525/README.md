# ResinKit Python SDK

A Python SDK for ResinKit.

## Requirements

- Python 3.9+
- uv for dependency management

## Installation

You can install the package using uv:

```bash
uv add resinkit-sdk-python
```

Or directly with pip:

```bash
pip install resinkit-sdk-python
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resinkit-sdk-python.git
cd resinkit-sdk-python
```

2. Install uv (if not already installed):
```bash
curl -sSL https://install.python-uv.org | python3 -
```

3. Install dependencies:
```bash
uv install
```

4. Run tests:
```bash
uv run pytest
```

## Usage

```python
from resinkit import Client

# Initialize the client
client = Client()

# Use the client
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
