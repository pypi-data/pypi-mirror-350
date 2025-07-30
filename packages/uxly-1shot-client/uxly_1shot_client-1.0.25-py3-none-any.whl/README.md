# 1Shot API Python Client

A Python client for the 1Shot API that provides both synchronous and asynchronous interfaces.

## Installation

```bash
pip install uxly-1shot-client
```

## Development

### Setting Up the Development Environment

There are two ways to set up your development environment:

#### Option 1: Using Hatch (Recommended)

[Hatch](https://hatch.pypa.io/) is a modern Python project manager that handles environments, dependencies, and builds.

1. Install Hatch:
```bash
pip install hatch
```

2. Create and enter the development environment:
```bash
# This creates a virtual environment and installs all dependencies
python -m hatch shell
```

The `hatch shell` command:
- Creates an isolated environment
- Installs all development dependencies
- Activates the environment
- Sets up the project in editable mode

**Important Note**: The Hatch shell is for development work only. When you need to build the package, you should exit the Hatch shell first:
```bash
# Exit the Hatch shell
exit

# Build the package from outside the Hatch shell
hatch build
```

#### Option 2: Using venv

If you prefer using Python's built-in virtual environment:

1. Create and activate a virtual environment:
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix-like systems (Linux/macOS):
source .venv/bin/activate
```

2. Install development dependencies:
```bash
# Install the package in editable mode with development dependencies
pip install -e ".[dev]"
```

### Key Differences

- **Hatch Shell**:
  - Manages the entire project lifecycle
  - Automatically handles dependency installation
  - Provides consistent environments across team members
  - Environment is project-specific and managed by Hatch
  - Use for development, testing, and running code
  - Exit the shell before running `hatch build`

- **venv**:
  - Python's built-in virtual environment tool
  - More manual control over the environment
  - Requires explicit dependency installation
  - Environment is managed by you
  - More familiar to Python developers

### Development Workflow

1. Start development:
```bash
# Enter the Hatch shell for development
python -m hatch shell
```

2. Make your changes and run tests:
```bash
# Run tests
pytest

# Run linters
ruff check .
```

3. Build the package:
```bash
# First exit the Hatch shell
exit

# Then build the package
hatch build
```

4. If you need to make more changes, repeat from step 1.

### IDE Configuration

If your IDE shows import errors (like "Import could not be resolved") even after installing dependencies, you may need to configure your IDE to use the correct Python interpreter:

#### VS Code
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS)
2. Type "Python: Select Interpreter"
3. Choose the interpreter from your Hatch environment (it should be something like `hatch/virtual/default/Scripts/python.exe` on Windows or `hatch/virtual/default/bin/python` on Unix-like systems)

#### PyCharm
1. Go to `File > Settings > Project > Python Interpreter` (Windows/Linux) or `PyCharm > Preferences > Project > Python Interpreter` (macOS)
2. Click the gear icon and select "Add"
3. Choose "Existing Environment" and select the Python interpreter from your Hatch environment at `hatch/virtual/default/Scripts/python.exe` (Windows) or `hatch/virtual/default/bin/python` (Unix-like systems)

#### General Tips
- Make sure your IDE's Python extension is installed and up to date
- Try reloading your IDE window after selecting the correct interpreter
- If using VS Code, you might need to install the Pylance extension for better Python support

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=uxly_1shot_client
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

You can run these tools manually:
```bash
# Format code
black src tests

# Sort imports
isort src tests

# Run linter
flake8 src tests

# Check types
mypy src tests
```

Or use pre-commit to run them automatically on commit:
```bash
pre-commit run --all-files
```

## Usage

### Synchronous Client

```python
import os

# its handy to set your API key and secret with environment variables
API_KEY = os.getenv("ONESHOT_API_KEY")
API_SECRET = os.getenv("ONESHOT_API_SECRET")
BUSINESS_ID = os.getenv("ONESHOT_BUSINESS_ID") 

from uxly_1shot_client import Client

# Initialize the client
client = Client(
    api_key=API_KEY,
    api_secret=API_SECRET,
    base_url="https://api.1shotapi.com/v0"  # Optional, defaults to this URL
)

# List transactions for a business
transactions = client.transactions.list(
    business_id=BUSINESS_ID,
    params={"page": 1, "page_size": 10}
)

# Get transaction endpoint details
transaction_endpoint = client.transactions.get(transactions.response[0].id)

# Execute a transaction
execution = client.transactions.execute(
    transaction_id=transaction_endpoint.id,
    params={
        "amount": "1000000000000000000",  # 1 ETH in wei
        "recipient": "0x123..."
    }
)

executions_list = client.executions.list(business_id=BUSINESS_ID)

execution_status = client.executions.get(execution.id)

wallet = client.wallets.get(escrow_wallet_id="54ee551b-5586-48c9-a7ee-72d74ed889c0", include_balances=True)

wallets = client.wallets.list(BUSINESS_ID)

mint_endpoint_payload = {
        "chain": 11155111,
        "contractAddress": "0xA1BfEd6c6F1C3A516590edDAc7A8e359C2189A61",
        "escrowWalletId": f"{wallet.id}",
        "name": "Sepolia Token Deployer",
        "description": "This deploys ERC20 tokens on Sepolia",
        "functionName": "deployToken",
        "callbackUrl": "https://rapid-clam-infinitely.ngrok-free.app/1shot",
        "stateMutability": "nonpayable",
        "inputs": [
            {
                "name": "admin",
                "type": "address",
                "index": 0,
            },
            {
                "name": "name",
                "type": "string",
                "index": 1
            },
            {
                "name": "ticker",
                "type": "string",
                "index": 2
            },
            {
                "name": "premint",
                "type": "uint",
                "index": 3
            }
        ],
        "outputs": []
    }

# Create a new transaction
new_transaction = client.transactions.create(
    business_id=BUSINESS_ID,
    params=mint_endpoint_payload
)
```

### Asynchronous Client

```python
import os

# its handy to set your API key and secret with environment variables
API_KEY = os.getenv("ONESHOT_API_KEY")
API_SECRET = os.getenv("ONESHOT_API_SECRET")
BUSINESS_ID = os.getenv("ONESHOT_BUSINESS_ID") 

import asyncio
from uxly_1shot_client import AsyncClient

async def main():
    # Initialize the client
    client = AsyncClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        base_url="https://api.1shotapi.com/v0"  # Optional, defaults to this URL
    )
    # List transactions for a business
    transactions = await client.transactions.list(
        business_id=BUSINESS_ID,
        params={"page": 1, "page_size": 10}
    )
    # Execute a transaction
    execution = await client.transactions.execute(
        transaction_id="424f56a9-cc15-4b5c-9bab-5fc5c9569869",
        params={
            "account": "0xE936e8FAf4A5655469182A49a505055B71C17604"
        }
    )
    
    # Get available transaction endpoints attached to your organization
    transaction = await client.executions.list(BUSINESS_ID)
    for transaction in transactions.response:
        print(f"Transaction ID: {transaction.id}, Status: {transaction.name}")

    # Get available wallets attached to your organization
    wallets = await client.wallets.list(BUSINESS_ID)
    for wallet in wallets.response:
        print(f"Wallet ID: {wallet.id}, Address: {wallet.account_address}")

# Run the async code
asyncio.run(main())
```

### Webhook Verification

#### Using the Standalone Function

```python
from uxly_1shot_client import verify_webhook
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Get the webhook body and signature
    body = await request.json()
    signature = body.pop("signature", None)
    
    if not signature:
        raise HTTPException(status_code=400, detail="Signature missing")
    
    # Your webhook public key
    public_key = "your_webhook_public_key"
    
    try:
        # Verify the webhook signature
        is_valid = verify_webhook(
            body=body,
            signature=signature,
            public_key=public_key
        )
        
        if not is_valid:
            raise HTTPException(status_code=403, detail="Invalid signature")
            
        return {"message": "Webhook verified successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
```

#### Using the WebhookVerifier Class

```python
from uxly_1shot_client import WebhookVerifier
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Create a verifier instance with your public key
verifier = WebhookVerifier(public_key="your_webhook_public_key")

@app.post("/webhook")
async def handle_webhook(request: Request):
    # Get the webhook body and signature
    body = await request.json()
    signature = body.pop("signature", None)
    
    if not signature:
        raise HTTPException(status_code=400, detail="Signature missing")
    
    try:
        # Verify the webhook signature
        is_valid = verifier.verify(
            body=body,
            signature=signature
        )
        
        if not is_valid:
            raise HTTPException(status_code=403, detail="Invalid signature")
            
        return {"message": "Webhook verified successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
```

## Error Handling

The client raises exceptions for various error conditions:

- `requests.exceptions.RequestException` for synchronous client errors
- `httpx.HTTPError` for asynchronous client errors
- `ValueError` for invalid parameters
- `InvalidSignature` for invalid webhook signatures

## Type Hints

The client includes comprehensive type hints for better IDE support and type checking. All models and responses are properly typed using Pydantic models.

## Publishing

This package is published to PyPI using modern Python packaging tools. Here's how to publish a new version:

1. Install the required tools globally (outside of any virtual environment):
```bash
# Install twine globally
pip install twine

# Install hatch and hatchling if you haven't already
pip install hatch hatchling
```

2. Update the version in `pyproject.toml`:
```toml
[project]
version = "0.1.0"  # Update this to your new version
```

3. Build the package:
```bash
# Make sure you're not in the Hatch shell
hatch build
```

4. Test the build:
```bash
# On Windows:
hatch run python -m pip install dist\uxly_1shot_client-1.0.25-py3-none-any.whl

# On Unix-like systems (Linux/macOS):
hatch run python -m pip install dist/uxly_1shot_client-1.0.25-py3-none-any.whl
```

5. Upload to PyPI:
```bash
# First, upload to TestPyPI to verify everything works
python -m twine upload --repository testpypi dist/uxly_1shot_client-1.0.25-py3-none-any.whl dist/uxly_1shot_client-1.0.25.tar.gz

# If everything looks good, upload to the real PyPI
python -m twine upload dist/uxly_1shot_client-1.0.25-py3-none-any.whl dist/uxly_1shot_client-1.0.25.tar.gz
```

Note: You'll need to have a PyPI account and configure your credentials. You can do this by:
1. Creating a `~/.pypirc` file:
```ini
[pypi]
username = your_username
password = your_password
```

Or by using environment variables:
```bash
# On Windows PowerShell:
$env:TWINE_USERNAME="your_username"
$env:TWINE_PASSWORD="your_password"

# On Windows Command Prompt:
set TWINE_USERNAME=your_username
set TWINE_PASSWORD=your_password

# On Unix-like systems (Linux/macOS):
export TWINE_USERNAME=your_username
export TWINE_PASSWORD=your_password
```

**Important**: Make sure you're not in the Hatch shell when running twine commands. The tools should be installed globally and run from your system's Python environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 