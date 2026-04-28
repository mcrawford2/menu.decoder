# What your project does
Menu Decoder is a tool that allows users to get a quick restaurant summary from pasted menu text. Instead of manually searching through menus, users can paste menu content into a Flask web app and get cuisine type, price range, average dish price, vegetarian friendliness, pescatarian friendliness, and repeated allergen signals.

# How to install and run it
1. Create or activate the existing virtual environment in this repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Start the web app with `python app.py`.
4. Open the local address shown in the terminal, paste menu text into the form, and submit it.

# Any required API keys or setup steps
- No API keys are needed.
- The app uses local keyword matching and text parsing only.