# Create the markdown content as a string
readme_content = """# CitizenPulse

CitizenPulse is an AI powered civic intelligence platform built to help city authorities manage public complaints more effectively. In large cities like Delhi, thousands of reports about roads, water, and pollution are filed daily. This system automatically organizes these reports, identifies urgent problems, and helps officers focus on what matters most.

## The Problem

Citizens face many issues with traditional systems:
* Complaints are often scattered across different places
* Many people report the exact same issue which creates extra work
* It is hard for authorities to know which problem is the most urgent

## The Solution

CitizenPulse automates the entire process to make it faster and smarter:
* Smart Grouping: The system uses AI to understand the meaning of a complaint and group it with similar ones.
* Urgency Scoring: Each group of issues gets a priority score that increases as more people report it.
* Live Officer Dashboard: Authorities see a clear list of problems sorted by urgency.
* Geospatial Heatmap: A visual map shows where most issues are happening in the city.

## Key Features

* Semantic AI Clustering: Groups complaints by their actual meaning rather than just keywords.
* Interactive Heatmap: Uses maps to track problem hotspots in real time.
* Automated Updates: Notifies citizens via email once their issue is resolved.
* Modern Interface: A clean and responsive design for both citizens and government staff.

## Project Structure

The project is divided into two main parts:

### Backend
* main.py: The main entry point for the server.
* schema.py: Defines the structure of the data.
* init_db.py: Sets up the database for the first time.
* requirements.txt: Lists all the software needed to run the backend.
* codee.py: Contains the logic for processing complaints.

### Frontend
* Components: Includes parts like the Admin Dashboard, Citizen Form, Landing Page, and Login Form.
* Assets: Stores images such as the project flowchart and background.
* API: Handles the communication between the website and the server.
* Districts: Contains data related to different city regions.

## Technology Stack

### Frontend
* React and TypeScript
* Vite for fast performance
* Leaflet.js for maps

### Backend
* FastAPI for the server logic
* SQLite for storage
* JWT for secure login

### Artificial Intelligence
* Google Gemini Flash 2.0 for advanced text analysis
* Sentence Transformers specifically all MiniLM L6 v2 for grouping similar complaints

## How It Works

1. Submit: A citizen fills out a form to report an issue.
2. Process: The AI analyzes the text and compares it to existing complaints.
3. Group: If the issue is already known, it is added to an existing group. If it is new, a new group is made.
4. Prioritize: The system gives the group a priority level based on the type of issue and frequency.
5. Resolve: Officers use the dashboard to address the problem and mark it as finished.
6. Notify: An automatic email is sent to the citizen to let them know the work is done.

## Installation

### For the Backend
* Open the backend folder
* Install the packages listed in the requirements file
* Run the initialization script to prepare the database
* Start the server

### For the Frontend
* Open the frontend folder
* Install the necessary dependencies
* Start the development server to view the website

## Impact

CitizenPulse turns messy data into clear insights. By grouping issues together, it allows authorities to solve one major problem instead of handling hundreds of separate tickets. This leads to faster repairs, better use of public money, and happier citizens. This project was developed as a hackathon project in 2026.
