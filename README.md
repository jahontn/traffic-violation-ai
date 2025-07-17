Agentic AI Traffic Violation Detection Crew
This project demonstrates a robust, multi-agent AI system for detecting, classifying, and reporting traffic violations in real-time. It is built using the CrewAI framework and is designed to be deployed on edge devices, such as those connected to cameras at traffic intersections.

The system processes video feeds locally to ensure low latency and minimize data transfer, only sending confirmed violation footage to a central server for further action.

Core Features
Edge-First Processing: All initial video analysis is performed directly on the edge device, ensuring immediate response times and efficient use of network bandwidth.

Agentic Workflow: The problem is decomposed into specialized roles handled by distinct AI agents, creating a clear, modular, and powerful workflow.

Traffic Monitor: The spotter, watching for potential incidents.

Violation Analyst: The expert, using an ML model to confirm and classify violations.

Reporting Officer: The dispatcher, sending confirmed evidence to a central hub.

Model Manager: The trainer, responsible for the long-term improvement of the system.

Enforced Learning Loop: The architecture includes an agent dedicated to a continuous improvement cycle. It can be configured to use feedback from human reviewers to trigger retraining pipelines in Google Cloud's Vertex AI and deploy updated models back to the edge fleet.

Modular & Extensible Tools: The agents' capabilities (camera access, model inference, API calls) are defined in a separate tools directory, making it easy to integrate with your specific hardware and infrastructure.

How It Works
The primary operational flow is managed by a sequential crew that executes the following tasks:

Monitor Traffic: The Traffic Monitor agent uses the Live Camera Feed Tool to watch the video stream. When it detects a potential incident (e.g., a car running a red light), it captures a short video clip.

Analyze Violation: The captured clip is passed to the Violation Analyst agent. This agent uses the Edge AI Inference Tool (which would load a custom-trained model) to determine if a violation occurred and, if so, to classify its type (e.g., "Red Light Violation", "Stop Sign Violation").

Report Violation: If a violation is confirmed, the analysis results and video footage are passed to the Violation Reporting Officer. This agent uses the Central Server API Tool to package and transmit the evidence to a central processing hub. If no violation is detected, the process stops, and the temporary footage is discarded.

Project Structure
/traffic_violation_crew
|
├── .venv/                    # Virtual environment
├── main.py                   # Main entry point to run the crew
├── agents.py                 # Defines the roles and goals of each agent
├── tasks.py                  # Defines the specific tasks for the agents
├── pyproject.toml            # Project configuration and dependencies
|
└─── /tools
    ├── __init__.py
    └── custom_tools.py       # Implementations of tools for camera, AI models, etc.

Getting Started
Follow these steps to set up and run the project on your local machine.

1. Prerequisites

Python 3.10 or higher

2. Clone the Repository

git clone <your-repository-url>
cd traffic_violation_crew

3. Set Up the Environment
The project is configured to use uv and a pyproject.toml file for environment management. The crewai command will handle this automatically.

4. Run the Crew
Execute the main crew with the following command:

crewai run

This command will:

Create a local virtual environment (.venv).

Install all the required dependencies from pyproject.toml.

Execute the run_crew function in main.py.

You will see verbose output in your terminal as the agents execute their tasks in sequence.

Adapting for Real-World Use
The tools in tools/custom_tools.py are currently simulations. To deploy this system, you will need to replace the placeholder logic with real implementations:

get_current_feed(): Modify this function to use a library like OpenCV (cv2) to connect to a real camera's RTSP stream and capture video clips.

run_inference_on_footage(): Integrate your custom-trained machine learning model (e.g., a TensorFlow Lite .tflite or ONNX file) to perform inference on the video clips captured by the camera tool.

send_violation_report(): Update this function to make a real HTTP POST request to your central server's API endpoint, uploading the violation data and footage.

Vertex AI Tools: Implement the functions to make actual API calls to the Google Cloud AI Platform using the google-cloud-aiplatform client library.
