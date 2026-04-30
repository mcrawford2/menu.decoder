# What your project does
Menu Decoder is a tool that allows users to get a quick restaurant summary from pasted menu text. Instead of manually searching through menus, users can paste menu content into a Flask web app and get cuisine type, price range, average dish price, vegetarian friendliness, pescatarian friendliness, and repeated allergen signals. This is useful for all restaurant-goers, but especially those who have food restrictions who are constantly having to manually read though menus. This app allows them to choose a restaurant more efficiently, and continue eating with peace of mind.

# How to install and run it
1. Create or activate the existing virtual environment in this repository.
2. Run `pip install -r requirements.txt` to install the dependencies
3. Run `python app.py` to start the web app
4. Open the local address shown in the terminal (http://127.0.0.1:5000/)
5. Find restaurnt of choice and paste menu text into the form
6. Click 'Analyze menu' for menu summary
7. Click 'Paste new menu' to restart

# Any required API keys or setup steps
- No API keys are needed.
- The app uses local keyword matching and text parsing only