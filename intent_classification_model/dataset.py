import random
import csv

base_greetings = [
    "Hi", "Hello", "Hey", "Good morning", "Good afternoon", "Good evening",
    "How are you", "What's up", "Yo", "Greetings", "Hiya", "Morning",
    "Afternoon", "Evening", "Howdy", "Wassup", "Sup"
]
modifiers = ["", "there", "please", "now", "today", "friend", "mate"]

general_queries = set()
for base in base_greetings:
    for modifier in modifiers:
        query = f"{base} {modifier}".strip()
        general_queries.add(query)

general_queries_list = list(general_queries)
if len(general_queries_list) >= 167:
    general_queries_list = random.sample(general_queries_list, 167)
else:
    general_queries_list += random.choices(general_queries_list, k=167 - len(general_queries_list))

actions = ["rent", "buy", "lease", "find", "show", "get"]
property_types = [
    "apartment", "villa", "flat", "house", "condo", "studio", "penthouse",
    "townhouse", "bungalow", "duplex"
]
purposes = ["rent", "sale", "lease"]
features = [
    "pool", "parking", "garden", "balcony", "gym", "security", "furnished",
    "unfurnished", "pet-friendly", "with a view"
]
attributes = [
    "price", "rent", "size", "address", "location", "area", "number of bedrooms",
    "number of bathrooms", "year built", "amenities"
]
locations = [
    "downtown", "suburbs", "near the park", "in the city center", "close to work",
    "in a quiet area", "near schools", "by the beach"
]
numbers = ["one", "two", "three", "four", "five"]

templates = [
    "I want to {action} a {property_type}",
    "Find me a {property_type} for {purpose}",
    "Show me {property_type} with {feature}",
    "What is the {attribute} of a {property_type} in {location}?",
    "Do you have any {property_type} with {number} bedrooms?",
    "I'm looking for a {property_type} in {location}",
    "Can you find me a {property_type} that is {feature}?",
    "I need a {property_type} for {purpose} in {location}"
]

database_queries_set = set()
while len(database_queries_set) < 167:
    template = random.choice(templates)
    query = template.format(
        action=random.choice(actions),
        property_type=random.choice(property_types),
        purpose=random.choice(purposes),
        feature=random.choice(features),
        attribute=random.choice(attributes),
        location=random.choice(locations),
        number=random.choice(numbers)
    )
    database_queries_set.add(query)
database_queries_list = list(database_queries_set)

subcategories = {
    "jokes": [
        "Tell me a joke", "Do you know any jokes?", "Make me laugh",
        "Say something funny", "Can you tell a funny story?", "What's your best joke?",
        "I need a laugh", "Cheer me up with a joke", "Do you have a sense of humor?",
        "Tell me something hilarious"
    ],
    "weather": [
        "What's the weather like?", "How's the weather today?", "Is it going to rain?",
        "What's the temperature outside?", "Do I need an umbrella?", "Is it sunny?",
        "Will it snow tomorrow?", "What's the forecast for the weekend?",
        "How's the weather in New York?", "Is it hot outside?"
    ],
    "programming": [
        "How do I code in Python?", "What's a for loop?", "Can you help me with programming?",
        "Explain object-oriented programming", "How do I write a function?",
        "What's the difference between Java and C++?", "How do I debug my code?",
        "What is a variable?", "How do I use arrays?", "What's a class in programming?"
    ],
    "general_knowledge": [
        "Who is the president of the United States?", "What is the capital of France?",
        "How tall is Mount Everest?", "When was the Declaration of Independence signed?",
        "Who wrote Romeo and Juliet?", "What is the boiling point of water?",
        "How many continents are there?", "What is the largest planet in the solar system?",
        "Who painted the Mona Lisa?", "What is the currency of Japan?"
    ],
    "personal_questions": [
        "What is your name?", "How old are you?", "Where are you from?",
        "Do you have any hobbies?", "What do you like to do?", "Are you a robot?",
        "Can you think?", "Do you have feelings?", "What's your favorite color?",
        "Do you sleep?"
    ],
    "random_statements": [
        "I like pizza", "Cats are cute", "I hate Mondays", "The sky is blue",
        "Life is beautiful", "I need coffee", "Music is life", "I love traveling",
        "Books are great", "Exercise is important"
    ],
    "other": [
        "Play some music", "Set an alarm for 7 AM", "Remind me to call John",
        "What's the time?", "Can you sing?", "Tell me a story",
        "What's your favorite movie?", "Do you know any recipes?", "How do I fix my car?",
        "What's the meaning of life?"
    ]
}

irrelevant_queries = []
for subcategory, queries in subcategories.items():
    if subcategory != "random_statements":
        for query in queries:
            variations = [query]
            if (query.endswith("?") or query.startswith(("What", "How", "Is", "Do", "Can"))):
                variations.append(f"Can you tell me {query.lower()}")
                variations.append(f"Please let me know {query.lower()}")
            else:
                variations.append(f"Can you {query.lower()}")
                variations.append(f"Please {query.lower()}")
                variations.append(f"I'd like you to {query.lower()}")
            irrelevant_queries.extend(variations)
    else:
        irrelevant_queries.extend(queries)
irrelevant_queries_set = set(irrelevant_queries)
if len(irrelevant_queries_set) >= 167:
    irrelevant_queries_list = random.sample(list(irrelevant_queries_set), 167)
else:
    irrelevant_queries_list = list(irrelevant_queries_set) + random.choices(
        list(irrelevant_queries_set), k=167 - len(irrelevant_queries_set)
    )
dataset = []
for query in general_queries_list:
    dataset.append({"User Query": query, "Intent Label": "general_query"})
for query in database_queries_list:
    dataset.append({"User Query": query, "Intent Label": "database_query"})
for query in irrelevant_queries_list:
    dataset.append({"User Query": query, "Intent Label": "irrelevant"})

random.shuffle(dataset)

if len(dataset) > 500:
    dataset = dataset[:500]

with open("intent_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["User Query", "Intent Label"])
    writer.writeheader()
    for row in dataset:
        writer.writerow(row)
print("CSV dataset generated as 'intent_dataset.csv' with 500 rows.")
