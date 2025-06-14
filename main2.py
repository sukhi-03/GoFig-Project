import streamlit as st
import json
import random
from datetime import datetime, timedelta
import copy # Import copy for deep copying policy

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

# --- Policy Handling ---
POLICY_FILE = 'policy.json'

def load_policy():
    """Loads policy from file or initializes a default one."""
    try:
        with open(POLICY_FILE, 'r') as f:
            p = json.load(f)
            # Ensure all current items exist in the loaded policy
            for cat, items in categories.items():
                if cat not in p:
                    p[cat] = {}
                for item in items.keys():
                    if item not in p[cat]:
                        p[cat][item] = 1.0 # Initialize new items
            # Remove items from policy that no longer exist in categories (optional)
            # current_items = {(cat, item) for cat, items in categories.items() for item in items}
            # policy_items = {(cat, item) for cat, items in p.items() for item in items}
            # for cat, item in policy_items - current_items:
            #     if cat in p and item in p[cat]:
            #         del p[cat][item]

            return p

    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize policy if file not found or corrupt
        return {
            cat: {item: 1.0 for item in items.keys()}
            for cat, items in categories.items()
        }

def save_policy(policy_data):
    """Saves the policy data to the JSON file."""
    with open(POLICY_FILE, 'w') as f:
        json.dump(policy_data, f, indent=4) # Use indent for readability

# Load the policy globally or pass it around explicitly
# Using global load for simplicity in this script structure
policy = load_policy()

# Set today's date
today = datetime.now()

def parse_expiry_date(date_str):
    """Parses expiry date string into datetime object."""
    try:
        return datetime.strptime(date_str, '%d %B %Y')
    except ValueError:
        # Handle potential errors if date format is inconsistent
        st.error(f"Error parsing date: {date_str}. Expected format 'DD Month YYYY'.")
        return None # Or return a default date like today

def days_until_expiry(expiry_date_str):
    """Calculates days between today and expiry date."""
    expiry_date = parse_expiry_date(expiry_date_str)
    if expiry_date:
        return (expiry_date - today).days
    return -1 # Indicate error or invalid date

# --- Hamper Creation Logic ---

def create_hamper(budget, selected_categories, expiry_days):
    """Creates a hamper with individual items based on policy and constraints."""
    selected_items = []
    current_total = 0
    min_expiry_date = today + timedelta(days=expiry_days) # Correct logic: Expiry should be AFTER this date

    combined_items = []
    for category in selected_categories:
        if category in categories and category in policy: # Check if category exists
            for item, details in categories[category].items():
                expiry_date_obj = parse_expiry_date(details['expiry_date'])
                # Ensure item exists in policy (might be newly added)
                if item not in policy[category]:
                     policy[category][item] = 1.0 # Initialize if missing

                # Filter by expiry date
                if expiry_date_obj and expiry_date_obj >= min_expiry_date:
                    # Use policy score (default 1.0 if somehow missing) + randomness
                    score = policy[category].get(item, 1.0) + random.uniform(-0.8, 0.8)
                    combined_items.append((item, details['price'], details['expiry_date'], category, score))

    # Sort by calculated score (policy + randomness), descending
    combined_items = sorted(combined_items, key=lambda x: x[4], reverse=True)

    # Select items within budget
    for item, price, expiry_date, category, _ in combined_items: # Ignore score now
        if current_total + price <= budget:
            selected_items.append((item, price, expiry_date, category))
            current_total += price

    return selected_items, current_total

def create_bundles(budget, selected_categories):
    """Creates bundles of items, prioritizing by policy score."""
    bundles = []
    remaining_budget = budget

    # 1. Gather all items from selected categories with their policy scores
    all_items_with_policy = []
    for category in selected_categories:
        if category in categories and category in policy:
            for item, details in categories[category].items():
                 # Ensure item exists in policy (might be newly added)
                if item not in policy[category]:
                     policy[category][item] = 1.0 # Initialize if missing
                item_price = details['price']
                policy_score = policy[category].get(item, 1.0) # Default to 1.0 if missing
                if item_price > 0: # Avoid division by zero or adding free items infinitely
                    all_items_with_policy.append(
                        {'name': item, 'price': item_price, 'category': category, 'policy': policy_score}
                    )

    # 2. Sort items by policy score (descending)
    all_items_with_policy.sort(key=lambda x: x['policy'], reverse=True)

    # 3. Create bundles greedily based on sorted items
    for item_data in all_items_with_policy:
        item_name = item_data['name']
        item_price = item_data['price']
        category = item_data['category']

        if remaining_budget >= item_price: # Can afford at least one
            max_quantity = remaining_budget // item_price
            if max_quantity > 0:
                bundles.append((item_name, max_quantity, category))
                remaining_budget -= max_quantity * item_price

        if remaining_budget <= 0: # Stop if budget is exhausted
            break

    total_spent = budget - remaining_budget
    return bundles, total_spent


# --- Policy Update Logic ---

def update_policy_score(policy_ref, category, item, feedback, learning_rate=0.3):
    """Updates the policy score for a given item based on feedback."""
    if category in policy_ref and item in policy_ref[category]:
        current_score = policy_ref[category][item]
        if feedback == 'liked':
            policy_ref[category][item] = current_score + learning_rate
            st.success(f"👍 Increased score for {item}", icon="📈")
        elif feedback == 'disliked':
            # Ensure score doesn't drop below a minimum (e.g., 0.1 or 0)
            policy_ref[category][item] = max(0.1, current_score - learning_rate)
            st.success(f"👎 Decreased score for {item}", icon="📉")
        # No change for neutral/no feedback
    else:
         st.warning(f"Could not update policy for {item} in {category} (not found).")

    # No need to return policy_ref, modification happens in place
    # Save the updated policy immediately after modification
    save_policy(policy_ref)


# --- Streamlit UI ---
st.set_page_config(layout="wide") # Use wider layout
st.title("🎁 AI Powered Hamper Creation 🎁")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("Hamper Configuration")

    # Input budget and categories
    budget = st.number_input("Enter your budget:", min_value=1.0, value=500.0, step=50.0, format="%.2f")
    available_categories = list(categories.keys())
    selected_categories = st.multiselect(
        "Select categories:",
        options=available_categories,
        default=available_categories # Default to all categories
    )
    expiry_days = st.slider(
        "Minimum days until expiry:",
        min_value=1,
        max_value=730, # Allow up to 2 years
        value=60,       # Default to 60 days
        help="Include items expiring on or after this many days from today."
        )

    # Initialize session state for hamper and total value if they don't exist
    if "hamper" not in st.session_state:
        st.session_state.hamper = []
    if "total_value" not in st.session_state:
        st.session_state.total_value = 0.0
    if "is_bundle" not in st.session_state:
        st.session_state.is_bundle = False # Flag to know the type of hamper


    # --- Create Hamper Button ---
    if st.button("✨ Create/Refresh Hamper ✨", type="primary", use_container_width=True):
        if not selected_categories:
            st.warning("Please select at least one category.")
        else:
            # Make a deep copy of the current policy for this run if needed,
            # Although modifying the global `policy` and saving is the current pattern.
            # current_policy_state = copy.deepcopy(policy) # Use if you want isolation per run

            if budget >= 5000: # Threshold for bundling
                st.session_state.hamper, st.session_state.total_value = create_bundles(budget, selected_categories)
                st.session_state.is_bundle = True
                st.success(f"Created Bundles! Total Value: ₹{st.session_state.total_value:.2f}")
            else:
                st.session_state.hamper, st.session_state.total_value = create_hamper(budget, selected_categories, expiry_days)
                st.session_state.is_bundle = False
                st.success(f"Created Hamper! Total Value: ₹{st.session_state.total_value:.2f}")

# --- Main Area for Display and Feedback ---

# Check if a hamper has been created
if st.session_state.hamper:
    st.header("Generated Hamper")
    st.info(f"Total Hamper Value: **₹{st.session_state.total_value:.2f}**")

    col1, col2 = st.columns([3, 1]) # Column for items, column for feedback/replacement

    with col1:
        st.subheader("Items Included")
        if not st.session_state.is_bundle:
            # Display individual items
            for i, item_details in enumerate(st.session_state.hamper):
                if isinstance(item_details, tuple) and len(item_details) == 4:
                    name, price, expiry_date, category = item_details
                    days_left = days_until_expiry(expiry_date)
                    expiry_info = f"Expires: {expiry_date} ({days_left} days left)"
                    st.markdown(f"- **{name}** ({category}) - ₹{price:.2f} \n  <small style='color:grey;'>{expiry_info}</small>", unsafe_allow_html=True)
                else:
                     st.warning(f"Unexpected item format in hamper: {item_details}") # Debugging help
        else:
            # Display bundled items
            for i, item_details in enumerate(st.session_state.hamper):
                 if isinstance(item_details, tuple) and len(item_details) == 3:
                    name, quantity, category = item_details
                    # Fetch price for display (optional but nice)
                    item_price = categories.get(category, {}).get(name, {}).get('price', 0)
                    total_item_price = quantity * item_price
                    st.markdown(f"- **{quantity}x {name}** ({category}) - Item Price: ₹{item_price:.2f}, Total: ₹{total_item_price:.2f}")
                 else:
                     st.warning(f"Unexpected item format in bundle: {item_details}") # Debugging help


    with col2:
        # Feedback section only for non-bundle hampers
        if not st.session_state.is_bundle and st.session_state.hamper:
            st.subheader("Item Feedback")
            st.caption("Help the AI learn your preferences!")

            # Use a flag to prevent multiple replacements in one cycle
            replacement_in_progress = False
            item_to_replace_index = -1
            replacement_chosen = None

            # Collect feedback first
            feedbacks = {}
            for i, item_details in enumerate(st.session_state.hamper):
                name, price, expiry_date, category = item_details
                feedback_key = f"feedback_{i}_{name}" # More robust key
                feedbacks[i] = st.radio(
                    f"Feedback for **{name}**:",
                    ['👍 Liked', '👎 Disliked', '😐 Neutral'],
                    key=feedback_key,
                    horizontal=True,
                    index=2 # Default to Neutral
                 )


            # Process feedback and potential replacements
            for i, item_details in enumerate(st.session_state.hamper):
                 name, price, expiry_date, category = item_details
                 feedback = feedbacks[i]

                 if feedback == '👍 Liked':
                      update_policy_score(policy, category, name, 'liked')
                 elif feedback == '👎 Disliked':
                      update_policy_score(policy, category, name, 'disliked')

                      # --- Replacement Logic ---
                      if not replacement_in_progress: # Only handle one replacement at a time per run
                           st.markdown("---")
                           st.write(f"Replacing **{name}** (₹{price:.2f})")
                           remaining_budget_for_replacement = price # Can replace with item of same or lower price
                           min_expiry_date = today + timedelta(days=expiry_days)

                           # Find replacement options in the same category
                           replacement_options = []
                           if category in categories and category in policy:
                               for repl_item, repl_details in categories[category].items():
                                    repl_price = repl_details['price']
                                    repl_expiry_str = repl_details['expiry_date']
                                    repl_expiry_obj = parse_expiry_date(repl_expiry_str)

                                    if (repl_item != name and
                                        repl_price <= remaining_budget_for_replacement and
                                        repl_expiry_obj and repl_expiry_obj >= min_expiry_date):
                                         # Ensure item exists in policy
                                        if repl_item not in policy[category]:
                                             policy[category][repl_item] = 1.0

                                        repl_score = policy[category].get(repl_item, 1.0)
                                        repl_days_left = days_until_expiry(repl_expiry_str)
                                        replacement_options.append(
                                            (repl_item, repl_price, repl_expiry_str, repl_score, repl_days_left)
                                        )

                           # Sort replacements: 1st by policy (desc), 2nd by days left (desc)
                           replacement_options.sort(key=lambda x: (x[3], x[4]), reverse=True)

                           # Get the top 2-3 replacement options for user choice
                           top_replacements = replacement_options[:3]

                           if top_replacements:
                                replacement_display = [
                                    f"{r[0]} (₹{r[1]:.2f}, {r[4]} days left)" for r in top_replacements
                                ]
                                replacement_choice_key = f"replacement_{i}_{name}"

                                # Use radio to select ONE replacement
                                chosen_replacement_display = st.radio(
                                    f"Choose replacement:",
                                    options=replacement_display,
                                    key=replacement_choice_key,
                                    index=None # No default selection initially
                                )

                                # If a choice is made, find the full details and trigger rerun
                                if chosen_replacement_display:
                                    # Find the original tuple corresponding to the display string
                                    chosen_details = None
                                    for r in top_replacements:
                                        if f"{r[0]} (₹{r[1]:.2f}, {r[4]} days left)" == chosen_replacement_display:
                                            chosen_details = r
                                            break

                                    if chosen_details:
                                        # Update hamper state
                                        new_item_tuple = (chosen_details[0], chosen_details[1], chosen_details[2], category)
                                        st.session_state.hamper[i] = new_item_tuple

                                        # Update total value
                                        st.session_state.total_value = st.session_state.total_value - price + chosen_details[1]

                                        st.success(f"Replaced '{name}' with '{chosen_details[0]}'.")
                                        st.success(f"🔄 Hamper updated!", icon="✅")

                                        # Set flags to stop further replacement processing in this run
                                        replacement_in_progress = True
                                        item_to_replace_index = i
                                        replacement_chosen = chosen_details[0]

                                        # IMPORTANT: Rerun to reflect changes immediately
                                        st.rerun() # Force Streamlit to restart script with updated state

                           else:
                                st.warning(f"No suitable replacement found for {name} in {category} within budget and expiry constraints.")
                           st.markdown("---")
                      # --- End Replacement Logic ---

    # Display current policy (optional, for debugging/transparency)
    # st.sidebar.subheader("Current AI Policy")
    # st.sidebar.json(policy, expanded=False)

elif not st.session_state.hamper and 'total_value' in st.session_state:
     # Handle case where hamper creation resulted in no items
     st.warning("Could not create a hamper with the selected criteria and budget. Try adjusting the budget, categories, or expiry date.")