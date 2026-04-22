## USAGE 1

# What you asked - the prompt or question
- I asked AI in plan mode to help with scoping out the steps of completing this project

# What AI generated - the output you received
- AI generated a MVP plan that maps out steps to complete the project in phases and by days.

# What you did with it - how you verified, modified, or integrated the output
- I am using this as my plan throughout the project, mostly yo help with time management and to stay o track of all necessary parts of the project. 
- I will conistently check in with this plan, and likely adapt it to fit my needs are the projects becomes further developed. 

# What you learned - what you understood better as a result
- A good MVP scope depends on measurable criteria, not just features. While creating my plan with AI, I realized how important it was for it not only include each feature I want to build, but also to space out the timing of each feature so that I can make sure that I have enough time to ensure they all work together before moving onto the next. 

## USAGE 2
# What you asked - the prompt or question
- I asked AI for help with starting to define acceptance criteria and how the program would define the txt files

# What AI generated - the output you received
- AI generated some code, which I went through and annotated to ensure understanding
- The code does the following: 
    - Read menu text from a .txt file or pasted input
    - Find lines with a price
    - Extract dish name + price
    - Tag allergens and cuisine keywords
    - Print summary + dishes

# What you did with it - how you verified, modified, or integrated the output
- I tried to verify that the code worked by copying and pasteing different restaurnt menus in the terminal. For each menu I tried, there was a different error. I think this is because each menu is formatted in a different way, which makes it hard for the program to parse.
- I narrowed the MVP implementation in `menu.py` to reduce parsing complexity

# What you learned - what you understood better as a result
 Restaurant menu data is messy and unstructured. It may be impossible to handle edge cases that will work for every single menu. To overcome this, I am going to try narrow the MVP to just:
    - User pastes menu text
    - Program flags dishes that contain fish, are vegetarian, or contain common allergens
    - Program displays average price range



### As of right now: menu decoder doesn't work but should...

# New MVP acceptance criteria
- Input: user can paste menu text directly into terminal.
- Dish parsing: a dish is counted when a line contains a price token.
- Flags: each detected dish includes `fish` (true/false), `vegetarian` (true/false), and `allergens` (list).
- Price analytics: program outputs `average_price` and `price_range` `[min, max]` for parsed prices.
- Resilience: blank input exits cleanly with a helpful message.

# What the program now does:
- User pastes menu text in terminal (no file argument mode).
- For each dish line with a price, it flags:
    - fish: true/false
    - egetarian: true/false
    - common allergens: list
It displays:
    - average_price
    - price_range as [min, max]