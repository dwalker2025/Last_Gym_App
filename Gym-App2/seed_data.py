from models import db, Meal
from app import app
import json


# Create sample meals

def seed_meals():
    """Seed the database with sample meals"""
    # Clear existing meals
    Meal.query.delete()

    # Sample meals for different dietary preferences and fitness goals
    meals = [
        # BREAKFAST OPTIONS
        # Vegan options
        Meal(
            name="Vegan Protein Oatmeal",
            description="Oatmeal with plant protein, berries, and nuts",
            calories=450,
            protein=25,
            carbs=60,
            fats=15,
            meal_type="breakfast",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="plant protein",
            allergens=json.dumps(["nuts"])
        ),
        Meal(
            name="Tofu Scramble",
            description="Scrambled tofu with vegetables and spices",
            calories=350,
            protein=20,
            carbs=25,
            fats=18,
            meal_type="breakfast",
            dietary_type="vegan",
            fitness_goal="cutting",
            primary_protein="tofu",
            allergens=json.dumps(["soy"])
        ),
        Meal(
            name="Protein Smoothie",
            description="Plant protein smoothie with banana, spinach, and almond milk",
            calories=500,
            protein=30,
            carbs=65,
            fats=12,
            meal_type="breakfast",
            dietary_type="vegan",
            fitness_goal="bulking",
            primary_protein="plant protein",
            allergens=json.dumps(["nuts"])
        ),

        # Vegetarian options
        Meal(
            name="Greek Yogurt Bowl",
            description="Greek yogurt with honey, granola, and fresh fruit",
            calories=400,
            protein=25,
            carbs=45,
            fats=12,
            meal_type="breakfast",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="yogurt",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Egg White Omelette",
            description="Egg white omelette with spinach, tomatoes, and feta cheese",
            calories=300,
            protein=25,
            carbs=10,
            fats=15,
            meal_type="breakfast",
            dietary_type="vegetarian",
            fitness_goal="cutting",
            primary_protein="eggs",
            allergens=json.dumps(["eggs", "dairy"])
        ),

        # Omnivore options
        Meal(
            name="Protein Pancakes",
            description="Protein-packed pancakes with maple syrup and berries",
            calories=550,
            protein=35,
            carbs=70,
            fats=15,
            meal_type="breakfast",
            dietary_type="omnivore",
            fitness_goal="bulking",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy", "eggs"])
        ),
        Meal(
            name="Breakfast Burrito",
            description="Eggs, turkey bacon, and vegetables wrapped in a tortilla",
            calories=450,
            protein=30,
            carbs=35,
            fats=22,
            meal_type="breakfast",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="eggs",
            allergens=json.dumps(["eggs", "gluten"])
        ),

        # LUNCH OPTIONS
        # Vegan options
        Meal(
            name="Lentil Salad",
            description="Lentils with mixed greens, vegetables, and vinaigrette",
            calories=400,
            protein=20,
            carbs=50,
            fats=15,
            meal_type="lunch",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="lentils",
            allergens=json.dumps([])
        ),
        Meal(
            name="Chickpea Buddha Bowl",
            description="Roasted chickpeas, quinoa, vegetables, and tahini dressing",
            calories=550,
            protein=22,
            carbs=80,
            fats=18,
            meal_type="lunch",
            dietary_type="vegan",
            fitness_goal="bulking",
            primary_protein="chickpeas",
            allergens=json.dumps(["sesame"])
        ),

        # Vegetarian options
        Meal(
            name="Mediterranean Wrap",
            description="Hummus, feta, and vegetables in a whole grain wrap",
            calories=450,
            protein=18,
            carbs=55,
            fats=20,
            meal_type="lunch",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="chickpeas",
            allergens=json.dumps(["gluten", "dairy"])
        ),
        Meal(
            name="Protein Pasta",
            description="High-protein pasta with tomato sauce and cheese",
            calories=550,
            protein=30,
            carbs=70,
            fats=15,
            meal_type="lunch",
            dietary_type="vegetarian",
            fitness_goal="bulking",
            primary_protein="pasta",
            allergens=json.dumps(["gluten", "dairy"])
        ),

        # Omnivore options
        Meal(
            name="Chicken Salad",
            description="Grilled chicken breast on a bed of mixed greens",
            calories=400,
            protein=35,
            carbs=15,
            fats=20,
            meal_type="lunch",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="chicken",
            allergens=json.dumps([])
        ),
        Meal(
            name="Turkey Sandwich",
            description="Lean turkey, avocado, and vegetables on whole grain bread",
            calories=450,
            protein=30,
            carbs=45,
            fats=15,
            meal_type="lunch",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="turkey",
            allergens=json.dumps(["gluten"])
        ),

        # DINNER OPTIONS
        # Vegan options
        Meal(
            name="Vegetable Stir Fry",
            description="Tofu and vegetables stir fried with brown rice",
            calories=450,
            protein=20,
            carbs=65,
            fats=12,
            meal_type="dinner",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="tofu",
            allergens=json.dumps(["soy"])
        ),
        Meal(
            name="Bean Chili",
            description="Three bean chili with plant protein and spices",
            calories=500,
            protein=28,
            carbs=70,
            fats=10,
            meal_type="dinner",
            dietary_type="vegan",
            fitness_goal="bulking",
            primary_protein="beans",
            allergens=json.dumps([])
        ),

        # Vegetarian options
        Meal(
            name="Eggplant Parmesan",
            description="Baked eggplant with tomato sauce and cheese",
            calories=500,
            protein=22,
            carbs=50,
            fats=25,
            meal_type="dinner",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="cheese",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Veggie Burger",
            description="Plant-based burger with sweet potato fries",
            calories=600,
            protein=25,
            carbs=80,
            fats=22,
            meal_type="dinner",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="plant protein",
            allergens=json.dumps(["gluten", "soy"])
        ),

        # Omnivore options
        Meal(
            name="Grilled Salmon",
            description="Grilled salmon with asparagus and quinoa",
            calories=500,
            protein=40,
            carbs=35,
            fats=22,
            meal_type="dinner",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="fish",
            allergens=json.dumps(["fish"])
        ),
        Meal(
            name="Lean Steak",
            description="Sirloin steak with sweet potato and broccoli",
            calories=600,
            protein=45,
            carbs=40,
            fats=25,
            meal_type="dinner",
            dietary_type="omnivore",
            fitness_goal="bulking",
            primary_protein="beef",
            allergens=json.dumps([])
        ),

        # SNACK OPTIONS
        # Vegan options
        Meal(
            name="Fruit and Nuts",
            description="Apple slices with almond butter",
            calories=250,
            protein=8,
            carbs=30,
            fats=12,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="nuts",
            allergens=json.dumps(["nuts"])
        ),
        Meal(
            name="Protein Energy Balls",
            description="Plant protein, dates, and oats rolled into bite-size balls",
            calories=200,
            protein=10,
            carbs=25,
            fats=8,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="bulking",
            primary_protein="plant protein",
            allergens=json.dumps(["nuts"])
        ),

        # Vegetarian options
        Meal(
            name="Cottage Cheese",
            description="Cottage cheese with berries and honey",
            calories=200,
            protein=20,
            carbs=15,
            fats=5,
            meal_type="snack",
            dietary_type="vegetarian",
            fitness_goal="cutting",
            primary_protein="dairy",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Protein Shake",
            description="Whey protein shake with banana and milk",
            calories=300,
            protein=30,
            carbs=30,
            fats=5,
            meal_type="snack",
            dietary_type="vegetarian",
            fitness_goal="bulking",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy"])
        ),

        # Omnivore options
        Meal(
            name="Jerky and Almonds",
            description="Beef jerky with a handful of almonds",
            calories=250,
            protein=20,
            carbs=10,
            fats=15,
            meal_type="snack",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="beef",
            allergens=json.dumps(["nuts"])
        ),
        Meal(
            name="Protein Bar",
            description="High protein bar with low sugar",
            calories=200,
            protein=20,
            carbs=20,
            fats=5,
            meal_type="snack",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy", "nuts"])
        ),
        Meal(
            name="Chia Seed Pudding",
            description="Chia seeds soaked in almond milk with berries and maple syrup",
            calories=350,
            protein=12,
            carbs=40,
            fats=18,
            meal_type="breakfast",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="chia seeds",
            allergens=json.dumps(["nuts"])
        ),
        Meal(
            name="Protein Waffles",
            description="High-protein waffles topped with Greek yogurt and fresh fruit",
            calories=520,
            protein=32,
            carbs=55,
            fats=20,
            meal_type="breakfast",
            dietary_type="vegetarian",
            fitness_goal="bulking",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy", "eggs", "gluten"])
        ),
        Meal(
            name="Smoked Salmon Bagel",
            description="Whole grain bagel with cream cheese, smoked salmon, and capers",
            calories=480,
            protein=28,
            carbs=48,
            fats=22,
            meal_type="breakfast",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="fish",
            allergens=json.dumps(["gluten", "dairy", "fish"])
        ),
        Meal(
            name="Low-Carb Breakfast Bowl",
            description="Scrambled eggs with avocado, turkey bacon, and vegetables",
            calories=420,
            protein=30,
            carbs=12,
            fats=30,
            meal_type="breakfast",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="eggs",
            allergens=json.dumps(["eggs"])
        ),

        # ADDITIONAL LUNCH OPTIONS
        Meal(
            name="Tempeh Salad",
            description="Marinated tempeh with mixed greens, avocado, and lime dressing",
            calories=420,
            protein=24,
            carbs=35,
            fats=22,
            meal_type="lunch",
            dietary_type="vegan",
            fitness_goal="cutting",
            primary_protein="tempeh",
            allergens=json.dumps(["soy"])
        ),
        Meal(
            name="Quinoa Power Bowl",
            description="Quinoa with roasted vegetables, black beans, and avocado",
            calories=520,
            protein=18,
            carbs=70,
            fats=20,
            meal_type="lunch",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="quinoa and beans",
            allergens=json.dumps([])
        ),
        Meal(
            name="Tuna Salad Sandwich",
            description="Tuna mixed with Greek yogurt on whole grain bread with lettuce and tomato",
            calories=450,
            protein=35,
            carbs=40,
            fats=18,
            meal_type="lunch",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="fish",
            allergens=json.dumps(["fish", "gluten", "dairy"])
        ),
        Meal(
            name="Protein-Packed Bento Box",
            description="Grilled chicken, hard-boiled eggs, edamame, and brown rice",
            calories=550,
            protein=45,
            carbs=50,
            fats=15,
            meal_type="lunch",
            dietary_type="omnivore",
            fitness_goal="bulking",
            primary_protein="chicken and eggs",
            allergens=json.dumps(["eggs", "soy"])
        ),

        # ADDITIONAL DINNER OPTIONS
        Meal(
            name="Lentil Shepherd's Pie",
            description="Lentil and vegetable base topped with mashed sweet potatoes",
            calories=480,
            protein=22,
            carbs=65,
            fats=14,
            meal_type="dinner",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="lentils",
            allergens=json.dumps([])
        ),
        Meal(
            name="Cauliflower Fried Rice",
            description="Riced cauliflower stir-fried with tofu, vegetables, and spices",
            calories=320,
            protein=20,
            carbs=25,
            fats=18,
            meal_type="dinner",
            dietary_type="vegan",
            fitness_goal="cutting",
            primary_protein="tofu",
            allergens=json.dumps(["soy"])
        ),
        Meal(
            name="Stuffed Bell Peppers",
            description="Bell peppers stuffed with quinoa, black beans, corn, and cheese",
            calories=420,
            protein=18,
            carbs=50,
            fats=16,
            meal_type="dinner",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="quinoa and beans",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Pesto Pasta with Eggs",
            description="Whole grain pasta with pesto sauce and poached eggs",
            calories=550,
            protein=25,
            carbs=65,
            fats=22,
            meal_type="dinner",
            dietary_type="vegetarian",
            fitness_goal="bulking",
            primary_protein="eggs",
            allergens=json.dumps(["gluten", "eggs", "dairy", "nuts"])
        ),
        Meal(
            name="Baked Cod with Vegetables",
            description="Oven-baked cod fillet with roasted vegetables and quinoa",
            calories=380,
            protein=35,
            carbs=30,
            fats=12,
            meal_type="dinner",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="fish",
            allergens=json.dumps(["fish"])
        ),
        Meal(
            name="Turkey Meatballs",
            description="Lean turkey meatballs with zucchini noodles and tomato sauce",
            calories=450,
            protein=40,
            carbs=20,
            fats=22,
            meal_type="dinner",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="turkey",
            allergens=json.dumps(["eggs"])
        ),
        Meal(
            name="Chicken Fajita Bowl",
            description="Grilled chicken with peppers, onions, black beans, and brown rice",
            calories=580,
            protein=42,
            carbs=65,
            fats=15,
            meal_type="dinner",
            dietary_type="omnivore",
            fitness_goal="bulking",
            primary_protein="chicken",
            allergens=json.dumps([])
        ),

        # ADDITIONAL SNACK OPTIONS
        Meal(
            name="Roasted Chickpeas",
            description="Crunchy roasted chickpeas seasoned with spices",
            calories=180,
            protein=10,
            carbs=22,
            fats=6,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="chickpeas",
            allergens=json.dumps([])
        ),
        Meal(
            name="Hummus and Veggies",
            description="Homemade hummus with carrot and cucumber sticks",
            calories=220,
            protein=8,
            carbs=25,
            fats=12,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="chickpeas",
            allergens=json.dumps(["sesame"])
        ),
        Meal(
            name="Edamame",
            description="Steamed edamame pods lightly salted",
            calories=150,
            protein=12,
            carbs=12,
            fats=6,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="cutting",
            primary_protein="soy",
            allergens=json.dumps(["soy"])
        ),
        Meal(
            name="Avocado Toast",
            description="Whole grain toast with mashed avocado and hemp seeds",
            calories=280,
            protein=10,
            carbs=30,
            fats=16,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="maintenance",
            primary_protein="hemp seeds",
            allergens=json.dumps(["gluten"])
        ),
        Meal(
            name="Trail Mix",
            description="Mix of nuts, seeds, and dried fruits",
            calories=250,
            protein=8,
            carbs=22,
            fats=18,
            meal_type="snack",
            dietary_type="vegan",
            fitness_goal="bulking",
            primary_protein="nuts",
            allergens=json.dumps(["nuts"])
        ),
        Meal(
            name="Protein Muffin",
            description="Homemade protein muffin with blueberries",
            calories=220,
            protein=15,
            carbs=25,
            fats=8,
            meal_type="snack",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy", "eggs", "gluten"])
        ),
        Meal(
            name="Greek Yogurt Parfait",
            description="Greek yogurt layered with granola and berries",
            calories=280,
            protein=20,
            carbs=30,
            fats=8,
            meal_type="snack",
            dietary_type="vegetarian",
            fitness_goal="maintenance",
            primary_protein="yogurt",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Hard-Boiled Eggs",
            description="Hard-boiled eggs with a pinch of salt",
            calories=140,
            protein=12,
            carbs=0,
            fats=10,
            meal_type="snack",
            dietary_type="vegetarian",
            fitness_goal="cutting",
            primary_protein="eggs",
            allergens=json.dumps(["eggs"])
        ),
        Meal(
            name="Protein Rice Cakes",
            description="Rice cakes topped with cottage cheese and cucumber",
            calories=180,
            protein=15,
            carbs=20,
            fats=3,
            meal_type="snack",
            dietary_type="vegetarian",
            fitness_goal="cutting",
            primary_protein="dairy",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Turkey Roll-Ups",
            description="Sliced turkey rolled with avocado and lettuce",
            calories=200,
            protein=22,
            carbs=5,
            fats=12,
            meal_type="snack",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="turkey",
            allergens=json.dumps([])
        ),
        Meal(
            name="Tuna on Crackers",
            description="Tuna salad on whole grain crackers",
            calories=230,
            protein=20,
            carbs=18,
            fats=10,
            meal_type="snack",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="fish",
            allergens=json.dumps(["fish", "gluten"])
        ),
        Meal(
            name="Beef and Cheese Roll",
            description="Sliced roast beef with cheese and bell pepper strips",
            calories=240,
            protein=25,
            carbs=3,
            fats=15,
            meal_type="snack",
            dietary_type="omnivore",
            fitness_goal="cutting",
            primary_protein="beef",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Protein Banana Bread",
            description="Homemade protein-enriched banana bread",
            calories=280,
            protein=12,
            carbs=35,
            fats=12,
            meal_type="snack",
            dietary_type="omnivore",
            fitness_goal="bulking",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy", "eggs", "gluten"])
        ),

        # POST-WORKOUT OPTIONS
        Meal(
            name="Chocolate Protein Recovery Shake",
            description="Plant-based chocolate protein with banana and almond milk",
            calories=320,
            protein=30,
            carbs=40,
            fats=8,
            meal_type="post-workout",
            dietary_type="vegan",
            fitness_goal="bulking",
            primary_protein="plant protein",
            allergens=json.dumps(["nuts"])
        ),
        Meal(
            name="Berry Protein Smoothie",
            description="Whey protein with mixed berries, banana, and milk",
            calories=350,
            protein=35,
            carbs=45,
            fats=5,
            meal_type="post-workout",
            dietary_type="vegetarian",
            fitness_goal="bulking",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy"])
        ),
        Meal(
            name="Chicken and Rice",
            description="Grilled chicken breast with white rice and steamed vegetables",
            calories=480,
            protein=40,
            carbs=50,
            fats=10,
            meal_type="post-workout",
            dietary_type="omnivore",
            fitness_goal="bulking",
            primary_protein="chicken",
            allergens=json.dumps([])
        ),
        Meal(
            name="Protein Pancakes with Fruits",
            description="Quick protein pancakes topped with fresh berries",
            calories=420,
            protein=30,
            carbs=50,
            fats=12,
            meal_type="post-workout",
            dietary_type="omnivore",
            fitness_goal="maintenance",
            primary_protein="whey protein",
            allergens=json.dumps(["dairy", "eggs", "gluten"])
        )
    ]

    # To use this in the seed_meals function, add the line:
    # meals.extend(additional_meals)
    # right before the loop that adds meals to the session


    # Add all meals to the session
    for meal in meals:
        db.session.add(meal)

    # Commit the session to save changes
    db.session.commit()
    print(f"Added {len(meals)} meals to the database")


from models import db, Exercise, WorkoutTemplate
from app import app
import json


def seed_exercises():
    """Seed the database with sample exercises"""
    # Clear existing exercises
    Exercise.query.delete()

    # Sample exercises for different muscle groups and difficulty levels
    exercises = [
        # Chest exercises
        Exercise(
            name="Push-up",
            description="A bodyweight exercise that targets the chest, shoulders, and triceps",
            muscle_group="chest",
            difficulty="beginner",
            equipment_needed=json.dumps(["none"]),
            contraindications=json.dumps(["wrist injury", "shoulder injury"]),
            video_url="https://example.com/push-up"
        ),
        Exercise(
            name="Bench Press",
            description="A barbell exercise that primarily targets the chest muscles",
            muscle_group="chest",
            difficulty="intermediate",
            equipment_needed=json.dumps(["barbell", "bench"]),
            contraindications=json.dumps(["shoulder injury", "pectoral strain"]),
            video_url="https://example.com/bench-press"
        ),
        Exercise(
            name="Incline Dumbbell Press",
            description="A dumbbell exercise that targets the upper chest",
            muscle_group="chest",
            difficulty="intermediate",
            equipment_needed=json.dumps(["dumbbells", "incline bench"]),
            contraindications=json.dumps(["shoulder injury", "rotator cuff injury"]),
            video_url="https://example.com/incline-dumbbell-press"
        ),
        Exercise(
            name="Chest Fly",
            description="An isolation exercise that targets the chest muscles",
            muscle_group="chest",
            difficulty="intermediate",
            equipment_needed=json.dumps(["dumbbells", "bench"]),
            contraindications=json.dumps(["shoulder injury"]),
            video_url="https://example.com/chest-fly"
        ),
        Exercise(
            name="Cable Crossover",
            description="A cable exercise that targets the chest muscles from multiple angles",
            muscle_group="chest",
            difficulty="advanced",
            equipment_needed=json.dumps(["cable machine"]),
            contraindications=json.dumps(["shoulder injury", "chest strain"]),
            video_url="https://example.com/cable-crossover"
        ),

        # Back exercises
        Exercise(
            name="Pull-up",
            description="A bodyweight exercise that targets the back and biceps",
            muscle_group="back",
            difficulty="intermediate",
            equipment_needed=json.dumps(["pull-up bar"]),
            contraindications=json.dumps(["shoulder injury", "elbow injury"]),
            video_url="https://example.com/pull-up"
        ),
        Exercise(
            name="Lat Pulldown",
            description="A machine exercise that targets the latissimus dorsi muscles",
            muscle_group="back",
            difficulty="beginner",
            equipment_needed=json.dumps(["lat pulldown machine"]),
            contraindications=json.dumps(["shoulder injury", "upper back injury"]),
            video_url="https://example.com/lat-pulldown"
        ),
        Exercise(
            name="Bent Over Row",
            description="A barbell exercise that targets the middle back muscles",
            muscle_group="back",
            difficulty="intermediate",
            equipment_needed=json.dumps(["barbell"]),
            contraindications=json.dumps(["lower back injury", "herniated disc"]),
            video_url="https://example.com/bent-over-row"
        ),
        Exercise(
            name="Seated Cable Row",
            description="A cable exercise that targets the middle back muscles",
            muscle_group="back",
            difficulty="beginner",
            equipment_needed=json.dumps(["cable machine"]),
            contraindications=json.dumps(["lower back injury"]),
            video_url="https://example.com/seated-cable-row"
        ),
        Exercise(
            name="Deadlift",
            description="A compound exercise that targets the entire posterior chain",
            muscle_group="back",
            difficulty="advanced",
            equipment_needed=json.dumps(["barbell"]),
            contraindications=json.dumps(["lower back injury", "herniated disc", "hamstring injury"]),
            video_url="https://example.com/deadlift"
        ),

        # Leg exercises
        Exercise(
            name="Squat",
            description="A compound exercise that targets the quadriceps, hamstrings, and glutes",
            muscle_group="legs",
            difficulty="intermediate",
            equipment_needed=json.dumps(["barbell", "squat rack"]),
            contraindications=json.dumps(["knee injury", "lower back injury"]),
            video_url="https://example.com/squat"
        ),
        Exercise(
            name="Leg Press",
            description="A machine exercise that targets the quadriceps, hamstrings, and glutes",
            muscle_group="legs",
            difficulty="beginner",
            equipment_needed=json.dumps(["leg press machine"]),
            contraindications=json.dumps(["knee injury"]),
            video_url="https://example.com/leg-press"
        ),
        Exercise(
            name="Lunges",
            description="A unilateral exercise that targets the quadriceps, hamstrings, and glutes",
            muscle_group="legs",
            difficulty="beginner",
            equipment_needed=json.dumps(["none", "dumbbells"]),
            contraindications=json.dumps(["knee injury", "ankle injury"]),
            video_url="https://example.com/lunges"
        ),
        Exercise(
            name="Romanian Deadlift",
            description="A barbell exercise that targets the hamstrings and lower back",
            muscle_group="legs",
            difficulty="intermediate",
            equipment_needed=json.dumps(["barbell"]),
            contraindications=json.dumps(["lower back injury", "hamstring injury"]),
            video_url="https://example.com/romanian-deadlift"
        ),
        Exercise(
            name="Leg Extension",
            description="A machine exercise that isolates the quadriceps",
            muscle_group="legs",
            difficulty="beginner",
            equipment_needed=json.dumps(["leg extension machine"]),
            contraindications=json.dumps(["knee injury", "patellar tendonitis"]),
            video_url="https://example.com/leg-extension"
        ),

        # Shoulder exercises
        Exercise(
            name="Overhead Press",
            description="A barbell exercise that targets the shoulders and triceps",
            muscle_group="shoulders",
            difficulty="intermediate",
            equipment_needed=json.dumps(["barbell"]),
            contraindications=json.dumps(["shoulder injury", "rotator cuff injury"]),
            video_url="https://example.com/overhead-press"
        ),
        Exercise(
            name="Lateral Raise",
            description="A dumbbell exercise that targets the lateral deltoids",
            muscle_group="shoulders",
            difficulty="beginner",
            equipment_needed=json.dumps(["dumbbells"]),
            contraindications=json.dumps(["shoulder injury", "rotator cuff injury"]),
            video_url="https://example.com/lateral-raise"
        ),
        Exercise(
            name="Front Raise",
            description="A dumbbell exercise that targets the anterior deltoids",
            muscle_group="shoulders",
            difficulty="beginner",
            equipment_needed=json.dumps(["dumbbells"]),
            contraindications=json.dumps(["shoulder injury", "rotator cuff injury"]),
            video_url="https://example.com/front-raise"
        ),
        Exercise(
            name="Rear Delt Fly",
            description="A dumbbell exercise that targets the posterior deltoids",
            muscle_group="shoulders",
            difficulty="beginner",
            equipment_needed=json.dumps(["dumbbells"]),
            contraindications=json.dumps(["shoulder injury", "rotator cuff injury"]),
            video_url="https://example.com/rear-delt-fly"
        ),
        Exercise(
            name="Face Pull",
            description="A cable exercise that targets the rear deltoids and upper back",
            muscle_group="shoulders",
            difficulty="intermediate",
            equipment_needed=json.dumps(["cable machine"]),
            contraindications=json.dumps(["shoulder injury", "rotator cuff injury"]),
            video_url="https://example.com/face-pull"
        ),

        # Arm exercises
        Exercise(
            name="Bicep Curl",
            description="A dumbbell exercise that targets the biceps",
            muscle_group="arms",
            difficulty="beginner",
            equipment_needed=json.dumps(["dumbbells"]),
            contraindications=json.dumps(["elbow injury", "wrist injury"]),
            video_url="https://example.com/bicep-curl"
        ),
        Exercise(
            name="Tricep Pushdown",
            description="A cable exercise that targets the triceps",
            muscle_group="arms",
            difficulty="beginner",
            equipment_needed=json.dumps(["cable machine"]),
            contraindications=json.dumps(["elbow injury", "wrist injury"]),
            video_url="https://example.com/tricep-pushdown"
        ),
        Exercise(
            name="Hammer Curl",
            description="A dumbbell exercise that targets the biceps and forearms",
            muscle_group="arms",
            difficulty="beginner",
            equipment_needed=json.dumps(["dumbbells"]),
            contraindications=json.dumps(["elbow injury", "wrist injury"]),
            video_url="https://example.com/hammer-curl"
        ),
        Exercise(
            name="Skullcrusher",
            description="A dumbbell or barbell exercise that targets the triceps",
            muscle_group="arms",
            difficulty="intermediate",
            equipment_needed=json.dumps(["barbell", "dumbbells", "bench"]),
            contraindications=json.dumps(["elbow injury", "shoulder injury"]),
            video_url="https://example.com/skullcrusher"
        ),
        Exercise(
            name="Cable Curl",
            description="A cable exercise that targets the biceps",
            muscle_group="arms",
            difficulty="beginner",
            equipment_needed=json.dumps(["cable machine"]),
            contraindications=json.dumps(["elbow injury", "wrist injury"]),
            video_url="https://example.com/cable-curl"
        ),

        # Core exercises
        Exercise(
            name="Plank",
            description="A bodyweight exercise that targets the core muscles",
            muscle_group="core",
            difficulty="beginner",
            equipment_needed=json.dumps(["none"]),
            contraindications=json.dumps(["lower back injury", "shoulder injury"]),
            video_url="https://example.com/plank"
        ),
        Exercise(
            name="Crunch",
            description="A bodyweight exercise that targets the abdominal muscles",
            muscle_group="core",
            difficulty="beginner",
            equipment_needed=json.dumps(["none"]),
            contraindications=json.dumps(["lower back injury", "neck injury"]),
            video_url="https://example.com/crunch"
        ),
        Exercise(
            name="Russian Twist",
            description="A bodyweight or weighted exercise that targets the obliques",
            muscle_group="core",
            difficulty="intermediate",
            equipment_needed=json.dumps(["none", "medicine ball", "weight plate"]),
            contraindications=json.dumps(["lower back injury"]),
            video_url="https://example.com/russian-twist"
        ),
        Exercise(
            name="Hanging Leg Raise",
            description="A bodyweight exercise that targets the lower abdominal muscles",
            muscle_group="core",
            difficulty="advanced",
            equipment_needed=json.dumps(["pull-up bar"]),
            contraindications=json.dumps(["lower back injury", "shoulder injury"]),
            video_url="https://example.com/hanging-leg-raise"
        ),
        Exercise(
            name="Mountain Climber",
            description="A dynamic bodyweight exercise that targets the core and provides cardiovascular benefits",
            muscle_group="core",
            difficulty="intermediate",
            equipment_needed=json.dumps(["none"]),
            contraindications=json.dumps(["wrist injury", "shoulder injury"]),
            video_url="https://example.com/mountain-climber"
        ),

        # Cardio exercises
        Exercise(
            name="Running",
            description="A cardiovascular exercise that improves endurance and burns calories",
            muscle_group="cardio",
            difficulty="beginner",
            equipment_needed=json.dumps(["none", "treadmill"]),
            contraindications=json.dumps(["knee injury", "ankle injury", "foot injury"]),
            video_url="https://example.com/running"
        ),
        Exercise(
            name="Cycling",
            description="A low-impact cardiovascular exercise that targets the legs",
            muscle_group="cardio",
            difficulty="beginner",
            equipment_needed=json.dumps(["stationary bike", "bicycle"]),
            contraindications=json.dumps(["knee injury", "hip injury"]),
            video_url="https://example.com/cycling"
        ),
        Exercise(
            name="Jump Rope",
            description="A high-intensity cardiovascular exercise that improves coordination",
            muscle_group="cardio",
            difficulty="intermediate",
            equipment_needed=json.dumps(["jump rope"]),
            contraindications=json.dumps(["knee injury", "ankle injury", "foot injury"]),
            video_url="https://example.com/jump-rope"
        ),
        Exercise(
            name="Rowing",
            description="A full-body cardiovascular exercise that targets the back, legs, and arms",
            muscle_group="cardio",
            difficulty="intermediate",
            equipment_needed=json.dumps(["rowing machine"]),
            contraindications=json.dumps(["lower back injury", "shoulder injury"]),
            video_url="https://example.com/rowing"
        ),
        Exercise(
            name="Burpee",
            description="A high-intensity full-body exercise that combines a squat, push-up, and jump",
            muscle_group="cardio",
            difficulty="advanced",
            equipment_needed=json.dumps(["none"]),
            contraindications=json.dumps(["knee injury", "shoulder injury", "wrist injury"]),
            video_url="https://example.com/burpee"
        )
    ]

    # Add all exercises to the session
    for exercise in exercises:
        db.session.add(exercise)

    # Commit the session to save changes
    db.session.commit()
    print(f"Added {len(exercises)} exercises to the database")


def seed_workout_templates():
    """Seed the database with sample workout templates"""
    # Clear existing workout templates
    WorkoutTemplate.query.delete()

    # Create workout templates
    templates = [
        # Beginner workouts
        WorkoutTemplate(
            name="Beginner Full Body Workout",
            description="A full body workout designed for beginners to build strength and endurance",
            difficulty="beginner",
            workout_type="strength",
            duration=45,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 1,  # Push-up
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                },
                {
                    "exercise_id": 7,  # Lat Pulldown
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                },
                {
                    "exercise_id": 12,  # Leg Press
                    "sets": 3,
                    "reps": 12,
                    "rest": 90
                },
                {
                    "exercise_id": 17,  # Lateral Raise
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 26,  # Plank
                    "sets": 3,
                    "reps": "30 seconds",
                    "rest": 60
                }
            ])
        ),
        WorkoutTemplate(
            name="Beginner Cardio Workout",
            description="A beginner-friendly cardio workout to improve cardiovascular health",
            difficulty="beginner",
            workout_type="cardio",
            duration=30,
            fitness_goal="cutting",
            exercises=json.dumps([
                {
                    "exercise_id": 31,  # Running
                    "sets": 1,
                    "reps": "15 minutes",
                    "rest": 0
                },
                {
                    "exercise_id": 33,  # Jump Rope
                    "sets": 3,
                    "reps": "1 minute",
                    "rest": 60
                },
                {
                    "exercise_id": 28,  # Russian Twist
                    "sets": 3,
                    "reps": 15,
                    "rest": 45
                },
                {
                    "exercise_id": 30,  # Mountain Climber
                    "sets": 3,
                    "reps": "30 seconds",
                    "rest": 30
                }
            ])
        ),
        WorkoutTemplate(
            name="Beginner Upper Body Workout",
            description="A beginner-friendly upper body workout to build strength",
            difficulty="beginner",
            workout_type="strength",
            duration=40,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 1,  # Push-up
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                },
                {
                    "exercise_id": 7,  # Lat Pulldown
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                },
                {
                    "exercise_id": 9,  # Seated Cable Row
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 21,  # Bicep Curl
                    "sets": 3,
                    "reps": 12,
                    "rest": 45
                },
                {
                    "exercise_id": 22,  # Tricep Pushdown
                    "sets": 3,
                    "reps": 12,
                    "rest": 45
                }
            ])
        ),

        # Intermediate workouts
        WorkoutTemplate(
            name="Intermediate Push/Pull/Legs Split - Push Day",
            description="An intermediate push workout focusing on chest, shoulders, and triceps",
            difficulty="intermediate",
            workout_type="strength",
            duration=60,
            fitness_goal="bulking",
            exercises=json.dumps([
                {
                    "exercise_id": 2,  # Bench Press
                    "sets": 4,
                    "reps": 8,
                    "rest": 90
                },
                {
                    "exercise_id": 3,  # Incline Dumbbell Press
                    "sets": 3,
                    "reps": 10,
                    "rest": 75
                },
                {
                    "exercise_id": 16,  # Overhead Press
                    "sets": 3,
                    "reps": 8,
                    "rest": 90
                },
                {
                    "exercise_id": 17,  # Lateral Raise
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 22,  # Tricep Pushdown
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 24,  # Skullcrusher
                    "sets": 3,
                    "reps": 10,
                    "rest": 75
                }
            ])
        ),
        WorkoutTemplate(
            name="Intermediate Push/Pull/Legs Split - Pull Day",
            description="An intermediate pull workout focusing on back and biceps",
            difficulty="intermediate",
            workout_type="strength",
            duration=60,
            fitness_goal="bulking",
            exercises=json.dumps([
                {
                    "exercise_id": 6,  # Pull-up
                    "sets": 4,
                    "reps": "max",
                    "rest": 90
                },
                {
                    "exercise_id": 8,  # Bent Over Row
                    "sets": 4,
                    "reps": 8,
                    "rest": 90
                },
                {
                    "exercise_id": 9,  # Seated Cable Row
                    "sets": 3,
                    "reps": 10,
                    "rest": 75
                },
                {
                    "exercise_id": 20,  # Face Pull
                    "sets": 3,
                    "reps": 15,
                    "rest": 60
                },
                {
                    "exercise_id": 21,  # Bicep Curl
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                },
                {
                    "exercise_id": 23,  # Hammer Curl
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                }
            ])
        ),
        WorkoutTemplate(
            name="Intermediate Push/Pull/Legs Split - Leg Day",
            description="An intermediate leg workout focusing on quadriceps, hamstrings, and glutes",
            difficulty="intermediate",
            workout_type="strength",
            duration=60,
            fitness_goal="bulking",
            exercises=json.dumps([
                {
                    "exercise_id": 11,  # Squat
                    "sets": 4,
                    "reps": 8,
                    "rest": 120
                },
                {
                    "exercise_id": 14,  # Romanian Deadlift
                    "sets": 3,
                    "reps": 10,
                    "rest": 90
                },
                {
                    "exercise_id": 13,  # Lunges
                    "sets": 3,
                    "reps": 10,
                    "rest": 60
                },
                {
                    "exercise_id": 15,  # Leg Extension
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 26,  # Plank
                    "sets": 3,
                    "reps": "45 seconds",
                    "rest": 60
                }
            ])
        ),

        # HIIT workouts
        WorkoutTemplate(
            name="HIIT Cardio Workout",
            description="A high-intensity interval training workout for maximum calorie burn",
            difficulty="intermediate",
            workout_type="cardio",
            duration=30,
            fitness_goal="cutting",
            exercises=json.dumps([
                {
                    "exercise_id": 35,  # Burpee
                    "sets": 4,
                    "reps": "30 seconds work, 30 seconds rest",
                    "rest": 0
                },
                {
                    "exercise_id": 33,  # Jump Rope
                    "sets": 4,
                    "reps": "30 seconds work, 30 seconds rest",
                    "rest": 0
                },
                {
                    "exercise_id": 30,  # Mountain Climber
                    "sets": 4,
                    "reps": "30 seconds work, 30 seconds rest",
                    "rest": 0
                },
                {
                    "exercise_id": 13,  # Lunges
                    "sets": 4,
                    "reps": "30 seconds work, 30 seconds rest",
                    "rest": 0
                },
                {
                    "exercise_id": 1,  # Push-up
                    "sets": 4,
                    "reps": "30 seconds work, 30 seconds rest",
                    "rest": 0
                }
            ])
        ),

        # Advanced workouts
        WorkoutTemplate(
            name="Advanced Full Body Workout",
            description="A challenging full body workout for experienced fitness enthusiasts",
            difficulty="advanced",
            workout_type="strength",
            duration=75,
            fitness_goal="bulking",
            exercises=json.dumps([
                {
                    "exercise_id": 10,  # Deadlift
                    "sets": 5,
                    "reps": 5,
                    "rest": 180
                },
                {
                    "exercise_id": 2,  # Bench Press
                    "sets": 5,
                    "reps": 5,
                    "rest": 150
                },
                {
                    "exercise_id": 6,  # Pull-up
                    "sets": 4,
                    "reps": "max",
                    "rest": 120
                },
                {
                    "exercise_id": 16,  # Overhead Press
                    "sets": 4,
                    "reps": 8,
                    "rest": 120
                },
                {
                    "exercise_id": 11,  # Squat
                    "sets": 5,
                    "reps": 5,
                    "rest": 180
                },
                {
                    "exercise_id": 29,  # Hanging Leg Raise
                    "sets": 3,
                    "reps": 15,
                    "rest": 90
                }
            ])
        ),
        WorkoutTemplate(
            name="Advanced Upper/Lower Split - Upper Day",
            description="An advanced upper body workout for experienced lifters",
            difficulty="advanced",
            workout_type="strength",
            duration=70,
            fitness_goal="bulking",
            exercises=json.dumps([
                {
                    "exercise_id": 2,  # Bench Press
                    "sets": 5,
                    "reps": 5,
                    "rest": 150
                },
                {
                    "exercise_id": 8,  # Bent Over Row
                    "sets": 4,
                    "reps": 8,
                    "rest": 120
                },
                {
                    "exercise_id": 16,  # Overhead Press
                    "sets": 4,
                    "reps": 8,
                    "rest": 120
                },
                {
                    "exercise_id": 6,  # Pull-up
                    "sets": 4,
                    "reps": "max",
                    "rest": 120
                },
                {
                    "exercise_id": 24,  # Skullcrusher
                    "sets": 3,
                    "reps": 10,
                    "rest": 90
                },
                {
                    "exercise_id": 21,  # Bicep Curl
                    "sets": 3,
                    "reps": 10,
                    "rest": 90
                }
            ])
        ),
        WorkoutTemplate(
            name="Advanced Upper/Lower Split - Lower Day",
            description="An advanced lower body workout for experienced lifters",
            difficulty="advanced",
            workout_type="strength",
            duration=70,
            fitness_goal="bulking",
            exercises=json.dumps([
                {
                    "exercise_id": 11,  # Squat
                    "sets": 5,
                    "reps": 5,
                    "rest": 180
                },
                {
                    "exercise_id": 14,  # Romanian Deadlift
                    "sets": 4,
                    "reps": 8,
                    "rest": 150
                },
                {
                    "exercise_id": 13,  # Lunges
                    "sets": 3,
                    "reps": 10,
                    "rest": 90
                },
                {
                    "exercise_id": 15,  # Leg Extension
                    "sets": 3,
                    "reps": 12,
                    "rest": 90
                },
                {
                    "exercise_id": 29,  # Hanging Leg Raise
                    "sets": 4,
                    "reps": 12,
                    "rest": 90
                },
                {
                    "exercise_id": 28,  # Russian Twist
                    "sets": 3,
                    "reps": 15,
                    "rest": 60
                }
            ])
        ),

        # Maintenance workouts
        WorkoutTemplate(
            name="Maintenance 3-Day Split - Day 1: Chest and Triceps",
            description="A workout focused on chest and triceps for maintaining muscle mass",
            difficulty="intermediate",
            workout_type="strength",
            duration=50,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 2,  # Bench Press
                    "sets": 4,
                    "reps": 10,
                    "rest": 90
                },
                {
                    "exercise_id": 3,  # Incline Dumbbell Press
                    "sets": 3,
                    "reps": 12,
                    "rest": 75
                },
                {
                    "exercise_id": 4,  # Chest Fly
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 22,  # Tricep Pushdown
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 24,  # Skullcrusher
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                }
            ])
        ),
        WorkoutTemplate(
            name="Maintenance 3-Day Split - Day 2: Back and Biceps",
            description="A workout focused on back and biceps for maintaining muscle mass",
            difficulty="intermediate",
            workout_type="strength",
            duration=50,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 8,  # Bent Over Row
                    "sets": 4,
                    "reps": 10,
                    "rest": 90
                },
                {
                    "exercise_id": 7,  # Lat Pulldown
                    "sets": 3,
                    "reps": 12,
                    "rest": 75
                },
                {
                    "exercise_id": 9,  # Seated Cable Row
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 21,  # Bicep Curl
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 23,  # Hammer Curl
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                }
            ])
        ),
        WorkoutTemplate(
            name="Maintenance 3-Day Split - Day 3: Legs and Shoulders",
            description="A workout focused on legs and shoulders for maintaining muscle mass",
            difficulty="intermediate",
            workout_type="strength",
            duration=50,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 11,  # Squat
                    "sets": 4,
                    "reps": 10,
                    "rest": 90
                },
                {
                    "exercise_id": 14,  # Romanian Deadlift
                    "sets": 3,
                    "reps": 12,
                    "rest": 75
                },
                {
                    "exercise_id": 15,  # Leg Extension
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 16,  # Overhead Press
                    "sets": 3,
                    "reps": 10,
                    "rest": 75
                },
                {
                    "exercise_id": 17,  # Lateral Raise
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                }
            ])
        ),

        # Cutting workouts
        WorkoutTemplate(
            name="Cutting Workout - Full Body Circuit",
            description="A high-intensity circuit training workout for fat loss",
            difficulty="intermediate",
            workout_type="circuit",
            duration=45,
            fitness_goal="cutting",
            exercises=json.dumps([
                {
                    "exercise_id": 1,  # Push-up
                    "sets": 3,
                    "reps": 15,
                    "rest": 30
                },
                {
                    "exercise_id": 11,  # Squat
                    "sets": 3,
                    "reps": 15,
                    "rest": 30
                },
                {
                    "exercise_id": 6,  # Pull-up
                    "sets": 3,
                    "reps": "max",
                    "rest": 30
                },
                {
                    "exercise_id": 13,  # Lunges
                    "sets": 3,
                    "reps": 12,
                    "rest": 30
                },
                {
                    "exercise_id": 30,  # Mountain Climber
                    "sets": 3,
                    "reps": "45 seconds",
                    "rest": 30
                },
                {
                    "exercise_id": 33,  # Jump Rope
                    "sets": 3,
                    "reps": "1 minute",
                    "rest": 30
                }
            ])
        ),
        WorkoutTemplate(
            name="Cutting Workout - HIIT and Core",
            description="A high-intensity interval training workout with core exercises for maximum fat burn",
            difficulty="advanced",
            workout_type="circuit",
            duration=35,
            fitness_goal="cutting",
            exercises=json.dumps([
                {
                    "exercise_id": 35,  # Burpee
                    "sets": 4,
                    "reps": "30 seconds work, 15 seconds rest",
                    "rest": 0
                },
                {
                    "exercise_id": 26,  # Plank
                    "sets": 4,
                    "reps": "45 seconds",
                    "rest": 15
                },
                {
                    "exercise_id": 30,  # Mountain Climber
                    "sets": 4,
                    "reps": "30 seconds work, 15 seconds rest",
                    "rest": 0
                },
                {
                    "exercise_id": 28,  # Russian Twist
                    "sets": 4,
                    "reps": 20,
                    "rest": 15
                },
                {
                    "exercise_id": 33,  # Jump Rope
                    "sets": 4,
                    "reps": "30 seconds work, 15 seconds rest",
                    "rest": 0
                }
            ])
        ),

        # Home workouts
        WorkoutTemplate(
            name="Home Workout - No Equipment",
            description="A full body workout that can be done at home with no equipment",
            difficulty="beginner",
            workout_type="circuit",
            duration=30,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 1,  # Push-up
                    "sets": 3,
                    "reps": 10,
                    "rest": 45
                },
                {
                    "exercise_id": 11,  # Squat (bodyweight)
                    "sets": 3,
                    "reps": 15,
                    "rest": 45
                },
                {
                    "exercise_id": 13,  # Lunges (bodyweight)
                    "sets": 3,
                    "reps": 10,
                    "rest": 45
                },
                {
                    "exercise_id": 26,  # Plank
                    "sets": 3,
                    "reps": "30 seconds",
                    "rest": 45
                },
                {
                    "exercise_id": 30,  # Mountain Climber
                    "sets": 3,
                    "reps": "30 seconds",
                    "rest": 45
                }
            ])
        ),
        WorkoutTemplate(
            name="Home Workout - Minimal Equipment",
            description="A full body workout that can be done at home with minimal equipment (dumbbells)",
            difficulty="intermediate",
            workout_type="strength",
            duration=45,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {
                    "exercise_id": 1,  # Push-up
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 11,  # Squat (with dumbbells)
                    "sets": 3,
                    "reps": 12,
                    "rest": 60
                },
                {
                    "exercise_id": 17,  # Lateral Raise
                    "sets": 3,
                    "reps": 12,
                    "rest": 45
                },
                {
                    "exercise_id": 21,  # Bicep Curl
                    "sets": 3,
                    "reps": 12,
                    "rest": 45
                },
                {
                    "exercise_id": 24,  # Skullcrusher
                    "sets": 3,
                    "reps": 12,
                    "rest": 45
                },
                {
                    "exercise_id": 28,  # Russian Twist
                    "sets": 3,
                    "reps": 15,
                    "rest": 45
                }
            ])
        )
    ]

    # Add all templates to the session
    for template in templates:
        db.session.add(template)

    # Commit the session to save changes
    db.session.commit()
    print(f"Added {len(templates)} workout templates to the database")




if __name__ == "__main__":
    with app.app_context():
        seed_exercises()
        seed_workout_templates()
        print("Database seeding completed successfully!")


if __name__ == "__main__":
    with app.app_context():
        seed_meals()