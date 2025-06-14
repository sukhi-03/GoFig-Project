import streamlit as st
import json
import random
from datetime import datetime, timedelta
import os
import copy # Import copy for deep copies if needed

# --- Data ---
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

POLICY_FILE = 'policy.json'
LEARNING_RATE = 0.3

# --- Helper Functions ---
def load_policy():
    """Loads policy from file or initializes a default one."""
    if os.path.exists(POLICY_FILE):
        try:
            with open(POLICY_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            st.error("Error reading policy file. Starting with default policy.")
        except Exception as e:
            st.error(f"An unexpected error occurred loading the policy: {e}")
    return {
        cat: {item: 1.0 for item in items.keys()}
        for cat, items in categories.items()
    }

def save_policy(policy_data):
    """Saves the policy data to the JSON file."""
    try:
        with open(POLICY_FILE, 'w') as f:
            json.dump(policy_data, f, indent=4)
    except Exception as e:
        st.error(f"Error saving policy file: {e}")


def parse_expiry_date(date_str):
    """Parses expiry date string into datetime object."""
    try:
        return datetime.strptime(date_str, '%d %B %Y')
    except ValueError:
        st.warning(f"Could not parse date: {date_str}. Using distant future date.")
        return datetime.now() + timedelta(days=365*10)

def days_until_expiry(expiry_date_str):
    """Calculates days remaining until expiry."""
    expiry_date = parse_expiry_date(expiry_date_str)
    return (expiry_date - datetime.now()).days

def create_hamper(budget, selected_categories, expiry_days, policy):
    """Creates a hamper based on budget, categories, expiry, and policy."""
    selected_items = []
    current_total = 0
    today = datetime.now()
    min_expiry_date = today + timedelta(days=expiry_days)

    combined_items = []
    for category in selected_categories:
        if category not in categories:
            st.warning(f"Category '{category}' not found in data. Skipping.")
            continue
        if category not in policy:
             policy[category] = {item: 1.0 for item in categories[category].keys()} # Ensure category exists in policy

        for item, details in categories[category].items():
            if item not in policy[category]:
                policy[category][item] = 1.0 # Ensure item exists in policy

            expiry_date = parse_expiry_date(details['expiry_date'])
            if expiry_date >= min_expiry_date:
                combined_items.append({
                    'name': item,
                    'price': details['price'],
                    'expiry_date': details['expiry_date'],
                    'category': category,
                    'score': policy[category].get(item, 1.0) + random.uniform(-0.1, 0.1)
                })

    combined_items = sorted(combined_items, key=lambda x: x['score'], reverse=True)

    for item_data in combined_items:
        if current_total + item_data['price'] <= budget:
            selected_items.append(item_data)
            current_total += item_data['price']

    return selected_items, current_total

def update_policy_feedback(policy_data, category, item, feedback):
    """Updates the policy based on user feedback and saves it."""
    if category not in policy_data:
        policy_data[category] = {}
    if item not in policy_data[category]:
         policy_data[category][item] = 1.0

    current_score = policy_data[category].get(item, 1.0)

    if feedback == 'liked':
        policy_data[category][item] = min(current_score + LEARNING_RATE, 5.0)
    elif feedback == 'disliked':
        policy_data[category][item] = max(0.1, current_score - LEARNING_RATE)

    save_policy(policy_data)
    return policy_data

# --- Streamlit App ---
st.set_page_config(layout="wide")
st.title("🎁 AI Powered Hamper Creation Model 🎁")

# --- Initialize Session State ---
if 'policy' not in st.session_state:
    st.session_state.policy = load_policy()
if 'hamper_items' not in st.session_state:
    st.session_state.hamper_items = []
if 'hamper_total_value' not in st.session_state:
    st.session_state.hamper_total_value = 0.0
if 'mode' not in st.session_state:
    st.session_state.mode = None # 'hamper', 'bundle', 'high_budget_choice'
if 'high_budget_choice' not in st.session_state: # Stores 'custom' or 'ready-made'
    st.session_state.high_budget_choice = None
if 'bundle_quantities' not in st.session_state:
    st.session_state.bundle_quantities = {}
if 'last_feedback' not in st.session_state:
    st.session_state.last_feedback = {}
if 'replacement_radio_state' not in st.session_state:
    st.session_state.replacement_radio_state = {}
# Add state to track the value of the high-budget choice radio to detect changes
if 'high_budget_radio_choice_value' not in st.session_state:
     st.session_state.high_budget_radio_choice_value = None

# --- Sidebar Inputs ---
st.sidebar.header("Hamper Configuration")
budget = st.sidebar.number_input("Enter your budget:", min_value=1.0, value=500.0, step=50.0, format="%.2f")
available_categories = list(categories.keys())
selected_categories = st.sidebar.multiselect(
    "Select categories:",
    options=available_categories,
    default=available_categories
)
expiry_days = st.sidebar.slider(
    "Minimum days until expiry:",
    min_value=1,
    max_value=1095,
    value=30,
    help="Only include items expiring on or after this many days from now."
)

# --- Main Logic ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Create Your Hamper / Bundle")

    # Generate Button Action
    if st.sidebar.button("✨ Generate / Configure ✨", key="generate"):
        # Reset states
        st.session_state.hamper_items = []
        st.session_state.hamper_total_value = 0.0
        st.session_state.bundle_quantities = {}
        st.session_state.last_feedback = {}
        st.session_state.replacement_radio_state = {}
        st.session_state.high_budget_choice = None
        st.session_state.mode = None
        st.session_state.high_budget_radio_choice_value = None # Reset this too

        if not selected_categories:
             st.warning("Please select at least one category.")
        elif budget <= 5000:
            st.session_state.mode = 'hamper'
            st.session_state.hamper_items, st.session_state.hamper_total_value = create_hamper(
                budget, selected_categories, expiry_days, st.session_state.policy
            )
            if not st.session_state.hamper_items:
                st.info("No items could be added with the current criteria.")
        else:
            # Budget > 5000: Prompt for choice
            st.session_state.mode = 'high_budget_choice'
            st.rerun() # Rerun to display the choice prompt

    # --- High Budget Choice Prompt ---
    if st.session_state.mode == 'high_budget_choice':
        st.subheader(f"Budget > ₹5000: Choose Your Style")

        choice = st.radio(
            "Select an option:",
            ('Create a Custom Bundle (Select Items/Quantities)', 'Generate a Ready-made Hamper (AI Suggested)'),
            key='high_budget_radio_choice',
            index=0 # WORKAROUND: Default to first option instead of None
        )

        # Check if the choice is made and *different* from the stored value, or if it's the first time
        # (This handles the initial default selection correctly)
        if choice and choice != st.session_state.high_budget_radio_choice_value:
            st.session_state.high_budget_radio_choice_value = choice # Store the chosen value

            if 'Custom Bundle' in choice:
                st.session_state.high_budget_choice = 'custom'
                st.session_state.mode = 'bundle'
                # Initialize bundle quantities
                st.session_state.bundle_quantities = {}
                for cat in selected_categories:
                     if cat in categories:
                         for item_name in categories[cat]:
                              if item_name in categories[cat]:
                                  st.session_state.bundle_quantities[item_name] = 0
                st.success("Switched to Custom Bundle mode.")

            elif 'Ready-made Hamper' in choice:
                st.session_state.high_budget_choice = 'ready-made'
                st.session_state.mode = 'hamper'
                st.session_state.hamper_items, st.session_state.hamper_total_value = create_hamper(
                    budget, selected_categories, expiry_days, st.session_state.policy
                )
                st.success("Generated a Ready-made Hamper.")
                if not st.session_state.hamper_items:
                   st.info("No items could be added for the ready-made hamper.")

            st.rerun() # Rerun to show the chosen interface
        # Also need to handle the case where the default (index 0) is selected for the first time
        elif choice and st.session_state.high_budget_radio_choice_value is None:
             st.session_state.high_budget_radio_choice_value = choice # Store the default value
             # Assume default is Custom Bundle
             st.session_state.high_budget_choice = 'custom'
             st.session_state.mode = 'bundle'
             st.session_state.bundle_quantities = {}
             for cat in selected_categories:
                  if cat in categories:
                      for item_name in categories[cat]:
                           if item_name in categories[cat]:
                               st.session_state.bundle_quantities[item_name] = 0
             st.success("Switched to Custom Bundle mode (default).")
             st.rerun()


    # --- Display Area (Hamper Mode) ---
    if st.session_state.mode == 'hamper' and st.session_state.hamper_items:
        hamper_type = "AI Generated Hamper" if st.session_state.high_budget_choice != 'ready-made' else "Ready-made Hamper"
        st.subheader(hamper_type)
        st.markdown(f"**Total Value:** ₹{st.session_state.hamper_total_value:.2f} / **Budget:** ₹{budget:.2f}")
        st.markdown("---")

        feedback_action_taken = False

        indices_to_process = list(range(len(st.session_state.hamper_items)))

        for i in indices_to_process:
             if i >= len(st.session_state.hamper_items):
                  continue

             # Use deepcopy to avoid modifying the original dict inadvertently before replacement
             item_data = copy.deepcopy(st.session_state.hamper_items[i])
             item_name = item_data['name']
             item_price = item_data['price']
             item_expiry = item_data['expiry_date']
             item_category = item_data['category']
             # Ensure keys are highly unique across potential reruns and item changes
             feedback_key = f"feedback_{item_category}_{item_name}_{i}"
             replacement_radio_key = f"replacement_radio_{item_category}_{item_name}_{i}"

             # --- Display Item ---
             st.write(f"**{i+1}. {item_name}**")
             st.write(f"   Category: {item_category}, Price: ₹{item_price:.2f}, Expires: {item_expiry} ({days_until_expiry(item_expiry)} days left)")

             # --- Feedback Selectbox ---
             current_feedback_selection = st.selectbox(
                 f"Feedback:",
                 options=['', 'liked', 'disliked'],
                 index=0, # Default to blank
                 key=feedback_key,
                 help="Provide feedback to improve future suggestions."
             )

             # --- Process Feedback Change ---
             if current_feedback_selection and current_feedback_selection != st.session_state.last_feedback.get(feedback_key):
                 st.session_state.policy = update_policy_feedback(
                     st.session_state.policy, item_category, item_name, current_feedback_selection
                 )
                 st.session_state.last_feedback[feedback_key] = current_feedback_selection
                 st.success(f"Feedback '{current_feedback_selection}' recorded for {item_name}. Policy updated.")
                 feedback_action_taken = True

                 # --- Handle Replacement Logic ---
                 if current_feedback_selection == 'disliked':
                     st.warning(f"Finding replacements for '{item_name}'...")
                     remaining_budget_for_replacement = budget - (st.session_state.hamper_total_value - item_price)

                     # --- Find Replacement Options ---
                     replacement_options = []
                     if item_category in categories:
                         for repl_item, repl_details in categories[item_category].items():
                             repl_price = repl_details['price']
                             repl_expiry = repl_details['expiry_date']
                             repl_expiry_days = days_until_expiry(repl_expiry)
                             min_req_expiry_days = expiry_days

                             if (repl_item != item_name and
                                 repl_price <= remaining_budget_for_replacement and
                                 repl_expiry_days >= min_req_expiry_days):
                                 replacement_options.append({
                                     'name': repl_item,
                                     'price': repl_price,
                                     'expiry_date': repl_expiry,
                                     'category': item_category,
                                     'score': st.session_state.policy.get(item_category, {}).get(repl_item, 1.0)
                                 })

                     replacement_options.sort(key=lambda x: (-x['score'], x['price']))
                     top_replacements = replacement_options[:3] # Limit to 3 options

                     # --- Display Replacement Radio ---
                     if top_replacements:
                         replacement_display_names = [f"{r['name']} (₹{r['price']:.2f}, Exp: {r['expiry_date']})" for r in top_replacements]

                         chosen_replacement_display_name = st.radio(
                             f"Choose a replacement for '{item_name}':",
                             options=replacement_display_names,
                             key=replacement_radio_key,
                             index=0 # Default to the first option as a workaround
                         )

                         # --- Process Radio Selection Change ---
                         last_radio_state = st.session_state.replacement_radio_state.get(replacement_radio_key)

                         if chosen_replacement_display_name and chosen_replacement_display_name != last_radio_state:
                             chosen_replacement_details = next(
                                 (r for r in top_replacements if f"{r['name']} (₹{r['price']:.2f}, Exp: {r['expiry_date']})" == chosen_replacement_display_name),
                                 None
                             )

                             if chosen_replacement_details:
                                 original_item_name = st.session_state.hamper_items[i]['name']
                                 original_item_price = st.session_state.hamper_items[i]['price']

                                 st.session_state.hamper_items[i] = chosen_replacement_details
                                 st.session_state.hamper_total_value = st.session_state.hamper_total_value - original_item_price + chosen_replacement_details['price']
                                 st.session_state.replacement_radio_state[replacement_radio_key] = chosen_replacement_display_name

                                 original_feedback_key = f"feedback_{item_category}_{original_item_name}_{i}"
                                 st.session_state.last_feedback.pop(original_feedback_key, None)
                                 original_radio_key = f"replacement_radio_{item_category}_{original_item_name}_{i}"
                                 st.session_state.replacement_radio_state.pop(original_radio_key, None)

                                 st.success(f"Replaced '{original_item_name}' with '{chosen_replacement_details['name']}'.")
                                 st.rerun()

                             else:
                                  st.error("Error: Could not find details for the selected replacement.")

                         elif chosen_replacement_display_name and last_radio_state is None:
                              st.session_state.replacement_radio_state[replacement_radio_key] = chosen_replacement_display_name


                     else: # No replacements found
                         st.info(f"No suitable replacement found for '{item_name}' in '{item_category}'. Item remains disliked.")
                         st.session_state.replacement_radio_state.pop(replacement_radio_key, None)


                 elif current_feedback_selection == 'liked':
                      st.session_state.replacement_radio_state.pop(replacement_radio_key, None)


             is_last_item = (i == len(indices_to_process) - 1)
             if not is_last_item or st.session_state.last_feedback.get(feedback_key) == 'disliked':
                 st.markdown("---")


    # --- Display Area (Bundle Mode) ---
    elif st.session_state.mode == 'bundle':
        st.subheader("Build Your Custom Bundle")
        st.markdown(f"**Budget:** ₹{budget:.2f}")
        st.markdown("---")

        available_bundle_items = {}
        for cat in selected_categories:
            if cat in categories:
                for item_name, details in categories[cat].items():
                     if item_name not in available_bundle_items:
                         available_bundle_items[item_name] = {**details, 'category': cat}

        sorted_item_names = sorted(available_bundle_items.keys())
        bundle_cols = st.columns(2)
        col_idx = 0
        quantity_changed = False

        for item_name in sorted_item_names:
            details = available_bundle_items[item_name]
            item_price = details['price']
            item_category = details['category']
            item_expiry = details['expiry_date']
            item_key = f"bundle_qty_{item_name}"

            with bundle_cols[col_idx % 2]:
                 st.markdown(f"**{item_name}**")
                 st.caption(f"Category: {item_category} | Price: ₹{item_price:.2f} | Expires: {item_expiry}")

                 current_quantity = st.session_state.bundle_quantities.get(item_name, 0)
                 quantity = st.number_input(
                     f"Qty:",
                     min_value=0,
                     value=current_quantity,
                     step=1,
                     key=item_key,
                     label_visibility="collapsed"
                 )

                 if quantity != current_quantity:
                     st.session_state.bundle_quantities[item_name] = quantity
                     quantity_changed = True

                 st.markdown("---")
            col_idx += 1

        bundle_summary_items = []
        final_bundle_cost = 0.0
        for item_name, quantity in st.session_state.bundle_quantities.items():
             if quantity > 0 and item_name in available_bundle_items:
                 details = available_bundle_items[item_name]
                 item_price = details['price']
                 final_bundle_cost += quantity * item_price
                 bundle_summary_items.append({
                     'name': item_name, 'price': item_price, 'quantity': quantity,
                     'category': details['category'], 'expiry_date': details['expiry_date']
                 })

        st.session_state.hamper_items = bundle_summary_items
        st.session_state.hamper_total_value = final_bundle_cost

        st.sidebar.subheader("Bundle Summary")
        remaining_budget = budget - final_bundle_cost
        if final_bundle_cost > budget:
            st.sidebar.error(f"⚠️ Cost Exceeds Budget by ₹{abs(remaining_budget):.2f}!")
        elif final_bundle_cost == 0 and st.session_state.high_budget_choice == 'custom':
             st.sidebar.info("Add items to your custom bundle.")
        else:
            delta_color = "inverse" if remaining_budget < 0 else "normal"
            st.sidebar.metric("Current Bundle Cost", f"₹{final_bundle_cost:.2f}", f"₹{remaining_budget:.2f} Remaining", delta_color=delta_color)

        if bundle_summary_items:
             st.sidebar.markdown("**Items in Bundle:**")
             for item in bundle_summary_items:
                 st.sidebar.write(f"- {item['quantity']} x {item['name']} (₹{item['price']:.2f} ea)")

        if quantity_changed:
            st.rerun()


# --- Right Column (Policy Display) ---
with col2:
    st.header("Learned Preferences (Policy)")
    st.write("Higher scores mean the AI prefers suggesting this item (used for ready-made hampers).")
    with st.expander("Show Current Policy Scores", expanded=False):
        policy_to_display = st.session_state.get('policy', {})
        if policy_to_display:
            sorted_policy = {
                cat: dict(sorted(items.items()))
                for cat, items in sorted(policy_to_display.items())
            }
            st.json(sorted_policy, expanded=False)
        else:
            st.write("Policy not loaded yet.")

    st.info("💡 Feedback on 'Ready-made Hampers' (liked/disliked) updates these scores.")