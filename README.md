## AI Presentation Generator
This application automatically generates PowerPoint presentations from a topic using Google's Gemini API for text and the Pexels API for images.

# Important Note
You must add your own Google Gemini and Pexels API keys to generate presentations. The application will not work without them.

##  Steps to Run on Another Machine
1. Clone the Repository
Open your terminal and run the following commands:

Bash

git clone https://github.com/sakshivedi-1/PPT_Generator.git

2. Install Dependencies
Install all the required Python libraries using the requirements.txt file:

Bash

pip install -r requirements.txt
3. Add Your API Keys
Create a file to securely store your API keys:

Inside the .streamlit folder, a new file named secrets.toml.

Add your keys to secrets.toml in this format:

Ini, TOML

# .streamlit/secrets.toml
GOOGLE_API_KEY = "paste_your_google_gemini_key_here"
PEXELS_API_KEY = "paste_your_pexels_key_here"
4. Run the App
Launch the Streamlit application from your terminal:

Bash

streamlit run app.py
Your web browser will open with the application running.

##  Technology Stack
Backend: Python

UI: Streamlit

AI Model: Google Gemini

Image API: Pexels

