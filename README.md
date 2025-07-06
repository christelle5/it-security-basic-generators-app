## 🔐 IT Security Basic Generators App

**IT Security Basic Generators App** is a simple GUI-based desktop tool that demonstrates the basic principles of information security through five cryptographic methods.

### ✨ Features

- Generate pseudorandom number sequences.
- Encrypt and decrypt text using:
  - **MD5** (hashing)
  - **RC5-CBC-Pad** (symmetric encryption)
  - **RSA** (asymmetric encryption)
  - **Digital Signature (DSS)** (signing & verification)
- Save and read input/output data to/from files.
- Use either Python source code or a compiled `.exe` version (no Python required).

### 🛠️ Technologies Used

- Python 3
- PyCryptodome
- Tkinter
- PyInstaller (for `.exe` build)

### 🛆 Installation & Usage

You can run the app in two ways:

- **Option 1:**  
  Install the dependencies:

  ```bash
  pip install -r requirements.txt
  python main.py
  ```

- **Option 2:**  
  Run the compiled `main.exe` directly (no Python needed).

### 🧪 Included Cryptographic Methods

1. **Pseudorandom Number Generator** – for secure data generation.
2. **MD5** – for hashing input data.
3. **RC5-CBC-Pad** – symmetric encryption/decryption.
4. **RSA** – asymmetric encryption/decryption.
5. **Digital Signature (DSS)** – sign and verify digital messages.

### 📂 File Naming

When saving results, the app names files using the format:  
`result_YY-MM-DD_HH-MM-SS.txt`

### 📩 Feedback

If you have any questions, suggestions, or feedback — feel free to contact the developer.
