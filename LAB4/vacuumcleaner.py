import random

# Define environment
rooms = {
    'A': random.choice(['Clean', 'Dirty']),
    'B': random.choice(['Clean', 'Dirty']),
    'C': random.choice(['Clean', 'Dirty']),
    'D': random.choice(['Clean', 'Dirty'])
}

# Initial position of the agent
agent_position = random.choice(['A', 'B', 'C', 'D'])

# Display current state
def display_state():
    print(f"Agent is in Room {agent_position}")
    for room, status in rooms.items():
        print(f"Room {room}: {status}")
    print()

# Rule-based agent logic with smart movement
def vacuum_agent():
    global agent_position
    steps = 0

    # Keep track of cleaned rooms
    cleaned_rooms = set()

    while len(cleaned_rooms) < 4:
        display_state()

        # Clean current room if dirty
        if rooms[agent_position] == 'Dirty':
            print(f"🧹 Cleaning Room {agent_position}")
            rooms[agent_position] = 'Clean'
            cleaned_rooms.add(agent_position)
        else:
            print(f"✅ Room {agent_position} is already clean.")
            cleaned_rooms.add(agent_position)

        # Decide next move only if not all rooms are clean
        if len(cleaned_rooms) < 4:
            # Move to the next room that is still dirty
            for next_room in ['A', 'B', 'C', 'D']:
                if next_room not in cleaned_rooms:
                    agent_position = next_room
                    break

        steps += 1
        print(f"Step {steps} complete.\n")

    print("🎉 All rooms are clean!")
    display_state()

vacuum_agent()