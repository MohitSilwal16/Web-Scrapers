from time import perf_counter
from io import StringIO

words = [
    "apple",
    "banana",
    "orange",
    "grape",
    "mango",
    "peach",
    "pear",
    "plum",
    "cherry",
    "lemon",
    "lime",
    "melon",
    "berry",
    "kiwi",
    "papaya",
    "coconut",
    "fig",
    "date",
    "raisin",
    "apricot",
    "carrot",
    "potato",
    "tomato",
    "onion",
    "garlic",
    "pepper",
    "lettuce",
    "spinach",
    "broccoli",
    "cabbage",
    "rice",
    "bread",
    "pasta",
    "cheese",
    "butter",
    "milk",
    "cream",
    "yogurt",
    "egg",
    "honey",
    "sugar",
    "salt",
    "spice",
    "coffee",
    "tea",
    "water",
    "juice",
    "soda",
    "soup",
    "sauce",
    "oil",
    "vinegar",
    "cereal",
    "oatmeal",
    "pancake",
    "waffle",
    "cookie",
    "cake",
    "pie",
    "donut",
    "chocolate",
    "vanilla",
    "caramel",
    "mint",
    "cinnamon",
    "ginger",
    "nutmeg",
    "clove",
    "basil",
    "oregano",
    "thyme",
    "parsley",
    "rosemary",
    "sage",
    "dill",
    "chili",
    "cumin",
    "paprika",
    "turmeric",
    "saffron",
    "chicken",
    "beef",
    "pork",
    "fish",
    "shrimp",
    "crab",
    "lobster",
    "tofu",
    "bean",
    "lentil",
    "pea",
    "corn",
    "wheat",
    "barley",
    "oats",
    "rye",
    "quinoa",
    "millet",
    "buckwheat",
    "soy",
]


# 1
start = perf_counter()
text = " ".join(words)
stop = perf_counter()

elapsed = stop - start
print(f"{elapsed * 10e6:.2f} Micro-Seconds")

# 2
text = ""
start = perf_counter()
for word in words:
    text += word + " "

stop = perf_counter()

elapsed = stop - start
print(f"{elapsed * 10e6:.2f} Micro-Seconds")

# 3
text = StringIO()
start = perf_counter()

for word in words:
    text.write(word)
    text.write(" ")


stop = perf_counter()

elapsed = stop - start
print(f"{elapsed * 10e6:.2f} Micro-Seconds")
