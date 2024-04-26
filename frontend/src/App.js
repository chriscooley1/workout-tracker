import React, { useEffect, useState } from "react";
import axios from "axios";

const WorkoutApp = () => {
  const [workouts, setWorkouts] = useState([]);
  const [newWorkout, setNewWorkout] = useState("");

  // Fetch workouts on component mount
  useEffect(() => {
    axios
      .get("http://localhost:8000/")
      .then((response) => setWorkouts(response.data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Add a new workout
  const addWorkout = () => {
    axios
      .post("http://localhost:8000/", {
        number: workouts.length + 1,
        description: newWorkout,
      })
      .then((response) => {
        setWorkouts([...workouts, response.data]);
        setNewWorkout(""); // Clear input after submission
      })
      .catch((error) => console.error("Error adding workout:", error));
  };

  return (
    <div>
      <h1>Workouts</h1>
      {workouts.map((workout) => (
        <div key={workout.id}>{workout.number}. {workout.description}</div>
      ))}
      <input
        value={newWorkout}
        onChange={(e) => setNewWorkout(e.target.value)}
        placeholder="Add a new workout"
      />
      <button onClick={addWorkout}>Add Workout</button>
    </div>
  );
};

export default WorkoutApp;
