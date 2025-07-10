# CKKS Calculator Web App

This project is a web-based calculator that demonstrates privacy-preserving computation using the CKKS homomorphic encryption scheme via [TenSEAL](https://github.com/OpenMined/TenSEAL). It supports encrypted vector addition and multiplication, and compares the decrypted (approximate) result to the actual plaintext result, reporting precision loss.

## Features
- **CKKS Homomorphic Encryption**: All calculations are performed on encrypted data using the CKKS scheme.
- **Vector Operations**: Supports element-wise addition and multiplication of vectors (comma-separated numbers).
- **Precision Loss Tracking**: Reports the maximum and average absolute error between the decrypted CKKS result and the actual plaintext result.
- **Modern Web UI**: Responsive, user-friendly frontend.

## Setup Instructions

### Prerequisites
- Python 3.7+
- [TenSEAL](https://github.com/OpenMined/TenSEAL) (`pip install tenseal`)
- Flask (`pip install flask`)

### Installation
1. Clone this repository or copy the files to your project directory.
2. Install dependencies:
   ```bash
   pip install flask tenseal
   ```
3. Run the Flask app:
   ```bash
   python app.py
   ```
4. Open your browser and go to [http://localhost:5000/](http://localhost:5000/)

## Usage
1. Enter two numbers or vectors (comma-separated, e.g., `1,2,3`) in the input fields.
2. Select the operation (Add or Multiply).
3. Click **Calculate**.
4. The app will display:
   - The decrypted result (from CKKS)
   - The actual plaintext result
   - The precision loss (max and average absolute error)
   - A sample of the encrypted data

## Example
- **Input:**
  - First vector: `1,2,3`
  - Second vector: `4,5,6`
  - Operation: `Add`
- **Output:**
  - Decrypted result: `5.0, 7.0, 9.0` (approximate)
  - Actual result: `5.0, 7.0, 9.0`
  - Precision loss: Max abs error = `~1e-7`, Avg abs error = `~1e-7`

## Notes
- The CKKS scheme is approximate; small errors are expected.
- The app is for educational/demo purposes and not for production use.

## License
MIT 