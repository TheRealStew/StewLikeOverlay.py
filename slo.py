import requests
import re
import time
import os
import keyboard

# ANSI escape sequence for setting text color to red
RED_COLOR = "\033[91m"

# Maximum number of links to store in history
MAX_HISTORY_SIZE = 5

def generate_progress_bar(current_value, goal_value):
    progress = int((current_value / goal_value) * 100)
    text_color = '#ffffff'  # White text color
    emoji = '👍'  # Thumbs-up emoji

    progress_bar = f'<div style="background-color: #e0e0e0; width: 200px; height: 25px;">' \
                   f'<div style="background-color: #4287f5; width: {progress}%; height: 25px;"></div>' \
                   f'<div style="position: relative; top: -24px; text-align: center; color: {text_color};">' \
                   f'{current_value} {emoji}</div></div>'

    return progress_bar

# Function to save the link to the history file
def save_link_to_history(link):
    # Read the existing history file
    history = []
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as file:
            history = file.readlines()
    
    # Add the new link to the history
    history.append(link + "\n")
    
    # Trim the history to the maximum size
    if len(history) > MAX_HISTORY_SIZE:
        history = history[-MAX_HISTORY_SIZE:]
    
    # Write the updated history back to the file
    with open("history.txt", "w") as file:
        file.writelines(history)

# Function to select a link from the history
def select_link_from_history():
    # Read the history file
    history = []
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as file:
            history = file.readlines()
    
    # Display the list of links with indices
    print("\nHistory:")
    for i, link in enumerate(history):
        print(f"{i+1}. {link.strip()}")
    
    # Prompt for selection
    while True:
        choice = input("Select a link from history (1-5): ")
        if choice.isdigit() and 1 <= int(choice) <= len(history):
            selected_link = history[int(choice) - 1].strip()
            return selected_link
        else:
            print("Invalid choice. Please try again.")

# ASCII art for the start screen
start_screen = '''
  ____  _                  _     _ _           ___                 _                 ____        
 / ___|| |_ _____      __ | |   (_) | _____   / _ \__   _____ _ __| | __ _ _   _    |  _ \ _   _ 
 \___ \| __/ _ \ \ /\ / / | |   | | |/ / _ \ | | | \ \ / / _ \ '__| |/ _` | | | |   | |_) | | | |
  ___) | ||  __/\ V  V /  | |___| |   <  __/ | |_| |\ V /  __/ |  | | (_| | |_| |  _|  __/| |_| |
 |____/ \__\___| \_/\_/   |_____|_|_|\_\___|  \___/  \_/ \___|_|  |_|\__,_|\__, | (_)_|    \__, |
                                                                           |___/           |___/  
'''

# Clear the command prompt
os.system("cls")

# Print the start screen
print(RED_COLOR + start_screen)

# Check if history file exists, if not create an empty one
if not os.path.exists("history.txt"):
    open("history.txt", "a").close()

# Prompt for the video URL or history selection
while True:
    choice = input("Enter a YouTube video URL or press 'H' to select from history: ")
    if choice.lower() == "h":
        link = select_link_from_history()
        break
    elif choice.strip() != "":
        link = choice.strip()
        save_link_to_history(link)
        break
    else:
        print("Invalid choice. Please try again.")

# Prompt for the like goal
while True:
    like_goal = input("Enter the like goal (default: 5000): ")
    if like_goal.strip() == "":
        like_goal = 5000
        break
    elif like_goal.isdigit():
        like_goal = int(like_goal)
        break
    else:
        print("Invalid input. Please enter a valid number.")

# Specify the URL of the YouTube video
video_url = link

while True:
    # Send a GET request to the video URL and retrieve the HTML content
    response = requests.get(video_url)
    html_content = response.text

    # Use regular expressions to extract the like count from the HTML content
    match = re.search(r'like this video along with ([\d,]+) other people', html_content)
    like_count = int(match.group(1).replace(',', '')) if match else 0

    # Update the text file with the like count
    with open("like_count.txt", "w", encoding="utf-8") as file:
        file.write(str(like_count))

    # Generate the HTML progress bar
    progress_bar = generate_progress_bar(like_count, like_goal)

    # Generate the HTML file with the progress bar
    with open("progress.html", "w", encoding="utf-8") as file:
        file.write(progress_bar)

    print("Like count and progress bar updated successfully.")

    # Check if ` key is pressed to force a check
    if keyboard.is_pressed('`'):
        print("Force check requested.")

    # Check if the like goal is reached
    if like_count >= like_goal:
        while True:
            update_choice = input("Like goal reached! Would you like to update the like goal? (Y/N): ")
            if update_choice.lower() == "y":
                while True:
                    new_goal = input("Enter the new like goal: ")
                    if new_goal.isdigit():
                        like_goal = int(new_goal)
                        break
                    else:
                        print("Invalid input. Please enter a valid number.")
                break
            elif update_choice.lower() == "n":
                break
            else:
                print("Invalid choice. Please enter 'Y' or 'N'.")

    # Delay for a certain period before checking again (e.g., 1 minute)
    time.sleep(60)
