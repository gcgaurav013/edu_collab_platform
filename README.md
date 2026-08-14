Step-by-Step Setup Guide
Follow these steps to run the platform locally on your machine:

1. Configure the Environment
   Ensure you have Python 3.10 or higher installed, then set up your environment by executing the following commands in your terminal:

Bash

# Create a dedicated directory and navigate inside

mkdir edu_collab_platform
cd edu_collab_platform

# Initialize a clean virtual environment

python -m venv venv

# Activate the virtual environment

# On macOS/Linux:

source venv/bin/activate

# On Windows:

venv\Scripts\activate 2. Populate the Files
Create three distinct files matching the structure specified above: requirements.txt, core_modules.py, and app.py. Paste their corresponding code blocks into each file.

3. Install Required Dependencies
   Run the installation command to fetch the required processing, UI, and semantic calculation libraries:

Bash
pip install -r requirements.txt 4. Run the Streamlit Prototype Application
Launch the local web server hosting the application:

Bash
streamlit run app.py
Once initialized, a browser tab will automatically open at http://localhost:8501, loading your AI-Driven Multi-Format Educational Collaboration Platform dashboard.

💡 How to Use the App for a Demo
Authenticate the Model Core: Open the sidebar, select your preferred model engine provider (e.g., Gemini (Google)), and provide your API Key.

Upload a Target Document: Go to the Data Ingestion & Setup module and upload an educational PDF file.

Generate Assets: Navigate through the Summarization and Transformation tabs to instantly turn your document into flashcards, interactive quizzes, or multi-tiered study notes.

Review the Validation Metrics: Check the System Verification Ledger tab to review the mathematical reliability reports. Here, you can monitor how effectively the alignment engine catches potential model hallucinations before they reach a student.
