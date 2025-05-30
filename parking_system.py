from vehicle import Vehicle
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop() if self.items else None
    def peek(self): return self.items[-1] if self.items else None
    def is_empty(self): return len(self.items) == 0
    def size(self): return len(self.items)
    def __iter__(self): return iter(self.items)

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item): self.items.append(item)
    def dequeue(self): return self.items.pop(0) if self.items else None
    def is_empty(self): return len(self.items) == 0
    def size(self): return len(self.items)
    def __iter__(self): return iter(self.items)

class ParkingSystem:
    def __init__(self, capacity):
        self.capacity = capacity
        self.parking_lot = Stack()
        self.waiting_queue = Queue()
        self.logs = []

    def log_event(self, action, vehicle):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = f"[{timestamp}] {action}: {vehicle}"
        self.logs.append(log)
        console.print(log, style="dim")

    def park_vehicle(self, vehicle):
        if self.parking_lot.size() < self.capacity:
            self.parking_lot.push(vehicle)
            self.log_event("Arrived and Parked", vehicle)
            console.print(f"[bold green]Vehicle {vehicle.plate_number} parked successfully![/bold green]")
        else:
            vehicle.queued_at = datetime.now() # Set queued_at when vehicle enters queue
            self.waiting_queue.enqueue(vehicle)
            self.log_event("Parking full , Vehicle is now added to Queue ", vehicle)
            console.print(f"[bold yellow]Parking full. Vehicle {vehicle.plate_number} added to waiting queue.[/bold yellow]")

    def remove_vehicle_recursive(self, plate_number):
        def helper(temp_stack):
            if self.parking_lot.is_empty():
                return False
            current = self.parking_lot.pop()
            if current.plate_number == plate_number:
                self.log_event("Departed", current)
                console.print(f"[bold blue]Vehicle {plate_number} departed successfully![/bold blue]")
                return True
            else:
                temp_stack.push(current)
                found = helper(temp_stack)
                if found:
                    self.parking_lot.push(temp_stack.pop())
                return found

        temp_stack = Stack()
        found = helper(temp_stack)

        if not found:
            console.print(f"[bold red]Vehicle with plate {plate_number} not found in parking lot.[/bold red]")
        elif not self.waiting_queue.is_empty():
            next_vehicle = self.waiting_queue.dequeue()
            self.parking_lot.push(next_vehicle)
            self.log_event("Moved from Queue to Parking", next_vehicle)
            console.print(f"[bold magenta]Vehicle {next_vehicle.plate_number} moved from queue to parking lot.[/bold magenta]")

    def search_vehicle(self, plate_number):
        # Search in parking lot
        for vehicle in self.parking_lot.items:
            if vehicle.plate_number == plate_number:
                console.print(f"[bold green]Vehicle {plate_number} found in parking lot.[/bold green]")
                return vehicle

        # Search in waiting queue
        for vehicle in self.waiting_queue.items:
            if vehicle.plate_number == plate_number:
                console.print(f"[bold yellow]Vehicle {plate_number} found in waiting queue.[/bold yellow]")
                return vehicle

        console.print(f"[bold red]Vehicle {plate_number} not found.[/bold red]")
        return None

    def display_state(self):
        console.print(Panel("[bold blue]--- Parking Lot ---", expand=False))
        if self.parking_lot.is_empty():
            console.print("[italic dim]Parking lot is empty.[/italic dim]")
        else:
            parking_table = Table(show_header=True, header_style="bold green")
            parking_table.add_column("Plate Number")
            parking_table.add_column("Entry Time")
            parking_table.add_column("Exit Time")
            for vehicle in reversed(self.parking_lot.items):
                parking_table.add_row(vehicle.plate_number, str(vehicle.entry_time), str(vehicle.exit_time) if vehicle.exit_time else "N/A")
            console.print(parking_table)

        console.print(Panel("[bold yellow]--- Waiting Queue ---", expand=False))
        if self.waiting_queue.is_empty():
            console.print("[italic dim]Waiting queue is empty.[/italic dim]")
        else:
            queue_table = Table(show_header=True, header_style="bold yellow")
            queue_table.add_column("Plate Number")
            queue_table.add_column("Entry Time")
            queue_table.add_column("Queued At")
            for vehicle in self.waiting_queue.items:
                queue_table.add_row(vehicle.plate_number, str(vehicle.entry_time), str(vehicle.queued_at) if vehicle.queued_at else "N/A")
            console.print(queue_table)

    def report_usage(self):
        report_table = Table(show_header=True, header_style="bold cyan")
        report_table.add_column("Metric")
        report_table.add_column("Value")
        report_table.add_row("Total Parked Vehicles", str(self.parking_lot.size()))
        report_table.add_row("Total Waiting Vehicles", str(self.waiting_queue.size()))
        console.print(Panel("[bold cyan]=== Parking Report ===[/bold cyan]", expand=False))
        console.print(report_table)

        console.print(Panel("[bold magenta]--- Logs ---[/bold magenta]", expand=False))
        if not self.logs:
            console.print("[italic dim]No logs available.[/italic dim]")
        else:
            for log in self.logs:
                console.print(log, style="dim")
        return ""