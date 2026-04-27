import unicodedata #used for text cleaning and normalization
import re #used for finding and changing tetx patterns, such as prices and unwanted characters


# Keyword Dictionaries

#allergens to look for in menu items, mapped to common keywords that indicate their presence
ALLERGENS = {
    "dairy":     ["cheese", "cream", "milk", "butter", "yogurt", "parmesan", "mozzarella", "cheddar", "brie", "ricotta", "gouda", "feta"],
    "gluten":    ["bread", "pasta", "flour", "wheat", "crouton", "breaded", "battered", "tortilla", "noodle", "pita", "rye", "barley"],
    "nuts":      ["almond", "walnut", "pecan", "cashew", "pistachio", "hazelnut", "peanut", "pine nut", "macadamia", "chestnut"],
    "shellfish": ["shrimp", "crab", "lobster", "scallop", "clam", "oyster", "mussel", "prawn", "crawfish"],
    "eggs":      ["egg", "eggs", "frittata", "quiche", "aioli", "hollandaise", "meringue"],
    "soy":       ["soy", "tofu", "edamame", "miso", "tempeh"],
}

MEAT_KEYWORDS = [
    "chicken", "beef", "pork", "lamb", "duck", "steak", "bacon", "sausage",
    "turkey", "veal", "venison", "prosciutto", "pepperoni", "salami",
    "brisket", "chorizo", "pancetta", "ham", "ribs", "wings", "meat",
]

FISH_KEYWORDS = [
    "salmon", "tuna", "cod", "tilapia", "halibut", "mahi", "trout", "bass",
    "swordfish", "anchovy", "sardine", "fish", "shrimp", "scallop", "crab",
    "lobster", "clam", "oyster", "mussel", "prawn", "seafood", "octopus", "squid",
]

CUISINE_KEYWORDS = {
    "Italian":  ["pasta", "pizza", "risotto", "gnocchi", "tiramisu", "parmesan", "prosciutto", "bruschetta", "linguine", "penne", "carbonara"],
    "Mexican":  ["taco", "burrito", "enchilada", "salsa", "guacamole", "quesadilla", "tortilla", "cilantro", "carnitas", "tamale"],
    "Japanese": ["sushi", "ramen", "miso", "tempura", "udon", "soba", "teriyaki", "edamame", "sashimi", "tonkatsu"],
    "Indian":   ["curry", "naan", "tikka", "masala", "samosa", "dal", "paneer", "chutney", "biryani", "tandoori"],
    "American": ["burger", "fries", "wings", "bbq", "ribs", "mac and cheese", "grilled cheese", "brisket", "cornbread"],
    "Chinese":  ["fried rice", "dumpling", "wonton", "kung pao", "lo mein", "egg roll", "hoisin", "bok choy", "dim sum"],
    "Thai":     ["pad thai", "satay", "coconut milk", "lemongrass", "thai basil", "green curry", "tom yum"],
    "French":   ["crepe", "baguette", "brie", "croissant", "ratatouille", "bouillabaisse", "coq au vin", "souffle"],
    "Greek":    ["gyro", "tzatziki", "hummus", "falafel", "spanakopita", "dolma", "pita", "feta", "moussaka"],
    "Spanish":  ["paella", "tapas", "chorizo", "gazpacho", "patatas", "manchego", "albondigas"],
}

#matches prices to menu format, allowing for optional dollar sign, optional space, and ensuring it is at the end of the line
PRICE_PATTERN = re.compile(r'(?:\$\s*)?(\d+(?:\.\d{1,2})?)\s*$')

#to avoid false matches (such as ham in champagne)
def keyword_present(text, keywords):
    """Return True when any keyword appears as a whole word or phrase."""
    for keyword in keywords:
        pattern = r'(?<!\w)' + re.escape(keyword.lower()) + r'(?!\w)' #r'(?<!\w)': makes sure a keyword starts at a real word boundary
        if re.search(pattern, text):
            return True
    return False


# Menu Text Cleaning

def normalize_menu_text(raw_text):
    text = unicodedata.normalize("NFKC", raw_text)

    replacements = {
        "\u2018": "'", "\u2019": "'",   #left vs right single quotes
        "\u201c": '"', "\u201d": '"',   #left vs right double quotes
        "\u2013": "-", "\u2014": "-",   #en dash and em dash to hyphen
        "\u2022": "-",                  #bullet points to hyphen
        "\u00b7": "-",                  #middle dot (often used as bullet) to hyphen  
        "\u00a0": " ",                  #non-breaking space to regular space
        "\t": "    ",                   #tabs to 4 spaces
    }

    #cleaning up, making menu text consistent and easier to parse
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    text = text.replace("\r\n", "\n").replace("\r", "\n") #line endings 
    text = re.sub(r"\n{3,}", "\n\n", text)                #collapse multiple blank lines to max 2
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


# Analysis Helpers

#not directly used in final output
def detect_allergens(text):
    """Detect allergens in the text based on keyword matching."""
    text_lower = text.lower()
    found = []
    for allergen, keywords in ALLERGENS.items():
        if keyword_present(text_lower, keywords):
            found.append(allergen)
    return found


def detect_dietary_tags(text):
    """Detect dietary tags based on presence of meat/fish keywords."""
    text_lower = text.lower()
    has_meat = keyword_present(text_lower, MEAT_KEYWORDS)
    has_fish = keyword_present(text_lower, FISH_KEYWORDS)
    tags = []
    if not has_meat and not has_fish:
        tags.append("vegetarian")
    if not has_meat:
        tags.append("pescatarian-friendly")
    if has_fish:
        tags.append("contains-fish")
    if has_meat:
        tags.append("contains-meat")
    return tags


def is_friendly(dishes, predicate):
    """Heuristic for whether a menu has enough matching dishes to be friendly."""
    total_dishes = len(dishes)
    if total_dishes == 0:
        return False

    matching_dishes = sum(1 for dish in dishes if predicate(dish))
    return matching_dishes >= 3 and (matching_dishes / total_dishes) >= 0.15


def detect_cuisine(full_text):
    """Detect cuisine type based on keyword matching."""
    text_lower = full_text.lower()
    scores = {}
    for cuisine, keywords in CUISINE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[cuisine] = score
    if not scores:
        return "Unknown"
    return max(scores, key=scores.get)


def parse_dishes(clean_text):
    """
    Parse dishes from menu text, grouping multi-line descriptions.
    
    Strategy:
    1. Split text into logical blocks (separated by blank lines)
    2. For each block, find the line with a price (primary dish line)
    3. Remaining lines in the block are description/ingredients
    4. Combine name + description for analysis
    """
    dishes = []
    lines = clean_text.split("\n")
    
    # Group lines into blocks (sections separated by blank lines or section headers)
    blocks = []
    current_block = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            if current_block:
                blocks.append(current_block)
                current_block = []
            continue
        
        # Skip section headers (all caps, short, no price)
        if line.isupper() and not PRICE_PATTERN.search(line):
            if current_block:
                blocks.append(current_block)
                current_block = []
            continue
        
        current_block.append(line)
    
    if current_block:
        blocks.append(current_block)
    
    # Parse each block
    for block in blocks:
        # Find which line(s) contain prices
        price_lines = [(i, line) for i, line in enumerate(block) if PRICE_PATTERN.search(line)]
        
        if not price_lines:
            continue
        
        # Parse each price-containing line as a separate dish.
        for price_pos, (primary_idx, primary_line) in enumerate(price_lines):
            next_price_idx = price_lines[price_pos + 1][0] if price_pos + 1 < len(price_lines) else len(block)

            prices = PRICE_PATTERN.findall(primary_line)
            price = f"${prices[0]}" if prices else None
            name_and_description = PRICE_PATTERN.sub("", primary_line).strip(" .-")

            if not name_and_description or not price:
                continue

            name = name_and_description
            inline_description = ""
            split_match = re.split(r"\s[-:]\s", name_and_description, maxsplit=1)
            if len(split_match) == 2:
                name, inline_description = split_match

            # Collect description lines that belong to this dish, stopping at the next dish.
            description_parts = [inline_description] if inline_description else []
            for i in range(primary_idx + 1, next_price_idx):
                line = block[i]
                if PRICE_PATTERN.search(line):
                    continue
                description_parts.append(line)

            # Combine name + description for allergen/dietary analysis
            full_text = name
            if description_parts:
                full_text += " " + " ".join(part for part in description_parts if part)

            allergens = detect_allergens(full_text)
            tags = detect_dietary_tags(full_text)

            dishes.append({
                "name": name,
                "price": price,
                "allergens": allergens,
                "dietary_tags": tags,
            })
    
    return dishes


# Menu Analysis

def analyze_menu(clean_text):
    """Analyze the menu text to extract restaurant summary and dish details."""
    dishes = parse_dishes(clean_text)
    prices = [float(d["price"][1:]) for d in dishes if d["price"]] #loops through every dish, keeps only dishes with a price, removes $, converts text to number, then (after this loop) creates list of prices
    vegetarian_friendly = is_friendly(
        dishes,
        lambda dish: "contains-meat" not in dish["dietary_tags"] and "contains-fish" not in dish["dietary_tags"],
    )
    pescatarian_friendly = is_friendly(
        dishes,
        lambda dish: "contains-meat" not in dish["dietary_tags"],
    )

    avg_price = f"~${sum(prices)/len(prices):.2f}" if prices else "N/A" #.2f = 2 decimal places

# for Display
    if prices:
        avg = sum(prices) / len(prices)
        if avg < 12:    price_range = "$      (budget-friendly)"
        elif avg < 20:  price_range = "$$     (moderate)"
        elif avg < 35:  price_range = "$$$    (upscale)"
        else:           price_range = "$$$$   (fine dining)"
    else:
        price_range = "Unknown"

    # Count allergen keyword occurrences across the whole menu text
    text_lower = clean_text.lower()
    allergen_counts = {}
    for allergen, keywords in ALLERGENS.items():
        count = 0
        for kw in keywords:
            pattern = r"\b" + re.escape(kw.lower()) + r"\b"
            count += len(re.findall(pattern, text_lower))
        allergen_counts[allergen] = count

    # Flag any allergen where combined keyword occurrences exceed threshold
    FLAG_THRESHOLD = 10
    flagged = {a: c for a, c in allergen_counts.items() if c > FLAG_THRESHOLD}

    return {
        "restaurant_summary": {
            "cuisine_type": detect_cuisine(clean_text),
            "price_range": price_range,
            "average_dish_price": avg_price,
            "vegetarian_friendly": vegetarian_friendly,
            "pescatarian_friendly": pescatarian_friendly,
            "flagged_allergens": flagged,
        },
        "dishes": dishes,
    }


# Terminal Display

def display_results(data):
    summary = data.get("restaurant_summary", {})

    print("\n" + "="*60)
    print("  RESULTS")
    print("="*60)

    print("\n--- Restaurant Overview ---")
    print(f"  Cuisine:      {summary.get('cuisine_type', 'Unknown')}")
    print(f"  Price range:  {summary.get('price_range', 'Unknown')}")
    print(f"  Average dish: {summary.get('average_dish_price', 'N/A')}")
    vegetarian_friendly = str(summary.get('vegetarian_friendly', False)).lower()
    pescatarian_friendly = str(summary.get('pescatarian_friendly', False)).lower()
    print(f"  Vegetarian friendly:   {vegetarian_friendly}")
    print(f"  Pescatarian friendly:   {pescatarian_friendly}")

    # Show any high-frequency allergen hits (based on keywords)
    flagged = summary.get("flagged_allergens", {}) or {}
    if flagged:
        print("\n--- Flagged Allergens (high frequency) ---")
        for allergen, count in flagged.items():
            print(f"  {allergen}: {count} occurrences")

    print("="*60)


# User Input

def get_menu_from_user():
    print("\n" + "="*60)
    print("  MENU DECODER")
    print("="*60)
    print("\nPaste your menu text below.")
    print("When finished, type END on its own line and press Enter.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip().upper() == "END":
            break
        lines.append(line)

    return "\n".join(lines)


# Main

def main():
    raw_text = get_menu_from_user()

    if not raw_text.strip():
        print("\n[Error] No menu text was entered.")
        return

    if len(raw_text) > 50_000:
        print("\n[Error] Menu text is too long (max 50,000 characters).")
        return

    clean_text = normalize_menu_text(raw_text)
    result     = analyze_menu(clean_text)
    display_results(result)


if __name__ == "__main__":
    main()