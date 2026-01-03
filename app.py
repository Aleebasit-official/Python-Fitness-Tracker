import json
import os
from datetime import datetime

DATA_FILE = "fitness_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def clear():
    print("\n" * 3)

users = load_data()
current_user = None

while True:
    clear()
    print("FITNESS TRACKER")
    print("-" * 30)

    if current_user is None:
        print("1. Login")
        print("2. Signup")
        print("3. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            for user in users:
                if user["username"] == username and user["password"] == password:
                    current_user = user
                    print(f"\nWelcome back, {username}")
                    input("Press Enter to continue...")
                    break
            else:
                print("\nInvalid credentials")
                input("Press Enter to retry...")

        elif choice == "2":
            username = input("Choose username: ").strip()

            if any(u["username"] == username for u in users):
                print("\nUsername already exists")
                input("Press Enter...")
                continue

            password = input("Password: ").strip()
            confirm = input("Confirm password: ").strip()

            if password != confirm:
                print("\nPasswords do not match")
                input("Press Enter...")
                continue

            users.append({
                "username": username,
                "password": password,
                "profile": {},
                "activities": []
            })

            save_data(users)
            print("\nAccount created successfully")
            input("Press Enter...")

        elif choice == "3":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid option")
            input("Press Enter...")

    else:
        clear()
        print(f"Logged in as: {current_user['username']}")
        print("-" * 30)
        print("1. Set / Update Profile")
        print("2. Check BMI")
        print("3. Add Workout")
        print("4. View Progress")
        print("5. Logout")

        choice = input("Select option: ").strip()

        if choice == "1":
            try:
                age = int(input("Age: "))
                height = float(input("Height (m): "))
                weight = float(input("Weight (kg): "))

                current_user["profile"] = {
                    "age": age,
                    "height": height,
                    "weight": weight
                }

                save_data(users)
                print("\nProfile updated")

            except ValueError:
                print("\nInvalid input")

            input("Press Enter...")

        elif choice == "2":
            profile = current_user["profile"]

            if not profile:
                print("\nPlease set your profile first")
            else:
                bmi = profile["weight"] / (profile["height"] ** 2)
                bmi = round(bmi, 2)

                print(f"\nYour BMI: {bmi}")

                if bmi < 18.5:
                    print("Status: Underweight")
                elif bmi < 25:
                    print("Status: Normal")
                elif bmi < 30:
                    print("Status: Overweight")
                else:
                    print("Status: Obese")

            input("Press Enter...")

        elif choice == "3":
            workout = input("Workout type: ").strip()
            try:
                duration = int(input("Duration (minutes): "))

                current_user["activities"].append({
                    "workout": workout,
                    "duration": duration,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

                save_data(users)
                print("\nWorkout added")

            except ValueError:
                print("\nDuration must be a number")

            input("Press Enter...")

        elif choice == "4":
            activities = current_user["activities"]

            if not activities:
                print("\nNo workouts logged yet")
            else:
                total_minutes = sum(a["duration"] for a in activities)

                print(f"\nTotal workouts: {len(activities)}")
                print(f"Total minutes: {total_minutes}")

                print("\nRecent activity:")
                for a in activities[-3:]:
                    print(f"- {a['workout']} | {a['duration']} min | {a['date']}")

            input("Press Enter...")

        elif choice == "5":
            current_user = None
            print("\nLogged out")
            input("Press Enter...")

        else:
            print("\nInvalid option")
            input("Press Enter...")
