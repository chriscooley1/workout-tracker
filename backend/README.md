# Workout Tracker

This workout tracker utilizes SQLModel, a library for SQL databases, to define the structure of its database tables and manage relationships between them. Here's a description of each component:

1. User: Represents a user of the workout tracker. Each user has a unique user_id, username, email, and password. Users can set goals which are related to them through the goals relationship.

2. Goal: Represents a fitness goal set by a user. Each goal has a unique goal_id, name, and description. Goals are associated with a specific user through the user_id field and the user relationship.

3. MuscleGroup: Represents a muscle group targeted in a workout. Each muscle group has a unique group_id and a name.

4. Equipment: Represents workout equipment. Each equipment item has a unique equipment_id, name, and description.

5. Workout: Represents a specific workout routine. Each workout has a unique workout_id, name, description, and is associated with a muscle group and equipment through the muscle_group_id and equipment_id fields, respectively.

6. Progress: Represents the progress made by a user in completing workouts. Each progress entry has a unique progress_id, user_id, workout_id, and date_completed field. Progress entries are linked to users and workouts through the user_id and workout_id fields.

7. IntensityLevel: Represents the intensity level of a workout. Each intensity level has a unique intensity_id, name, and description.

## Installation

1. First you'll need to pull down the code into a directory of your choosing

2. Make sure to run a 
   pip install -r requirements.txt
   which will install everything you need to run the program.

3. If you're using vscode, click run and debug and select the Python Debugger: FastAPI option

4. You'll also need to make sure you create a .env file, which is where you'll put your database info.