import random
import time

class Player:
    def __init__(self, username):
        self.username = username
        self.clean_balance = 10000
        self.dirty_balance = 0
        self.stocks = 0
        self.stock_price = 100
        self.real_estate = 0
        self.passive_income = 0
        self.in_jail = False
        self.turns_in_jail = 0
        self.bribe_cost = 5000
        
        # NEW FEATURES
        self.respect = 50  # 0-100 scale
        self.fear = 0      # 0-100 scale
        self.contacts = {}  # {"lawyer": level, "corrupt_cop": level, etc.}
        self.loans = {}    # {"shark_name": amount_owed}
        self.total_debt = 0
        self.unlocked_crimes = ["petty_theft", "drug_deal"]
        self.real_estate_value = 50000  # market value of properties
        self.days_played = 0
        self.heat_level = 0  # police attention 0-100

    def status(self):
        print(f"\n🏴‍☠️ === {self.username}'s Criminal Empire === 🏴‍☠️")
        print(f"💰 Clean Money: ${self.clean_balance:,.2f}")
        print(f"💸 Dirty Money: ${self.dirty_balance:,.2f}")
        print(f"📈 Stocks: {self.stocks} shares @ ${self.stock_price:.2f}")
        print(f"🏠 Real Estate: {self.real_estate} units (Value: ${self.real_estate_value:,})")
        print(f"💵 Passive Income: ${self.passive_income}/turn")
        if self.total_debt > 0:
            print(f"💀 Total Debt: ${self.total_debt:,.2f}")
        print(f"⚡ Respect: {self.respect}/100 | 😨 Fear: {self.fear}/100")
        print(f"🚨 Heat Level: {self.heat_level}/100")
        if self.in_jail:
            print(f"🚔 JAILED for {self.turns_in_jail} more turns")
        if self.contacts:
            print(f"📞 Contacts: {list(self.contacts.keys())}")
        print(f"🔓 Available Crimes: {self.unlocked_crimes}")
        print("=" * 50)

class GameEvents:
    @staticmethod
    def trigger_random_event(player):
        if random.random() < 0.15:  # 15% chance each turn
            events = [
                GameEvents.police_raid,
                GameEvents.stock_crash,
                GameEvents.cartel_war,
                GameEvents.real_estate_boom,
                GameEvents.betrayal,
                GameEvents.opportunity,
                GameEvents.loan_shark_visit
            ]
            event = random.choice(events)
            event(player)
            return True
        return False

    @staticmethod
    def police_raid(player):
        print("\n🚨🚨 POLICE RAID! 🚨🚨")
        loss = min(player.dirty_balance, random.randint(5000, 20000))
        player.dirty_balance -= loss
        player.heat_level += 20
        print(f"Police seized ${loss} in dirty money! Heat level increased.")
        if player.dirty_balance < 0:
            player.dirty_balance = 0

    @staticmethod
    def stock_crash(player):
        print("\n📉 STOCK MARKET CRASH!")
        crash = random.uniform(0.3, 0.7)
        player.stock_price *= crash
        print(f"All stocks crashed {(1-crash)*100:.0f}%! New price: ${player.stock_price:.2f}")

    @staticmethod
    def cartel_war(player):
        print("\n💥 CARTEL WAR ERUPTED!")
        player.real_estate_value *= random.uniform(0.7, 0.9)
        player.stock_price *= random.uniform(0.8, 1.1)
        player.heat_level += 15
        print("Real estate values dropping, markets unstable, heat rising!")

    @staticmethod
    def real_estate_boom(player):
        print("\n🏘️ REAL ESTATE BOOM!")
        player.real_estate_value *= random.uniform(1.2, 1.5)
        player.passive_income += player.real_estate * 100
        print("Property values soaring! Passive income increased!")

    @staticmethod
    def betrayal(player):
        if player.respect < 30 and player.contacts:
            print("\n🗡️ BETRAYED BY LOW RESPECT!")
            contact = random.choice(list(player.contacts.keys()))
            del player.contacts[contact]
            loss = random.randint(5000, 15000)
            player.clean_balance -= loss
            player.heat_level += 25
            print(f"{contact} sold you out! Lost ${loss} and gained heat.")

    @staticmethod
    def opportunity(player):
        print("\n✨ SPECIAL OPPORTUNITY!")
        opportunities = [
            "A corrupt politician wants a bribe for future favors",
            "Black market weapons dealer needs funding",
            "Underground casino needs investors"
        ]
        print(random.choice(opportunities))
        if player.clean_balance >= 10000:
            choice = input("Invest $10,000? (y/n): ").lower()
            if choice == 'y':
                player.clean_balance -= 10000
                if random.random() < 0.7:
                    gain = random.randint(15000, 30000)
                    player.dirty_balance += gain
                    print(f"Success! Gained ${gain} dirty money!")
                else:
                    print("Investment failed. Money lost.")

    @staticmethod
    def loan_shark_visit(player):
        if player.total_debt > 0:
            print("\n🦈 LOAN SHARK VISIT!")
            interest = int(player.total_debt * 0.1)
            player.total_debt += interest
            print(f"Debt increased by ${interest} interest. Total debt: ${player.total_debt}")

def simulate_stock_price(current_price):
    change_percent = random.uniform(-0.15, 0.15)
    return round(current_price * (1 + change_percent), 2)

def unlock_new_crimes(player):
    all_crimes = {
        "bank_heist": {"respect_needed": 60, "description": "High-risk bank robbery"},
        "kidnapping": {"respect_needed": 70, "description": "Kidnap for ransom"},
        "arms_dealing": {"respect_needed": 80, "description": "Sell illegal weapons"},
        "assassination": {"respect_needed": 90, "description": "Contract killing"}
    }
    
    for crime, requirements in all_crimes.items():
        if crime not in player.unlocked_crimes and player.respect >= requirements["respect_needed"]:
            player.unlocked_crimes.append(crime)
            print(f"🔓 NEW CRIME UNLOCKED: {crime} - {requirements['description']}")

def commit_crime(player):
    if player.in_jail:
        print("You're in jail. Can't commit crimes.")
        return

    print("\nAvailable crimes:")
    for i, crime in enumerate(player.unlocked_crimes, 1):
        print(f"{i}. {crime.replace('_', ' ').title()}")
    
    try:
        choice = int(input("Choose crime (number): ")) - 1
        if choice < 0 or choice >= len(player.unlocked_crimes):
            print("Invalid choice.")
            return
        
        crime_type = player.unlocked_crimes[choice]
        execute_crime(player, crime_type)
    except ValueError:
        print("Enter a number.")

def execute_crime(player, crime_type):
    crime_data = {
        "petty_theft": {"risk": 0.2, "reward": (500, 2000), "jail_time": (1, 2)},
        "drug_deal": {"risk": 0.3, "reward": (2000, 8000), "jail_time": (2, 4)},
        "bank_heist": {"risk": 0.5, "reward": (20000, 50000), "jail_time": (5, 10)},
        "kidnapping": {"risk": 0.4, "reward": (15000, 40000), "jail_time": (4, 8)},
        "arms_dealing": {"risk": 0.3, "reward": (10000, 25000), "jail_time": (3, 6)},
        "assassination": {"risk": 0.6, "reward": (30000, 80000), "jail_time": (7, 15)}
    }
    
    data = crime_data[crime_type]
    base_risk = data["risk"]
    
    # Modify risk based on contacts and heat
    risk_modifier = 1.0
    if "corrupt_cop" in player.contacts:
        risk_modifier -= 0.1 * player.contacts["corrupt_cop"]
    if "fixer" in player.contacts:
        risk_modifier -= 0.05 * player.contacts["fixer"]
    
    risk_modifier += player.heat_level / 200  # Higher heat = more risk
    actual_risk = min(0.9, base_risk * risk_modifier)
    
    print(f"Attempting {crime_type.replace('_', ' ')}...")
    
    if random.random() < actual_risk:  # Caught
        jail_time = random.randint(*data["jail_time"])
        if "lawyer" in player.contacts:
            jail_time = max(1, jail_time - player.contacts["lawyer"])
        
        player.in_jail = True
        player.turns_in_jail = jail_time
        player.heat_level += 20
        print(f"🚔 BUSTED! Sentenced to {jail_time} turns. Heat increased.")
        
        # Lose respect for getting caught
        player.respect -= 5
        
    else:  # Success
        reward = random.randint(*data["reward"])
        player.dirty_balance += reward
        player.respect += 3
        player.fear += 2
        player.heat_level += 5
        print(f"💰 Success! Earned ${reward} dirty money. Respect and fear increased!")

def manage_contacts(player):
    print("\n📞 === CONTACT MANAGEMENT === 📞")
    available_contacts = {
        "lawyer": {"cost": 15000, "max_level": 3, "description": "Reduces jail time"},
        "corrupt_cop": {"cost": 20000, "max_level": 3, "description": "Reduces crime risk"},
        "fixer": {"cost": 25000, "max_level": 2, "description": "Reduces risk, better laundering"},
        "politician": {"cost": 50000, "max_level": 2, "description": "Reduces heat buildup"},
        "arms_dealer": {"cost": 30000, "max_level": 2, "description": "Better crime rewards"}
    }
    
    print("Your contacts:")
    for contact, level in player.contacts.items():
        print(f"  {contact}: Level {level}")
    
    print("\nAvailable to recruit/upgrade:")
    for contact, data in available_contacts.items():
        current_level = player.contacts.get(contact, 0)
        if current_level < data["max_level"]:
            cost = data["cost"] * (current_level + 1)
            print(f"  {contact} (Level {current_level + 1}): ${cost} - {data['description']}")
    
    contact_name = input("\nWho do you want to recruit/upgrade? (or 'back'): ").lower()
    if contact_name == 'back':
        return
    
    if contact_name in available_contacts:
        current_level = player.contacts.get(contact_name, 0)
        if current_level >= available_contacts[contact_name]["max_level"]:
            print("Contact already at max level.")
            return
        
        cost = available_contacts[contact_name]["cost"] * (current_level + 1)
        if player.clean_balance >= cost:
            player.clean_balance -= cost
            player.contacts[contact_name] = current_level + 1
            print(f"✅ {contact_name} recruited/upgraded to level {current_level + 1}!")
        else:
            print("Not enough clean money.")
    else:
        print("Invalid contact name.")

def loan_sharks(player):
    print("\n🦈 === LOAN SHARKS === 🦈")
    print("Available loans:")
    print("1. Borrow $50,000 (30% interest per turn)")
    print("2. Borrow $100,000 (25% interest per turn)")
    print("3. Borrow $200,000 (20% interest per turn)")
    print("4. Pay back debt")
    print("5. Back")
    
    choice = input("Choose option: ")
    
    if choice == "1":
        loan_amount = 50000
        interest_rate = 0.3
    elif choice == "2":
        loan_amount = 100000
        interest_rate = 0.25
    elif choice == "3":
        loan_amount = 200000
        interest_rate = 0.2
    elif choice == "4":
        if player.total_debt > 0:
            if player.clean_balance >= player.total_debt:
                player.clean_balance -= player.total_debt
                print(f"Paid off ${player.total_debt} debt!")
                player.total_debt = 0
                player.loans = {}
            else:
                print(f"You need ${player.total_debt} but only have ${player.clean_balance}")
        else:
            print("You have no debt.")
        return
    elif choice == "5":
        return
    else:
        print("Invalid choice.")
        return
    
    # Take loan
    shark_name = random.choice(["Vinny", "Big Tony", "The Cleaner", "Mad Dog"])
    player.loans[shark_name] = {"amount": loan_amount, "interest": interest_rate}
    player.total_debt += loan_amount
    player.dirty_balance += loan_amount
    print(f"💰 {shark_name} lent you ${loan_amount}. Pay back with {interest_rate*100}% interest!")

def launder_money(player):
    if player.in_jail:
        print("Can't launder from jail.")
        return

    if player.dirty_balance == 0:
        print("No dirty money to launder.")
        return

    print("Laundering methods:")
    print("1. Casino (70% success, 60% conversion)")
    print("2. Shell company (80% success, 50% conversion)")
    print("3. Crypto exchange (60% success, 80% conversion)")
    
    choice = input("Choose method: ")
    
    success_rates = {"1": 0.7, "2": 0.8, "3": 0.6}
    conversion_rates = {"1": 0.6, "2": 0.5, "3": 0.8}
    
    if choice not in success_rates:
        print("Invalid choice.")
        return
    
    success_rate = success_rates[choice]
    conversion_rate = conversion_rates[choice]
    
    # Contacts improve laundering
    if "fixer" in player.contacts:
        success_rate += 0.1 * player.contacts["fixer"]
    
    if random.random() < success_rate:
        amount = int(player.dirty_balance * conversion_rate)
        player.clean_balance += amount
        player.dirty_balance -= int(player.dirty_balance * 0.7)  # Some money always lost
        print(f"✅ Successfully laundered ${amount}!")
    else:
        loss = int(player.dirty_balance * 0.4)
        player.dirty_balance -= loss
        if random.random() < 0.3:  # Chance of getting caught
            player.in_jail = True
            player.turns_in_jail = random.randint(2, 5)
            print(f"💥 Laundering failed! Lost ${loss} and got jailed for {player.turns_in_jail} turns!")
        else:
            print(f"❌ Laundering failed. Lost ${loss}.")

def next_turn(player):
    player.days_played += 1
    
    if player.in_jail:
        player.turns_in_jail -= 1
        print(f"🔒 Day {player.days_played}: In jail... {player.turns_in_jail} turns left.")
        if player.turns_in_jail <= 0:
            player.in_jail = False
            player.heat_level = max(0, player.heat_level - 10)
            print("🔓 Released from jail. Heat decreased.")
        return

    # Collect passive income
    player.clean_balance += player.passive_income
    
    # Update stock price
    player.stock_price = simulate_stock_price(player.stock_price)
    
    # Handle debt interest
    total_interest = 0
    for shark, loan_data in player.loans.items():
        interest = int(loan_data["amount"] * loan_data["interest"])
        total_interest += interest
        loan_data["amount"] += interest
    
    if total_interest > 0:
        player.total_debt += total_interest
        print(f"💀 Loan shark interest: ${total_interest}. Total debt: ${player.total_debt}")
    
    # Reduce heat over time
    player.heat_level = max(0, player.heat_level - 2)
    
    # Check for random events
    GameEvents.trigger_random_event(player)
    
    # Check for new crime unlocks
    unlock_new_crimes(player)
    
    # Debt collection threat
    if player.total_debt > 100000:
        print("🦈 Loan sharks are getting impatient. Pay up or face consequences!")
        if random.random() < 0.3:
            damage = random.randint(5000, 15000)
            player.clean_balance -= damage
            player.respect -= 10
            print(f"💥 Loan sharks sent a message. Lost ${damage} and respect!")

def bribe(player):
    if not player.in_jail:
        print("You're not in jail.")
        return
    
    base_cost = player.bribe_cost
    # Politicians reduce bribe costs
    if "politician" in player.contacts:
        base_cost = int(base_cost * (0.8 ** player.contacts["politician"]))
    
    if player.clean_balance >= base_cost:
        player.clean_balance -= base_cost
        player.in_jail = False
        player.turns_in_jail = 0
        player.bribe_cost *= 1.5  # Bribes get more expensive
        print(f"💵 Bribed your way out for ${base_cost}!")
    else:
        print(f"Need ${base_cost} for bribe.")

def main():
    print("🏴‍☠️" + "=" * 50 + "🏴‍☠️")
    print("    WELCOME TO CRIMINAL EMPIRE: ULTIMATE EDITION")
    print("🏴‍☠️" + "=" * 50 + "🏴‍☠️")
    username = input("Enter your criminal alias: ")
    player = Player(username)
    print(f"\nWelcome to the underworld, {username}. Time to build your empire... or die trying.\n")

    COMMANDS = """
📋 === AVAILABLE COMMANDS === 📋
status      : View your criminal empire
buy stock   : Buy legitimate stocks
sell stock  : Sell your stocks
invest      : Buy real estate ($5000)
crime       : Commit crimes for dirty money
launder     : Clean your dirty money
contacts    : Manage your criminal contacts
loans       : Deal with loan sharks
bribe       : Bribe your way out of jail
wait        : Pass time (advance game)
help        : Show this menu
quit        : Exit the game
"""
    print(COMMANDS)

    while True:
        cmd = input("🎮 > ").strip().lower()

        if cmd == "status":
            player.status()

        elif cmd == "buy stock":
            if player.in_jail:
                print("Can't trade stocks from jail.")
                continue
            try:
                count = int(input(f"Stocks to buy @ ${player.stock_price:.2f} each: "))
                cost = count * player.stock_price
                if count <= 0:
                    print("Positive numbers only.")
                elif cost > player.clean_balance:
                    print("Insufficient clean money.")
                else:
                    player.stocks += count
                    player.clean_balance -= cost
                    print(f"📈 Bought {count} stocks for ${cost:.2f}")
            except ValueError:
                print("Enter a valid number.")

        elif cmd == "sell stock":
            try:
                count = int(input(f"Stocks to sell (own {player.stocks}): "))
                if count <= 0:
                    print("Positive numbers only.")
                elif count > player.stocks:
                    print("Don't own that many stocks.")
                else:
                    revenue = count * player.stock_price
                    player.stocks -= count
                    player.clean_balance += revenue
                    print(f"💰 Sold {count} stocks for ${revenue:.2f}")
            except ValueError:
                print("Enter a valid number.")

        elif cmd == "invest":
            if player.in_jail:
                print("Can't invest from jail.")
                continue
            if player.clean_balance >= 5000:
                player.clean_balance -= 5000
                player.real_estate += 1
                player.passive_income += 500
                player.real_estate_value += 50000
                print("🏠 Bought real estate. Passive income +$500/turn.")
            else:
                print("Need $5000 for real estate.")

        elif cmd == "crime":
            commit_crime(player)

        elif cmd == "launder":
            launder_money(player)

        elif cmd == "contacts":
            manage_contacts(player)

        elif cmd == "loans":
            loan_sharks(player)

        elif cmd == "bribe":
            bribe(player)

        elif cmd == "wait":
            next_turn(player)

        elif cmd == "help":
            print(COMMANDS)

        elif cmd == "quit":
            print(f"👑 Thanks for playing, {username}. Your empire awaits your return...")
            print(f"📊 Final Stats: ${player.clean_balance + player.dirty_balance:,.2f} total money")
            print(f"⚡ Respect: {player.respect} | 😨 Fear: {player.fear} | 🏠 Properties: {player.real_estate}")
            break

        else:
            print("❌ Unknown command. Type 'help' for options.")

        # Game over conditions
        if player.total_debt > 200000 and player.clean_balance + player.dirty_balance < player.total_debt * 0.1:
            print("\n💀💀 GAME OVER 💀💀")
            print("The loan sharks have had enough. You've been eliminated.")
            print("In the criminal world, debts are paid in blood...")
            break

        if player.clean_balance + player.dirty_balance <= 0 and player.stocks == 0 and player.real_estate == 0 and not player.contacts:
            print("\n💀 GAME OVER 💀")
            print("Broke, powerless, and alone. The streets have claimed another victim.")
            break

if __name__ == '__main__':
    main()
