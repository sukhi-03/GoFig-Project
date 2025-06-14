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
                        p[cat][item] = 1.0 # Initialize new items with default score
            return p
    except (FileNotFoundError, json.JSONDecodeError):
        st.warning(f"Policy file '{POLICY_FILE}' not found or invalid. Initializing new policy.")
        return {
            cat: {item: 1.0 for item in items.keys()}
            for cat, items in categories.items()
        }

def save_policy(policy_data):
    """Saves the policy data to the JSON file."""
    try:
        with open(POLICY_FILE, 'w') as f:
            json.dump(policy_data, f, indent=4) # Use indent for readability
    except IOError as e:
        st.error(f"Error saving policy file: {e}")

policy = load_policy()
today = datetime.now()

def parse_expiry_date(date_str):
    """Parses expiry date string into datetime object."""
    try:
        return datetime.strptime(date_str, '%d %B %Y')
    except (ValueError, TypeError):
        st.error(f"Error parsing date: '{date_str}'. Expected format 'DD Month YYYY'.")
        return None

def days_until_expiry(expiry_date_str):
    """Calculates days between today and expiry date."""
    expiry_date = parse_expiry_date(expiry_date_str)
    if expiry_date:
        return (expiry_date.date() - today.date()).days
    return -9999 # Indicate error or invalid date

# --- Hamper Creation Logic ---

def create_hamper(budget, selected_categories, expiry_days):
    """Creates a hamper with individual items based on policy and constraints."""
    selected_items = []
    current_total = 0
    min_expiry_days = max(0, expiry_days)
    min_expiry_date = today + timedelta(days=min_expiry_days)
    combined_items = []

    for category in selected_categories:
        if category in categories and category in policy:
            for item, details in categories[category].items():
                if 'price' in details and 'expiry_date' in details and details['price'] > 0:
                    price = details['price']
                    expiry_date_str = details['expiry_date']
                    expiry_date_obj = parse_expiry_date(expiry_date_str)

                    if item not in policy[category]:
                         policy[category][item] = 1.0

                    if expiry_date_obj and expiry_date_obj >= min_expiry_date:
                        score = policy[category].get(item, 1.0) + random.uniform(-0.2, 0.2) # Reduced randomness
                        combined_items.append((item, price, expiry_date_str, category, score))

    combined_items = sorted(combined_items, key=lambda x: x[4], reverse=True)

    for item, price, expiry_date, category, _ in combined_items:
        if current_total + price <= budget:
            selected_items.append((item, price, expiry_date, category))
            current_total += price

    return selected_items, current_total

def create_bundles(budget, selected_categories):
    """Creates bundles of items, prioritizing by policy score."""
    bundles = []
    remaining_budget = budget
    all_items_with_policy = []

    for category in selected_categories:
        if category in categories and category in policy:
            for item, details in categories[category].items():
                if 'price' in details and details['price'] > 0:
                    item_price = details['price']
                    if item not in policy[category]:
                        policy[category][item] = 1.0
                    policy_score = policy[category].get(item, 1.0)
                    all_items_with_policy.append(
                        {'name': item, 'price': item_price, 'category': category, 'policy': policy_score}
                    )

    all_items_with_policy.sort(key=lambda x: x['policy'], reverse=True)

    min_affordable_price = float('inf')
    for item_data in all_items_with_policy:
         if item_data['price'] > 0:
              min_affordable_price = min(min_affordable_price, item_data['price'])

    for item_data in all_items_with_policy:
        item_name = item_data['name']
        item_price = item_data['price']
        category = item_data['category']

        if remaining_budget >= item_price:
            max_quantity = int(remaining_budget // item_price)
            if max_quantity > 0:
                bundles.append((item_name, max_quantity, category))
                remaining_budget -= max_quantity * item_price

        # Optimization: Stop if remaining budget can't afford the cheapest item
        if remaining_budget < min_affordable_price and min_affordable_price != float('inf'):
            break
        if remaining_budget <= 0:
             break

    total_spent = budget - remaining_budget
    return bundles, total_spent

# --- Policy Update Logic ---

def update_policy_score(policy_ref, category, item, feedback, learning_rate=0.3):
    """Updates the policy score for a given item based on feedback and saves the policy."""
    policy_changed = False
    if category in policy_ref and item in policy_ref[category]:
        current_score = policy_ref[category][item]
        new_score = current_score

        if feedback == 'liked':
            new_score = current_score + learning_rate
            st.toast(f"👍 Increased score for {item}", icon="📈")
        elif feedback == 'disliked':
            new_score = max(0.1, current_score - learning_rate) # Ensure score doesn't drop below 0.1
            st.toast(f"👎 Decreased score for {item}", icon="📉")

        if new_score != current_score:
             policy_ref[category][item] = new_score
             policy_changed = True
    else:
         st.warning(f"Could not update policy for '{item}' in '{category}' (not found).")

    if policy_changed:
        save_policy(policy_ref)


# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🎁 AI Powered Hamper Creation Model 🎁")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("Hamper Configuration")
    budget = st.number_input("Enter your budget:", min_value=1.0, value=1000.0, step=50.0, format="%.2f")
    available_categories = list(categories.keys())
    default_selection = [cat for cat in available_categories if cat in categories]
    selected_categories = st.multiselect(
        "Select categories:", options=available_categories, default=default_selection
    )
    expiry_days = st.slider(
        "Minimum days until expiry:", min_value=1, max_value=730, value=60,
        help="Include items expiring on or after this many days from today."
    )

    st.session_state.setdefault('hamper', [])
    st.session_state.setdefault('total_value', 0.0)
    st.session_state.setdefault('is_bundle', False)
    # Initialize state for feedback widgets if they don't exist
    st.session_state.setdefault('feedback_state', {})


    if st.button("✨ Create/Refresh Hamper ✨", type="primary", use_container_width=True):
        if not selected_categories:
            st.warning("Please select at least one category.")
        elif budget <= 0:
             st.warning("Please enter a budget greater than zero.")
        else:
            if budget >= 5000:
                hamper_items, total_val = create_bundles(budget, selected_categories)
                st.session_state.is_bundle = True
                action_text = "Created Bundles"
            else:
                hamper_items, total_val = create_hamper(budget, selected_categories, expiry_days)
                st.session_state.is_bundle = False
                action_text = "Created Hamper"

            st.session_state.hamper = hamper_items
            st.session_state.total_value = total_val
            # Reset feedback state when new hamper is created
            st.session_state.feedback_state = {}

            if not hamper_items:
                 st.toast("Could not find items matching criteria.", icon="😕")
            else:
                 st.toast(f"{action_text}! Total Value: ₹{st.session_state.total_value:.2f}", icon="🎉")


# --- Main Area for Display and Feedback ---
if st.session_state.hamper:
    st.header("Generated Hamper")
    st.metric(label="Total Hamper Value", value=f"₹{st.session_state.total_value:.2f}")
    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Items Included")
        if not st.session_state.is_bundle:
            # Display Individual Items
            for i, item_details in enumerate(st.session_state.hamper):
                if isinstance(item_details, tuple) and len(item_details) == 4:
                    name, price, expiry_date, category = item_details
                    days_left = days_until_expiry(expiry_date)
                    expiry_info = f"Expires: {expiry_date}"
                    if days_left != -9999: expiry_info += f" ({days_left} days left)"
                    else: expiry_info += " (Invalid Date)"
                    st.markdown(f"- **{name}** ({category}) - ₹{price:.2f} \n  <small style='color:grey;'>{expiry_info}</small>", unsafe_allow_html=True)
                else: st.warning(f"Skipping display: Unexpected item format {item_details}")
        else:
            # Display Bundled Items
            for i, item_details in enumerate(st.session_state.hamper):
                 if isinstance(item_details, tuple) and len(item_details) == 3:
                    name, quantity, category = item_details
                    item_price = categories.get(category, {}).get(name, {}).get('price', 0)
                    total_item_price = quantity * item_price
                    st.markdown(f"- **{quantity}x {name}** ({category}) - Item Price: ₹{item_price:.2f}, Total: ₹{total_item_price:.2f}")
                 else: st.warning(f"Skipping display: Unexpected bundle format {item_details}")

    with col2:
        # Feedback and Replacement Section (Only for non-bundle hampers)
        if not st.session_state.is_bundle and st.session_state.hamper:
            st.subheader("Item Feedback")
            st.caption("Help the AI learn your preferences!")

            replacement_active_key = f"replacement_active_{random.random()}" # Unique key per run
            st.session_state.setdefault(replacement_active_key, False)

            # Store feedback choices temporarily during the run
            current_run_feedback = {}

            for i, item_details in enumerate(st.session_state.hamper):
                if not (isinstance(item_details, tuple) and len(item_details) == 4): continue
                name, price, expiry_date, category = item_details
                feedback_key = f"feedback_{i}_{name}_{category}"

                st.markdown("---")
                fb_col1, fb_col2 = st.columns([3, 1])
                with fb_col1:
                     st.write(f"Feedback for **{name}**:")
                with fb_col2:
                    # *** CORRECTED LINE ***
                    # Provide the default index (2 for Neutral). Streamlit uses the
                    # value stored under `key` if the user has interacted.
                    feedback = st.radio(
                        f"fb_{i}", # Use a minimal label as item name is above
                        options=['👍 Liked', '👎 Disliked', '😐 Neutral'],
                        key=feedback_key, # Key for state persistence
                        horizontal=True,
                        index=2, # Default visual state is Neutral (index 2)
                        label_visibility="collapsed"
                    )
                    current_run_feedback[i] = feedback # Store choice for processing below

            # --- Process Feedback and Replacements AFTER rendering all radio buttons ---
            replacement_triggered_this_run = False
            for i, item_details in enumerate(st.session_state.hamper):
                 if i not in current_run_feedback: continue # Skip if feedback wasn't rendered
                 if replacement_triggered_this_run: break # Only handle one replacement per run

                 feedback = current_run_feedback[i]
                 name, price, expiry_date, category = item_details # Unpack again

                 # Process policy update first
                 if feedback == '👍 Liked':
                     update_policy_score(policy, category, name, 'liked')
                 elif feedback == '👎 Disliked':
                     update_policy_score(policy, category, name, 'disliked')

                     # --- Replacement Logic for Disliked Item ---
                     if not st.session_state[replacement_active_key]:
                         st.session_state[replacement_active_key] = True # Mark replacement UI active
                         replacement_triggered_this_run = True # Prevent multiple replacements

                         st.write(f"🔄 Find replacement for **{name}** (₹{price:.2f})")
                         max_replacement_price = price
                         min_expiry_date_for_replacement = today + timedelta(days=expiry_days)
                         replacement_options = []

                         if category in categories and category in policy:
                             for repl_item, repl_details in categories[category].items():
                                 if 'price' in repl_details and 'expiry_date' in repl_details:
                                     repl_price = repl_details['price']
                                     repl_expiry_str = repl_details['expiry_date']
                                     repl_expiry_obj = parse_expiry_date(repl_expiry_str)
                                     if (repl_item != name and repl_price > 0 and
                                         repl_price <= max_replacement_price and
                                         repl_expiry_obj and repl_expiry_obj >= min_expiry_date_for_replacement):
                                         if repl_item not in policy[category]: policy[category][repl_item] = 1.0
                                         repl_score = policy[category].get(repl_item, 1.0)
                                         repl_days_left = days_until_expiry(repl_expiry_str)
                                         if repl_days_left != -9999:
                                             replacement_options.append(
                                                 (repl_item, repl_price, repl_expiry_str, repl_score, repl_days_left)
                                             )

                         replacement_options.sort(key=lambda x: (x[3], x[4]), reverse=True)
                         top_replacements = replacement_options[:3]

                         if top_replacements:
                             replacement_map = {f"{r[0]} (₹{r[1]:.2f}, {r[4]} days)": r for r in top_replacements}
                             replacement_display_options = list(replacement_map.keys())
                             replacement_choice_key = f"replacement_{i}_{name}"
                             chosen_replacement_display = st.radio(
                                 f"Select replacement:", options=replacement_display_options,
                                 key=replacement_choice_key, index=None
                             )

                             if chosen_replacement_display:
                                 chosen_details = replacement_map[chosen_replacement_display]
                                 new_item_tuple = (chosen_details[0], chosen_details[1], chosen_details[2], category)
                                 original_hamper = st.session_state.hamper
                                 original_hamper[i] = new_item_tuple
                                 st.session_state.hamper = original_hamper
                                 st.session_state.total_value = st.session_state.total_value - price + chosen_details[1]

                                 st.success(f"Replaced '{name}' with '{chosen_details[0]}'.")
                                 st.toast(f"🔄 Hamper updated!", icon="✅")
                                 # Reset the feedback state for the *next* run visually
                                 # st.session_state[feedback_key] = 2 # This might reset too early before rerun
                                 # Instead, clear the general feedback state on new hamper creation

                                 del st.session_state[replacement_active_key] # Reset flag
                                 st.rerun() # Rerun immediately
                         else:
                             st.warning(f"No suitable replacement found for {name}.")
                             del st.session_state[replacement_active_key] # Reset flag

            # Clean up the replacement flag if it wasn't deleted by a rerun
            if replacement_active_key in st.session_state:
                 try: del st.session_state[replacement_active_key]
                 except KeyError: pass


#elif not st.session_state.hamper and 'total_value' in st.session_state:
#    # Optional: Message if hamper creation attempt resulted in empty list
#    pass # Toast message already handles this after button click