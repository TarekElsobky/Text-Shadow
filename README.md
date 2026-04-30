# Text Shadow - Secure Text Steganography Tool

## Overview
Text Shadow is a desktop steganography application that securely hides encrypted messages within ordinary carrier text using invisible zero-width Unicode characters. It combines Fernet authenticated encryption (AES-128-CBC + HMAC-SHA256) with zero-width character encoding to embed messages undetectably in plain text for discreet transmission or storage.

## Key Features
- **Invisible Embedding**: Uses zero-width Unicode characters to hide encrypted data without altering the visual appearance of carrier text
- **Authenticated Encryption**: Fernet symmetric encryption with optional custom key input or auto-generated keys
- **Modern GUI**: CustomTkinter-based dark mode interface with intuitive navigation
- **File Import**: Import carrier text from local .txt files
- **Clipboard Integration**: One-click copy for generated hidden text and extracted messages
- **Live Operation Logs**: Real-time color-coded feedback for all processes
- **Non-Blocking Operations**: Multi-threaded processing to keep UI responsive
- **Cross-Platform**: Compatible with Windows, macOS, and Linux (Python 3.8+)

## Project Architecture
Modular separation of concerns between core logic and UI components:
```
text_shadow_app/
├── core/                      # Core steganography and cryptographic logic
│   ├── __init__.py
│   ├── constants.py           # Zero-width character definitions and UI color schemes
│   └── steganography.py       # SteganographyEngine with crypto and encoding/decoding logic
├── ui/                        # Graphical user interface components
│   ├── __init__.py
│   ├── ui_widgets.py          # Reusable UI elements (HoverButton, LogBox)
│   └── ui_panels.py           # Main panels (Sidebar, HidePanel, ExtractPanel)
├── __init__.py                # Package initialization
├── main.py                    # Application entry point and root window configuration
├── eyes.ico                   # Windows application icon
├── requirements.txt           # Python dependencies
├── run.bat                    # Windows quick-launch script
└── venv/                      # Virtual environment (local, not version-controlled)
```

### Module Breakdown
#### Core Modules
- **constants.py**: Defines three zero-width Unicode characters for binary encoding:
  - `ZW_ZERO`: Represents binary 0
  - `ZW_ONE`: Represents binary 1
  - `ZW_SPACE`: Represents binary byte separators
  Also contains all UI color constants for consistent theming.
- **steganography.py**: `SteganographyEngine` class with static methods for:
  - Fernet key generation (auto or custom seed via SHA-256 derivation)
  - AES-128-CBC + HMAC-SHA256 encryption/decryption
  - Encrypted text to binary conversion
  - Binary-to-zero-width character mapping and reverse
  - Message embedding into carrier text and extraction from hidden text

#### UI Modules
- **ui_widgets.py**: Custom reusable components:
  - `HoverButton`: Button with hover state effects
  - `LogBox`: Scrolling log display with color-coded log levels (SUCCESS, ERROR, INFO, WARNING)
- **ui_panels.py**: Main interface components:
  - `Sidebar`: Navigation panel to switch between Hide/Extract modes
  - `HidePanel`: Interface for embedding messages into carrier text
  - `ExtractPanel`: Interface for extracting messages from hidden text
- **main.py**: Initializes CustomTkinter root window, configures dark mode, sets up main layout with sidebar, content panels, and shared log box.

## Technical Implementation
Message hiding process:
1. **Key Generation**: Random 32-byte Fernet key auto-generated if no custom key provided. Custom keys are hashed via SHA-256 to derive a 32-byte Fernet key.
2. **Encryption**: Secret message encrypted using Fernet (AES-128-CBC with HMAC-SHA256 authentication) to produce base64-encoded ciphertext.
3. **Binary Conversion**: Ciphertext converted to 8-bit binary string with byte separators.
4. **Zero-Width Encoding**: Binary digits mapped to zero-width characters (0→ZW_ZERO, 1→ZW_ONE, space→ZW_SPACE).
5. **Embedding**: Zero-width characters inserted into carrier text at index 1 (one per character position) to produce final hidden text.

Extraction reverses this process: zero-width characters extracted, converted to binary, decrypted with the same key, and original message recovered.

## Dependencies
- `customtkinter>=5.2.0`: Modern Tkinter extension for native-looking GUIs
- `cryptography>=41.0.0`: Cryptographic primitives for Fernet encryption and SHA-256 key derivation

## Setup Instructions
### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
1. Navigate to the `text_shadow_app` directory:
   ```bash
   cd text_shadow_app
   ```
2. Create and activate a virtual environment (recommended):
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
### Option 1: Windows Quick Launch
Double-click `run.bat` in the project directory.

### Option 2: Manual Launch (All Platforms)
With virtual environment activated:
```bash
python -m text_shadow_app.main
```

### Option 3: Direct Python Execution
```bash
cd text_shadow_app
venv/Scripts/python.exe -m text_shadow_app.main  # Windows
venv/bin/python -m text_shadow_app.main          # macOS/Linux
```

## Usage Guide
### Hiding a Message
1. Launch the application and select **Hide Message** from the sidebar (default mode)
2. (Optional) Enter a custom encryption key in the "ENCRYPTION KEY" field. Auto-generated if left empty.
3. Enter your secret message in the "SECRET MESSAGE" text box
4. Enter or import carrier text via the Import File button in the "CARRIER TEXT" box
5. Click **GENERATE HIDDEN TEXT**
6. Copy output from the "OUTPUT" panel using the Copy to Clipboard button

### Extracting a Message
1. Select **Extract Message** from the sidebar
2. Enter the same encryption key used for hiding (or leave empty if auto-generated key was used)
3. Paste text containing the hidden message into the "TEXT WITH HIDDEN MESSAGE" box
4. Click **EXTRACT MESSAGE**
5. Copy the decrypted message from the "EXTRACTED MESSAGE" panel

### Live Logs
The "LIVE LOGS" panel provides real-time feedback including process status, character counts, error messages, and success confirmations.

## Security Considerations
- **Key Management**: Encryption keys are required for extraction. Store custom keys securely—lost keys cannot be recovered.
- **Steganography Limitations**: Zero-width characters may be stripped by some text processors (CMS platforms, messaging apps). Test hidden text in target environments before use.
- **Encryption Strength**: Fernet provides authenticated encryption for both confidentiality and integrity. Custom keys are derived using SHA-256.

## Troubleshooting
- **Icon Not Found**: Application runs normally without `eyes.ico` (error silently ignored)
- **File Import Fails**: Ensure imported files are valid UTF-8 encoded .txt files
- **Invalid Decryption Key**: Verify the same key used for hiding is entered. Auto-generated keys cannot be recovered if unsaved.
- **No Hidden Message Found**: Ensure pasted text contains zero-width characters—some editors strip invisible characters.
