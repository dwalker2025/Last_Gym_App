import WK
class STWK(WK):
    def __init__(self, type, name, calories, time_needed, sets, reps, weight):
        super().__init__(type, name, calories, time_needed)  # Call parent constructor
        self.sets = sets
        self.reps = reps
        self.weight = weight

    # Getters
    def get_sets(self):
        return self.sets

    def get_reps(self):
        return self.reps

    def get_weight(self):
        return self.weight

    # Setters
    def set_sets(self, sets):
        self.sets = sets

    def set_reps(self, reps):
        self.reps = reps

    def set_weight(self, weight):
        self.weight = weight

    # Override __str__ to include strength-specific info
    def __str__(self):
        return f"StrengthWorkout{{type='{self.get_type()}', name='{self.get_name()}', calories={self.get_calories()}, timeNeeded={self.get_time_needed()} minutes, sets={self.sets}, reps={self.reps}, weight={self.weight} lbs}}"