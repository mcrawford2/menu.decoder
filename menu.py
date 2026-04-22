import re


PRICE_RE = re.compile(r"(\$?\d{1,3}(?:\.\d{2})?)")

COMMON_ALLERGENS = {
	"dairy": ["milk", "cheese", "cream", "butter"],
	"egg": ["egg", "aioli", "mayo"],
	"fish": ["fish", "salmon", "tuna", "cod", "anchovy"],
	"shellfish": ["shrimp", "crab", "lobster", "clam", "mussel", "oyster"],
	"peanut": ["peanut"],
	"tree nuts": ["almond", "cashew", "walnut", "pistachio", "pecan", "hazelnut"],
	"soy": ["soy", "tofu", "miso", "edamame"],
	"wheat/gluten": ["wheat", "bread", "pasta", "gluten", "flour"],
	"sesame": ["sesame", "tahini"],
}

FISH_WORDS = ["fish", "salmon", "tuna", "cod", "anchovy", "sardine", "trout", "halibut"]
MEAT_WORDS = ["chicken", "beef", "pork", "bacon", "ham", "turkey", "lamb", "sausage"]
SHELLFISH_WORDS = ["shrimp", "crab", "lobster", "clam", "mussel", "oyster", "scallop"]


def find_tags(text, mapping):
	lower_text = text.lower()
	return [label for label, words in mapping.items() if any(word in lower_text for word in words)]


def contains_any(text, words):
	lower_text = text.lower()
	return any(word in lower_text for word in words)


def parse_menu(text):
	dishes = []
	for raw_line in text.splitlines():
		line = raw_line.strip()
		if not line:
			continue

		price_match = PRICE_RE.search(line)
		if not price_match:
			continue

		price_text = price_match.group(1).replace("$", "")
		try:
			price = float(price_text)
		except ValueError:
			price = None

		name = line[:price_match.start()].strip(" -:|") or "UNKNOWN_DISH"
		text_for_flags = line
		has_fish = contains_any(text_for_flags, FISH_WORDS)
		has_shellfish = contains_any(text_for_flags, SHELLFISH_WORDS)
		has_meat = contains_any(text_for_flags, MEAT_WORDS)

		dishes.append(
			{
				"name": name,
				"price": price,
				"fish": has_fish,
				"vegetarian": (not has_meat) and (not has_fish) and (not has_shellfish),
				"allergens": find_tags(text_for_flags, COMMON_ALLERGENS),
				"warnings": [] if name != "UNKNOWN_DISH" else ["missing_name"],
			}
		)
	return dishes


def summarize(dishes):
	prices = [d["price"] for d in dishes if isinstance(d.get("price"), (int, float))]
	if prices:
		avg_price = round(sum(prices) / len(prices), 2)
		price_range = [round(min(prices), 2), round(max(prices), 2)]
	else:
		avg_price = None
		price_range = [None, None]

	return {
		"dish_count": len(dishes),
		"priced_dish_count": len(prices),
		"average_price": avg_price,
		"price_range": price_range,
	}


def read_text():
	print("Paste menu text, then press Enter on a blank line:")
	lines = []
	while True:
		line = input()
		if not line.strip():
			break
		lines.append(line)
	return "\n".join(lines)


def main():
	text = read_text()

	if not text.strip():
		print("No input provided.")
		return

	dishes = parse_menu(text)
	summary = summarize(dishes)

	print("Summary:")
	print(summary)
	print("\nDishes:")
	for i, dish in enumerate(dishes, 1):
		print(f"{i}. {dish['name']} | ${dish['price']}")
		print(f"   fish: {dish['fish']}")
		print(f"   vegetarian: {dish['vegetarian']}")
		print(f"   allergens: {dish['allergens']}")


if __name__ == "__main__":
	main()
