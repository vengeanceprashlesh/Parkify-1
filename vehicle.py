from datetime import datetime

class Vehicle:
    def __init__(self, plate_number):
        self.plate_number = plate_number
        self.entry_time = None
        self.exit_time = None
        self.queued_at = None  # New attribute to store the timestamp when vehicle enters the queue

    def __str__(self):
        return f"Vehicle({self.plate_number})"