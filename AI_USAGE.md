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
- I tried to verify that the code worked by copying and pasteing different restaurant menus in the terminal. For each menu I tried, there was a different error. I think this is because each menu is formatted in a different way, which makes it hard for the program to parse.
- I narrowed the MVP implementation in `menu.py` to reduce parsing complexity

# What you learned - what you understood better as a result
 Restaurant menu data is messy and unstructured. It may be impossible to handle edge cases that will work for every single menu. To overcome this, I am going to try narrow the MVP to just:
    - User pastes menu text
    - Program flags dishes that contain fish, are vegetarian, or contain common allergens
    - Program displays average price range


## USAGE 3

# What you asked - the prompt or question
- I was having a lot of difficulty with parsing errors after copying and pasteing menus. I then copy and pasted the errors into the Copilot integrated chatbox (the AI tool I usually use) and asked AI to help me understand and fix the errors, but I did not like the responses it was giving me. It kept creating new sample menu txt files and saying the errors were fixed, but I was still receiving errors ant not understanding the process. Because of this, I switched to Claude.ai and asked it to do the same thing. 

# What AI generated - the output you received
- Claude helped me treat the pasted menu as raw text from the start with no assumptions about formatting
- It directed me to use Unicodedata
- It also recommended using an API for normalizing menus rather than by keyword, which I will consider switching too once I reach my MVP

# What you did with it - how you verified, modified, or integrated the output
- I tested the new code with three different menu and saw as they each returned unique outputs, with no errors

# What you learned - what you understood better as a result
- Unicode is the universal system for representing text from every language and symbol set, and using Unicodedata converts compatibility of fancy Unicode characters into their simplest form
- Using an API rather than keyword search might make the program more accurate, because keyword libraries might be missing words that API would catch


## USAGE 4

# What you asked - the prompt or question
- I asked AI to help create two boolean expressions
1. The restaurant/menu is vegetarian friendly and shows true if there are more than three dishes with no meat or fish keywords, otherwise shows false
2. If the restaurant/menu is pescatarian friendly and shows true if there are more than three dishes with no meat keywords, otherwise show false

# What AI generated - the output you received
- The AI originally generated:
    vegetarian_friendly = sum(
        1
        for dish in dishes
        if "contains-meat" not in dish["dietary_tags"] and "contains-fish" not in dish["dietary_tags"]
    ) > 3
    pescatarian_friendly = all("contains-meat" not in dish["dietary_tags"] for dish in dishes)
...
    vegetarian_friendly = str(summary.get('vegetarian_friendly', False)).lower()
    pescatarian_friendly = str(summary.get('pescatarian_friendly', False)).lower()

# What you did with it - how you verified, modified, or integrated the output
- This is not output I expected because it does not look like boolean expressions I have used in the past. 
- I modified the code so that pescatarian_friendly also had to check for 3 non-meat dishes, rather than using all(), which would have been too strict
- I verified it worked accurately by testing the code with three different menus, and then manually reading over the code.

# What you learned - what you understood better as a result
- I learned a new method of creating conditional boolean true/false expressions. I was not used to seeing sum() to count the number of passing dishes, and then converted to true/false later. However, I think that having it organized this way makes it easy to read through in the context of the whole script. 
- This presented me another potential error: conditionals like these are keyword-based and only count parsed dish lines that have prices in-line. Accuracy may depend on dish wording and price-line formatting in the menu text.


## USAGE 5

# What you asked - the prompt or question
- I asked AI to help parse multi-line dish descriptions

# What AI generated - the output you received
- AI generated code that helped with blocks of parsed information, rather than individual lines. 

# What you did with it - how you verified, modified, or integrated the output
- I checked this by manually reading through and inputting more menus into the program, and it does seem the accuracy is better. However, I think it could still be better improved, specifically in regards to sorting based on item type (appetizer, entree, dessert, other)

# What you learned - what you understood better as a result
- Parsing in blocks rather than by line improved overall accuracy, especially for multi-line dish descriptions


## USAGE 6

# What you asked - the prompt or question
- When testing more menus, there was one restaurant that created errors. Because of this, I asked AI why some menus work while others don't

# What AI generated - the output you received
- AI replied that there was nothing in the code that would cause an error in one menu and not another. It filtered through parsing, formatting, text normalization, input rules, and validations, and returned nothing that would cause errors.

# What you did with it - how you verified, modified, or integrated the output
- Rather than asking generally about any errors, I pasted the exact menu that created the errors into the attached Copilot. 

# What you learned - what you understood better as a result
- AI from pasteing the error-causing menu directly into Copilot helped me learn that I need to account for menus that have pricing on their own lines. The block pricing I have was not prepared for that, but I will fix it to be able to handle these instances.
- This also helped me learn the importance of running multiple checks. Although it may feel as though I have run many already, menus especially can be formatted in so many unique ways, and I want this app to be bale to account for all types. 


## USAGE 7

# What you asked - the prompt or question
- While trying to incorporate organization based on item type (appetizer, entree, dessert, other), I asked Claude for tips on how to most efficiently add the new code and for potential problems adding this could cause

# What AI generated - the output you received
- Claude's response was to add it as new code after what has already been written, to avoid making everything ore fragile. It also told me to begin with header detection first, and to add an "other" category to avoid wrong classificaitons. 
- Claude warned that this addition would be tricky, and likely would create a lot more accuracy concerns. 

# What you did with it - how you verified, modified, or integrated the output
- I tried creating header detection similar to the dictionaries created for flagging allergens, meat, and fish. 
- After attempting to create and incorporate new code the new dicionaries, I am thinking that this modifiction is not worth the inaccuracies it will cause. The "other" section risks being large, and taking away from the validity of all categories. 

# What you learned - what you understood better as a result
- I thought item type organization would improve accuracy, but instead it added further complications 
- I knew that menus struggle with inconsistent formatting, but this brought forward an even larger extent of that as sections of menus are rarely titled the same. 
- Adding an API rather than using keywords might have been more productive for this


## USAGE 8

# What you asked - the prompt or question
- My final use of AI was re-reading through the entire text, and asking it what specific lines mean that I may have forgotten since starting the project or just want further clarification on
    - example: "what is .2f in line 218"

# What AI generated - the output you received
- For each question, AI generates a thorough response that allows me to understand not just the individual line, but how it impacts the whole tool
- in final testing, it also created new .py and .txt menus to test

# What you did with it - how you verified, modified, or integrated the output
- Sometimes I add what it tells me into comments directly in the code, so I can be reminded when I read through again. Other times I just read it's response for my internal understanding
- AI ran the test menus through the real menu.py code to validate accuracy

# What you learned - what you understood better as a result
- This helps me understand how pieces of code that were written across multiple days of work all come together for the final output