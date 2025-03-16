# Infinite Horizons

A work in progress.

## Getting Started

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/Calculator5329/infinite-horizons.git
   ```
   
2. **Change into the Project Directory**  
   ```bash
   cd infinite-horizons
   ```

3. **Ensure Python 3.10.11 is Installed**
   - Check your Python version:
     ```bash
     python --version
     ```
     or
     ```bash
     python3 --version
     ```
   - If it does **not** show `Python 3.10.11`, install it:
     - **Windows:** Download from [python.org](https://www.python.org/downloads/release/python-31011/)
     - **Mac/Linux:** Use a package manager like `brew` or `apt`
       ```bash
       sudo apt install python3.10
       ```
       or
       ```bash
       brew install python@3.10
       ```

4. **Create a Virtual Environment Using Python 3.10.11**
   - If you installed Python 3.10.11, run:
     ```bash
     python3.10 -m venv venv
     ```
   - If `python3.10` is not found, try:
     ```bash
     python -m venv venv
     ```

5. **Activate the Virtual Environment**  
   - On **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

6. **Install the Requirements**  
   ```bash
   pip install -r requirements.txt
   ```

## Usage

After installing dependencies, you can run the main script or module as needed:
```bash
python main.py
```
