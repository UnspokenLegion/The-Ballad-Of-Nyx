inventory = ["sword", "shield", "potion", "potion", "sword", "bow", "arrow", "arrow"]
def unique_items(inventory):
    if not inventory:
        print("Your inventory is empty!")
        return []
    unique_items = list(set(inventory))
    print(f"Unique items in inventory: {unique_items}")
    return unique_items

# The player's current stash of items
inventory = {
    "herbs": 3,      # Enough for 1 health potion
    "ginsing": 1,    # Not enough for a mana potion
    "fungi": 2,      
    "health_potion": 0,
    "mana_potion": 0,
    "strength_elixir": 0
}

# The blueprints for crafting
recipes = {
    "health_potion": {"herbs": 2},           # Combines 2 herbs
    "mana_potion": {"ginsing": 2},           # Combines 2 ginsing
    "strength_elixir": {"fungi": 2},         # Combines 2 fungi
    "rejuvenation_flask": {"herbs": 1, "ginsing": 1} # Combines two different items
}

def crafting_system():
    while True:
        print("\n--- Crafting System ---")
        print("Available items to craft:")
        
        # Only show items that have a defined recipe
        for crafted_item, ingredients in recipes.items():
            # Format the ingredients for display (e.g., "2x Herbs")
            reqs = ", ".join([f"{count}x {ing.title()}" for ing, count in ingredients.items()])
            print(f"- {crafted_item.replace('_', ' ').title()} (Requires: {reqs})")
            
        print("\nYour Inventory:")
        for item, count in inventory.items():
            if count > 0:
                 print(f"{item.title()}: {count}")

        choice = input("\nEnter the name of the item you want to craft (or type 'cancel' to go back): ").lower().replace(' ', '_')
        
        if choice == 'cancel':
            print("Exiting crafting menu.")
            break
            
        if choice in recipes:
            can_craft = True
            recipe = recipes[choice]
            
            # 1. Check if the player has enough of each required ingredient
            for ingredient, required_amount in recipe.items():
                if inventory.get(ingredient, 0) < required_amount:
                    can_craft = False
                    print(f"\nYou don't have enough {ingredient.title()}! You need {required_amount}.")
                    break # Stop checking if we are missing an ingredient
            
            # 2. If they have the ingredients, process the crafting
            if can_craft:
                # Remove ingredients from inventory
                for ingredient, required_amount in recipe.items():
                    inventory[ingredient] -= required_amount
                
                # Add the new item to inventory
                inventory[choice] = inventory.get(choice, 0) + 1
                print(f"\nSuccess! You crafted a {choice.replace('_', ' ').title()}!")
        else:
            print("\nInvalid item. Please choose a valid recipe.")