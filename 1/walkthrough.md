# Walkthrough - Simple AI Agent with No Memory and Tools (Task 1)

This document summarizes the steps taken to set up the Python environment, install required packages, create the Agent script, and verify its behavior.

## Project Structure under Folder 1
- `task1.py` - Main agent script.
- `.env` - Environment configuration containing the API key placeholder.
- `requirements.txt` - Python package dependencies.
- `walkthrough.md` - This documentation.

---

## Setup & Implementation

1. **Virtual Environment Setup**:
   - Created a local Python virtual environment `.venv` to isolate the project dependencies.

2. **Package Installation**:
   - Installed the required packages: `openai-agents`, `python-dotenv`, `langchain-openai==0.2.1`, and `pydantic`.
   - Captured the dependencies in `requirements.txt`.

3. **Script Implementation (`task1.py`)**:
   - Initialized `dotenv` to load the API key from `.env` relative to the script location (using `pathlib.Path(__file__)`).
   - Included safe fallback printing for console environments (if `IPython` is not present).
   - Created a `Fact Checker` agent using the `Agent` and `Runner` classes.
   - Replaced the invalid model `"gpt-4.1"` with `"gpt-4o-mini"`.
   - Wrapped the asynchronous `Runner.run()` in an async `main()` entrypoint function to avoid syntax errors when run directly.

---

## Verification

### 1. Requirements Capture
- Validated that `pip freeze` correctly outputs the installed packages.

### 2. Standalone Code Execution
- Executed `& .venv\Scripts\python 1/task1.py` to test the script.
- The script successfully:
  - Warns that `OPENAI_API_KEY` is not configured.
  - Successfully creates the `Fact Checker` agent.
  - Displays the prompt to verify.
  - Correctly throws an `openai.OpenAIError` indicating that the API key is missing (as expected, since it's not yet populated).

---

## Running the Task

To fully run the agent:
1. Open the `1/.env` file.
2. Add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-actual-api-key-here
   ```
3. Run the script:
   ```powershell
   & .venv\Scripts\python 1/task1.py
   ```
