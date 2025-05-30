from parking_system import ParkingSystem
from vehicle import Vehicle
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def typing_effect(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_loading(message, duration=1):
    typing_effect(message, 0.02)
    for _ in range(10):
        sys.stdout.write("▓")
        sys.stdout.flush()
        time.sleep(duration/10)
    print()

def display_menu():
    console.print(Panel("[bold green]Parking System Menu[/]", style="blue"))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Option", style="dim", width=12)
    table.add_column("Description")
    
    table.add_row("1", "Park a vehicle")
    table.add_row("2", "Remove a vehicle")
    table.add_row("3", "Search for a vehicle")
    table.add_row("4", "Display current state")
    table.add_row("5", "Generate usage report")
    table.add_row("6", "Exit")
    
    console.print(table)
    console.print("[yellow]Enter your choice: [/]", style="bold", end="")

def main():
    typing_effect("🚗 Welcome to Enhanced Parking System 🚗", 0.03)
    
    # Get capacity from user
    while True:
        try:
            capacity = int(input("Enter parking lot capacity: "))
            if capacity > 0:
                break
            else:
                console.print("[red]Capacity must be greater than 0.[/]")
        except ValueError:
            console.print("[red]Please enter a valid number.[/]")
    
    # Initialize the parking system with user-defined capacity
    parking_system = ParkingSystem(capacity)
    typing_effect(f"Parking system initialized with capacity: {capacity}")
    
    while True:
        # Replace print statements with console.print for the menu display
        display_menu() # Call the updated display_menu function
        
        choice = input("") # input is now empty as prompt is in display_menu
        
        if choice == '1':
            plate_number = console.input("[cyan]Enter vehicle plate number: [/]")
            vehicle = Vehicle(plate_number)
            show_loading("Processing vehicle entry...", 1)
            parking_system.park_vehicle(vehicle)
            # Display the current state after adding a vehicle
            parking_system.display_state()
            
        elif choice == '2':
            plate_number = console.input("[cyan]Enter vehicle plate number to remove: [/]")
            show_loading("Retrieving vehicle...", 1)
            parking_system.remove_vehicle_recursive(plate_number)
            # Display the current state after removing a vehicle
            # This will show if a queued vehicle was moved to the parking lot
            parking_system.display_state()
            
        elif choice == '3':
            plate_number = console.input("[cyan]Enter vehicle plate number to search: [/]")
            show_loading("Searching...", 1)
            parking_system.search_vehicle(plate_number)
            
        elif choice == '4':
            show_loading("Loading current state...", 0.5)
            parking_system.display_state()
            
        elif choice == '5':
            show_loading("Generating report...", 1)
            report = parking_system.report_usage()
            console.print(report)
        elif choice == '6':
            typing_effect("Thank you for using Enhanced Parking System. Goodbye!", 0.03)
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/]")

# These lines were moved into the main loop or specific functions for better context
# console.print("[green]✓ Vehicle parked successfully![/]")
# console.print("[red]✗ Parking lot is full! Vehicle added to queue.[/]")

if __name__ == "__main__":
    main()
