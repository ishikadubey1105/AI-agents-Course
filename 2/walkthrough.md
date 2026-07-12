# Walkthrough - Travel Agent AI (Task 2)

This document summarizes the steps taken to resolve the issues in Task 2, secure the credentials, and test the Travel Agent AI.

## Project Structure under Folder 2
- `task2.py` - Main travel agent AI loop.
- `.env` - Environment configuration containing the Groq API key placeholder.
- `requirements.txt` - Python package dependencies for Groq.
- `walkthrough.md` - This documentation.

---

## Issues Resolved

1. **Missing Dependency (`groq`)**:
   - Installed the `groq` package to enable imports.
   - Added `2/requirements.txt` to track dependencies.

2. **Hardcoded Credentials**:
   - Extracted the Groq API key from [task2.py](file:///c:/Users/ishik/.antigravity-ide/AI-agents-Course/2/task2.py).
   - Moved the key to the local environment configuration in [2/.env](file:///c:/Users/ishik/.antigravity-ide/AI-agents-Course/2/.env).
   - Updated the code in `task2.py` to resolve and load the `.env` file relative to the script location (using `pathlib.Path(__file__)`), which ensures it works correctly even when run from the workspace root.

---

## Verification

### Standalone Script Testing
- Tested the refactored script using a query piped to it:
  `echo "suggest a 2 day itinerary for Paris" | & .venv\Scripts\python 2/task2.py`
- The script successfully:
  - Initialized the Groq client.
  - Queried the `llama-3.1-8b-instant` model.
  - Returned a complete and detailed 2-day travel itinerary for Paris.

---

## Running the Code

To run the interactive loop:
1. Open the [2/.env](file:///c:/Users/ishik/.antigravity-ide/AI-agents-Course/2/.env) file to ensure your `GROQ_API_KEY` is present.
2. Run the script:
   ```powershell
   & .venv\Scripts\python 2/task2.py
   ```
3. Type your travel questions. Type `exit` or `quit` to end the conversation.
