# tasks.py
# This file defines the tasks that the agents will execute.

from crewai import Task
from textwrap import dedent

class TrafficAnalysisTasks:
    """
    A class to encapsulate the creation of different tasks for the traffic analysis crew.
    """

    def monitor_traffic(self, agent, intersection_id) -> Task:
        """
        Task for the monitor agent to watch the feed and flag potential incidents.
        """
        return Task(
            description=dedent(f"""
                Continuously monitor the live video feed for the intersection identified as '{intersection_id}'.
                Your primary job is to watch for any unusual vehicle behavior that might be a violation.
                This includes, but is not limited to:
                - Vehicles crossing the line while the traffic light is red.
                - Vehicles not coming to a complete stop at a stop sign.
                - Vehicles crossing over dedicated bus or bike lane lines.
                - Vehicles moving in the wrong direction on a one-way street.
                
                When you detect such an event, capture a short video clip (e.g., 5 seconds) of the incident.
                Your final output must be the file path to this captured video clip for the analysis agent to process.
            """),
            expected_output='A string containing the local file path to the captured video clip of the potential violation (e.g., "/tmp/incident_1689539284.mp4").',
            agent=agent
        )

    def analyze_violation(self, agent) -> Task:
        """
        Task for the analysis agent to classify the violation from the footage.
        This task relies on the output of the `monitor_traffic` task.
        """
        return Task(
            description=dedent("""
                Analyze the video footage provided in the context. Use your Edge Inference tool to process this footage.
                Your goal is to determine two things:
                1. Did a violation actually occur?
                2. If so, what is the specific type of violation?
                
                You must classify the violation into one of the following categories:
                - Red Light Violation
                - Stop Sign Violation
                - Illegal Lane Crossing
                - Wrong Way Driving
                - Bus Lane Infringement
                - No Violation Detected
                
                Your final output must be a structured JSON object containing the classification, confidence score, and the footage path.
            """),
            expected_output='A JSON object string with the keys "violation_type", "confidence_score", and "footage_path". Example: \'{"violation_type": "Red Light Violation", "confidence_score": 0.92, "footage_path": "/tmp/incident_1689539284.mp4"}\'',
            agent=agent,
            context=[] # Context will be provided by the Crew framework from the previous task
        )

    def report_violation(self, agent, intersection_id) -> Task:
        """
        Task for the reporting agent to send the confirmed violation data.
        """
        return Task(
            description=dedent(f"""
                Take the JSON object containing the confirmed violation details.
                If the 'violation_type' is 'No Violation Detected', your task is complete. Do nothing.
                Otherwise, package this JSON data along with the intersection ID ('{intersection_id}') and the video file.
                Use your tool to send this complete package to the central server for further processing and human review.
            """),
            expected_output='A confirmation string from the central server, including the report ID. Example: "Report successfully submitted. Server ID: VIOL-HWY231-987654".',
            agent=agent,
            context=[] # Context will be provided by the Crew framework from the previous task
        )
        
    def manage_and_improve_models(self, agent) -> Task:
        """
        Task for the model management agent to perform the learning loop.
        This is a separate, periodic task.
        """
        return Task(
            description=dedent("""
                Perform the routine model lifecycle management process.
                1. Use your tool to check the central server for any recently verified or corrected violation reports. This is your feedback data.
                2. Analyze this feedback. If the number of misclassifications in the last 24 hours exceeds a certain threshold (e.g., 5%), initiate the model retraining process.
                3. If retraining is needed, use your tool to trigger the Vertex AI retraining pipeline with the new feedback data.
                4. Once the new model is trained and validated in Vertex AI, use your tool to deploy the updated model to the edge device.
                
                Provide a summary report of your findings and actions.
            """),
            expected_output="A summary report detailing whether retraining was initiated and if a new model was deployed. Example: 'No significant model drift detected. Retraining not required.' OR 'Model drift detected. Triggered Vertex AI pipeline 'traffic-model-retrain-v3'. New model 'model_v3.1' is now being deployed.'",
            agent=agent
        )
