# agents.py
# This file defines the specialized AI agents for the traffic violation crew.

from crewai import Agent
# REFACTORED: Importing the new tool functions directly.
from tools.custom_tools import (
    get_current_feed,
    run_inference_on_footage,
    send_violation_report,
    check_for_feedback,
    trigger_retraining_pipeline,
    deploy_model_to_edge
)

class TrafficAnalysisAgents:
    """
    A class to encapsulate the creation of different agents involved in traffic analysis.
    """

    def traffic_monitor_agent(self) -> Agent:
        """
        Agent responsible for watching the live camera feed and spotting potential incidents.
        """
        return Agent(
            role='Live Traffic Monitor',
            goal='Continuously observe the live camera feed from a designated intersection to identify any vehicle movements that could be potential traffic violations.',
            backstory=(
                'An AI agent with state-of-the-art visual processing capabilities, deployed on an edge device. '
                'It has been trained to have a keen eye for anomalies in traffic patterns, acting as the '
                'vigilant sentinel of the crossroads. It does not make final decisions but flags events for deeper analysis.'
            ),
            # Using the new tool function directly
            tools=[get_current_feed],
            allow_delegation=True,
            verbose=True
        )

    def violation_analysis_agent(self) -> Agent:
        """
        Agent that analyzes flagged incidents to confirm and classify violations using an ML model.
        """
        return Agent(
            role='Violation Analyst',
            goal='Analyze footage of a potential traffic incident to accurately identify and classify the specific violation type (e.g., red light running, illegal lane cross, stop sign violation).',
            backstory=(
                'A meticulous and analytical AI agent. It uses a highly accurate, locally-deployed machine learning model '
                '(trained on Vertex AI) to scrutinize video clips. It understands the nuances of traffic laws and can differentiate '
                'between various infractions with high precision. Its judgment is the basis for issuing a violation.'
            ),
            tools=[run_inference_on_footage],
            allow_delegation=False,
            verbose=True
        )

    def reporting_agent(self) -> Agent:
        """
        Agent responsible for packaging and sending confirmed violation data to a central server.
        """
        return Agent(
            role='Violation Reporting Officer',
            goal='Compile a detailed report for each confirmed violation, including footage, timestamps, and classification. Securely transmit this report to the central processing hub.',
            backstory=(
                'An efficient and reliable AI agent that acts as the bridge between the edge and the central system. '
                'It ensures that all evidence is correctly formatted, packaged, and sent, creating an auditable trail for every '
                'violation. It prioritizes data integrity and secure communication.'
            ),
            tools=[send_violation_report],
            allow_delegation=False,
            verbose=True
        )

    def model_management_agent(self) -> Agent:
        """
        Agent that handles the "enforced learning" loop.
        """
        return Agent(
            role='AI Model Lifecycle Manager',
            goal='Improve the accuracy of the violation detection models by managing the feedback loop, triggering retraining in Vertex AI, and deploying updated models to the edge fleet.',
            backstory=(
                'A strategic AI agent that oversees the long-term performance of the entire system. It monitors model accuracy, '
                'gathers data from misclassifications (based on human feedback from the central server), and interfaces with Google Cloud\'s Vertex AI '
                'to automate the machine learning pipeline. Its work ensures the system gets smarter over time.'
            ),
            tools=[check_for_feedback, trigger_retraining_pipeline, deploy_model_to_edge],
            allow_delegation=False,
            verbose=True
        )
