class WK:
    def __init__(self, type, name, calories, time_needed):
        self.type = type  # e.g., "Weight Loss" or "Gaining Weight"
        self.name = name  # e.g., "Running" or "Bench Press"
        self.calories = calories  # calories burned
        self.time_needed = time_needed  # time in minutes to complete the workout

    # Getters
    def get_type(self):
        return self.type

    def get_name(self):
        return self.name

    def get_calories(self):
        return self.calories

    def get_time_needed(self):
        return self.time_needed

    # Setters
    def set_type(self, type):
        self.type = type

    def set_name(self, name):
        self.name = name

    def set_calories(self, calories):
        self.calories = calories

    def set_time_needed(self, time_needed):
        self.time_needed = time_needed

    # toString method
    def __str__(self):
        return f"Workout{{type='{self.type}', name='{self.name}', calories={self.calories}, timeNeeded={self.time_needed} minutes}}"