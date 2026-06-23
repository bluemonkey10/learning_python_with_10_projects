import snapshot_operations
from market_data import view_current_prices, save_market_snapshot, view_historical_data, search_historical_data, portfolio_simulator, exit_program
from snapshot_operations import load_snapshots, save_snapshots
import json

def program_menu():
    try:
        snapshots = load_snapshots("snapshots.json")
        print(f"Loaded {len(snapshots)} snapshots from snapshots.json")
    except (FileNotFoundError, json.JSONDecodeError):
        snapshots = []  # Initialize an empty list if the file doesn't exist or is empty
        save_snapshots(snapshots, "snapshots.json") # overwrite the file with an empty list

    while True:
        menu_options()

        try:
            choice = int(input("Choose an option (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        
        if choice >= 1 and choice <= 6:
            user_action(choice, snapshots)
            if choice == 6:
                break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")
            continue

def menu_options():
    print("\n===FAANG STOCK TRACKER===")
    print("1. View Current Prices")
    print("2. Save Market Snapshot")
    print("3. View Historical Data")
    print("4. Search Historical Data")
    print("5. Portfolio Simulator")
    print("6. Exit")


def user_action(choice, snapshots):
    if choice == 1:
        view_current_prices()
    elif choice == 2:
        save_market_snapshot(snapshots)
    elif choice == 3:
        view_historical_data(snapshots)
    elif choice == 4:
        search_historical_data(snapshots)
    elif choice == 5:
        portfolio_simulator(snapshots)
    elif choice == 6:
        exit_program(snapshots)
    else:
        print("Invalid choice. Please select a number between 1 and 6.")
