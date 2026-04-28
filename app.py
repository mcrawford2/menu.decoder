from flask import Flask, render_template, request

from menu import analyze_menu, normalize_menu_text

app = Flask(__name__)
MAX_MENU_LENGTH = 50_000


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    menu_text = ""

    if request.method == "POST":
        menu_text = request.form.get("menu_text", "")

        if not menu_text.strip():
            error = "Paste menu text before submitting."
        elif len(menu_text) > MAX_MENU_LENGTH:
            error = "Menu text is too long (max 50,000 characters)."
        else:
            clean_text = normalize_menu_text(menu_text)
            result = analyze_menu(clean_text)

    return render_template(
        "index.html",
        error=error,
        result=result,
        menu_text=menu_text,
        max_length=MAX_MENU_LENGTH,
    )


if __name__ == "__main__":
    app.run(debug=True)
