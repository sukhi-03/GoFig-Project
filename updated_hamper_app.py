import streamlit as st
import json
import random
from datetime import datetime, timedelta

# Example items and prices
categories = {
    'breakfast': {
        'Yoga Bar Super Muesli No Added Sugar (400 g)': {'price': 234, 'expiry_date': '25 January 2025'},
        'Yoga Bar Fruits Nuts & Seeds Muesli (400 g)': {'price': 234, 'expiry_date': '8 August 2027'},
        'Yoga Bar Creamy Peanut Butter (400 g)': {'price': 161, 'expiry_date': '6 August 2027'},
        'Yoga Bar Dark Chocolate & Cranberry Muesli (400 g)': {'price': 234, 'expiry_date': '6 July 2025'},
        'Yoga Bar Hazelnut 20g Protein Bar (70 g)': {'price': 84, 'expiry_date': '22 March 2027'},
        'True Elements Granola Fruit & Nut (450 g)': {'price': 288, 'expiry_date': '4 September 2027'}
    },
    'chocolates & cookies': {
        'Lindt Lindor Irresistibly Smooth Melting White Cornet (200 g)': {'price': 570, 'expiry_date': '27 June 2026'},
        'Lindt Les Grandes Dark Chocolate Hazelnut (150g)': {'price': 360, 'expiry_date': '4 May 2025'},
        'Lindt Excellence Orange Intense Dark Chocolate (100 g)': {'price': 270, 'expiry_date': '13 April 2026'},
        'STROOM Cashew Hazelnut Butter Bar (36 g)': {'price': 42, 'expiry_date': '9 July 2027'},
        'Yoga Bar Double Chocolate 20g bar Protein (70 g)': {'price': 84, 'expiry_date': '18 November 2025'},
        'Yoga Bar Chocolate Brownie 20g Protein Bar (70 g)': {'price': 84, 'expiry_date': '29 August 2027'},
        'STROOM Creamy Peanut Butter Energy Bar (36 g)': {'price': 35, 'expiry_date': '21 May 2026'},
        'STROOM Milk Chocolate Peanut Butter (36 g)': {'price': 35, 'expiry_date': '12 April 2025'},
        'STROOM Dark Chocolate Peanut Butter Energy (36 g)': {'price': 35, 'expiry_date': '1 November 2025'},
        'Open Secret Peanut Butter Story Box - 6 pcs (75 g)': {'price': 105, 'expiry_date': '26 August 2026'},
        'Lindt Swiss Classic Milk with Almond (100 g)': {'price': 270, 'expiry_date': '6 January 2027'},
        'Imperial Gold Selection Cookies (252 g)': {'price': 255, 'expiry_date': '6 May 2026'},
        'Lindt Swiss Luxury Selection (143 g)': {'price': 1499, 'expiry_date': '5 August 2026'},
        'Lindt Swiss Classic Milk with Hazelnuts (100 g)': {'price': 270, 'expiry_date': '24 April 2026'},
        'Lindt Lindor Smooth Melting Milk Chocolate Cornet (500 g)': {'price': 1200, 'expiry_date': '30 September 2025'},
        'Yoga Bar Almond Fudge 20g Protein Bar (70 g)': {'price': 84, 'expiry_date': '15 January 2025'},
        'Imperial Danish Cookies Blue (200 g)': {'price': 117, 'expiry_date': '24 February 2026'},
        'Lindt Excellence Dark Caramel with a Touch of Sea Salt (100 g)': {'price': 270, 'expiry_date': '24 August 2026'}
  },
    'chips & snacks': {
        'NutsMojo Assorted Flavor Cashew (25 g)': {'price': 21, 'expiry_date': '14 January 2026'},
        'Open Secret Cream and Onion Cashews (60 g)': {'price': 100, 'expiry_date': '11 October 2026'},
        'Cornitos Crusties Rajma Lemon Chilli (50 g)': {'price': 21, 'expiry_date': '29 June 2027'},
        'Cornitos Crusties Rajma King Curry (50 g)': {'price': 21, 'expiry_date': '15 August 2025'},
        'Cornitos Crusties Potato Peri Peri (50 g)': {'price': 21, 'expiry_date': '7 April 2027'},
        'Cornitos Crusties Chana Dilli Chaat (50 g)': {'price': 21, 'expiry_date': '12 January 2027'},
        'Cornitos Crusties Potato Italian Cheese (50 g)': {'price': 21, 'expiry_date': '26 May 2026'},
        'FiT Nutrition Energy Bar | Almonds(73%), Sea Salt & Dark Chocolate (35 g)': {'price': 84, 'expiry_date': '21 June 2027'},
        'True Elements Cheesy Onion Baked Cashews (200 g)': {'price': 257, 'expiry_date': '11 August 2026'}
    },
    'beverages': {
        'Cravova Classic Mojito (300 ml)': {'price': 30, 'expiry_date': '10 June 2026'},
        'Cravova Peach Mojito (300 ml)': {'price': 30, 'expiry_date': '10 February 2025'},
        'Cravova Fresh Lemonade (300 ml)': {'price': 30, 'expiry_date': '7 May 2025'},
        'Lavazza Club Powder Roast & Ground Coffee (250 g)': {'price': 630, 'expiry_date': '7 June 2027'},
        'Lavazza Qualitá Oro Roast & Ground Coffee (250 g)': {'price': 840, 'expiry_date': '26 January 2026'},
        'Lavazza Caffé Espresso Roast & Ground Coffee (250 g)': {'price': 630, 'expiry_date': '2 September 2027'},
        'Lavazza Qualitá Rossa Roast & Ground Coffee (250 g)': {'price': 595, 'expiry_date': '6 July 2026'}
    },
    'protein and health': {
        'Fit Nutrition Energy Bar| Almond, Apricot and Coconut (35 g)': {'price': 84, 'expiry_date': '12 August 2027'}
    },
    'meal solutions': {
        'Mothers Kitchen Punjabi Mango Pickle (180 g)': {'price': 143, 'expiry_date': '16 August 2027'},
        'Mothers Kitchen Slice Mango Pickle (180 g)': {'price': 143, 'expiry_date': '18 January 2026'},
        'Cookd Malai Tikka Kit (70 g)': {'price': 112, 'expiry_date': '23 July 2025'}
    }
 
}

# Load policy or initialize
try:
    with open('policy.json', 'r') as f:
        policy = json.load(f)
except FileNotFoundError:
    policy = {
        cat: {item: 1.0 for item in items.keys()}
              for cat, items in categories.items()
    }

# Set today's date
today = datetime.now()

def parse_expiry_date(date_str):
    return datetime.strptime(date_str, '%d %B %Y')

def create_hamper(budget, selected_categories, expiry_days):
    selected_items = []
    current_total = 0
    max_expiry_date = today + timedelta(days=expiry_days)

    combined_items = []
    for category in selected_categories:
        for item, details in categories[category].items():
            expiry_date = parse_expiry_date(details['expiry_date'])
            if expiry_date >= max_expiry_date:
                combined_items.append((item, details['price'], details['expiry_date'], category))

    combined_items = sorted(combined_items, key=lambda x: policy[x[3]][x[0]] + random.uniform(-0.8, 0.8), reverse=True)
    
    for item, price, expiry_date, category in combined_items:
        if current_total + price <= budget:
            selected_items.append((item, price, expiry_date, category))
            current_total += price
            
    return selected_items, current_total

def update_policy(policy, category, item, feedback, learning_rate=0.3):
    if feedback == 'liked':
        policy[category][item] += learning_rate
    elif feedback == 'disliked':
        policy[category][item] = max(1, policy[category][item] - learning_rate)
    
    with open('policy.json', 'w') as f:
        json.dump(policy, f)
    return policy

def create_bundles(budget, selected_categories):
    bundles = []
    current_total = 0

    for category in selected_categories:
        for item, details in categories[category].items():
            item_price = details['price']
            max_quantity = (budget - current_total) // item_price
            if max_quantity > 0:
                bundles.append((item, max_quantity, category))
                current_total += max_quantity * item_price
    return bundles, current_total

def days_until_expiry(expiry_date_str):
    expiry_date = parse_expiry_date(expiry_date_str)
    return (expiry_date - today).days

# Streamlit UI
st.title("AI Powered Hamper Creation Model")
st.sidebar.header("User Inputs")

# Input budget and categories
budget = st.sidebar.number_input("Enter your budget:", min_value=1, value=500, step=50)
selected_categories = st.sidebar.multiselect(
    "Select categories:",
    options=list(categories.keys()),
    default=list(categories.keys())
)
expiry_days = st.sidebar.slider("Days till expiry date:", min_value=1, max_value=365, value=30)

# Initialize session state
if "hamper" not in st.session_state:
    st.session_state.hamper = []
    st.session_state.total_value = 0

if st.sidebar.button("Create Hamper"):
    if budget > 5000:
        st.session_state.hamper, st.session_state.total_value = create_bundles(budget, selected_categories)
    else:
        st.session_state.hamper, st.session_state.total_value = create_hamper(budget, selected_categories, expiry_days)

if st.session_state.hamper:
    st.subheader("Selected Items")
    for item in st.session_state.hamper:
        if isinstance(item, tuple) and len(item) == 4:
            name, price, expiry_date, category = item
            st.write(f"{name} (Category: {category}) - Price: {price}, Expiry Date: {expiry_date}")
        elif isinstance(item, tuple) and len(item) == 3:
            name, quantity, category = item
            st.write(f"{quantity} x {name} (Category: {category})")
    st.write(f"Total Value: {st.session_state.total_value}")

    st.subheader("Feedback")
    for i, item in enumerate(st.session_state.hamper):
        if len(item) == 4:  # Regular hamper items
            name, price, expiry_date, category = item
            feedback = st.selectbox(f"Do you like {name}?", ['liked', 'disliked'], key=f"feedback_{i}")
            if feedback == 'disliked':
                policy = update_policy(policy, category, name, feedback)
                remaining_budget = budget - st.session_state.total_value + price

                # Find replacement options in the same category
                replacement_options = [
                    (itm, details['price'], details['expiry_date'])
                    for itm, details in categories[category].items()
                    if itm != name and details['price'] <= remaining_budget
                ]

                # Sort replacements: first by proximity to expiry, then by policy
                replacement_options.sort(key=lambda x: (days_until_expiry(x[2]), -policy[category].get(x[0], 0))) # added .get(x[0],0)

                # Get the top 2 replacement options
                top_replacements = replacement_options[:2]

                if top_replacements:
                    replacement_choice = st.radio(
                        f"Choose a replacement for {name}:",
                        [r[0] for r in top_replacements],  # Display only the item names
                        key=f"replacement_{i}"
                    )

                    # Find the chosen replacement details
                    chosen_replacement = next(r for r in top_replacements if r[0] == replacement_choice)

                    # Update hamper and total value
                    st.session_state.hamper[i] = (chosen_replacement[0], chosen_replacement[1], chosen_replacement[2], category)
                    st.session_state.total_value = st.session_state.total_value - price + chosen_replacement[1]
                else:
                    st.write(f"No replacement available for {name} in the same category.")
                break  # Refresh the UI after replacement
    
    st.write("Updated Policy:", policy)