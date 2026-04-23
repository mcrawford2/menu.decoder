import unicodedata
import re


# ── Allergen & keyword data ────────────────────────────────────────────────────

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

PRICE_PATTERN = re.compile(r'(?:\$\s*)?(\d+(?:\.\d{1,2})?)\s*$')


# ── Text cleaning ──────────────────────────────────────────────────────────────

def normalize_menu_text(raw_text):
    text = unicodedata.normalize("NFKC", raw_text)

    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2022": "-",
        "\u00b7": "-",
        "\u00a0": " ",
        "\t": "    ",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


# ── Analysis helpers ───────────────────────────────────────────────────────────

def detect_allergens(text):
    text_lower = text.lower()
    found = []
    for allergen, keywords in ALLERGENS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(allergen)
    return found


def detect_dietary_tags(text):
    text_lower = text.lower()
    has_meat = any(kw in text_lower for kw in MEAT_KEYWORDS)
    has_fish = any(kw in text_lower for kw in FISH_KEYWORDS)
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


def detect_cuisine(full_text):
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
    dishes = []
    for line in clean_text.split("\n"):
        line = line.strip()
        if not line or len(line) < 4:
            continue

        prices = PRICE_PATTERN.findall(line)
        price = f"${prices[0]}" if prices else None

        # skip section headers (all caps, no price)
        if line.isupper() and not price:
            continue

        if not price:
            continue

        name_part = PRICE_PATTERN.sub("", line).strip(" .-")
        if not name_part:
            continue

        allergens = detect_allergens(name_part)
        tags = detect_dietary_tags(name_part)

        dishes.append({
            "name": name_part,
            "price": price,
            "allergens": allergens,
            "dietary_tags": tags,
        })

    return dishes


# ── Core analysis ──────────────────────────────────────────────────────────────

def analyze_menu(clean_text):
    dishes = parse_dishes(clean_text)
    prices = [float(d["price"][1:]) for d in dishes if d["price"]]
    vegetarian_friendly = sum(
        1
        for dish in dishes
        if "contains-meat" not in dish["dietary_tags"] and "contains-fish" not in dish["dietary_tags"]
    ) > 3
    pescatarian_friendly = sum(
        1
        for dish in dishes
        if "contains-meat" not in dish["dietary_tags"]
    ) > 3

    avg_price = f"~${sum(prices)/len(prices):.2f}" if prices else "N/A"

    if prices:
        avg = sum(prices) / len(prices)
        if avg < 12:    price_range = "$      (budget-friendly)"
        elif avg < 20:  price_range = "$$     (moderate)"
        elif avg < 35:  price_range = "$$$    (upscale)"
        else:           price_range = "$$$$   (fine dining)"
    else:
        price_range = "Unknown"

    return {
        "restaurant_summary": {
            "cuisine_type": detect_cuisine(clean_text),
            "price_range": price_range,
            "average_dish_price": avg_price,
            "vegetarian_friendly": vegetarian_friendly,
            "pescatarian_friendly": pescatarian_friendly,
        },
        "dishes": dishes,
    }


# ── Display ────────────────────────────────────────────────────────────────────

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

    print("="*60)


# ── Input ──────────────────────────────────────────────────────────────────────

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


# ── Main ───────────────────────────────────────────────────────────────────────

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