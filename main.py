# main.py
# This is the main entry point for the application.
# To run the crew, execute: `crewai run main.py` in your terminal.

from agents import TrafficAnalysisAgents
from tasks import TrafficAnalysisTasks

from crewai import Crew, Process

# Instantiate the agents and tasks
agents = TrafficAnalysisAgents()
tasks = TrafficAnalysisTasks()

# Define the specific intersection this crew is responsible for
intersection_id = "CROSSROAD_HWY_231_MAIN_ST"

# Instantiate the agents
monitor_agent = agents.traffic_monitor_agent()
analysis_agent = agents.violation_analysis_agent()
reporting_agent = agents.reporting_agent()
model_management_agent = agents.model_management_agent()

# Instantiate the tasks
monitor_task = tasks.monitor_traffic(monitor_agent, intersection_id)
analyze_task = tasks.analyze_violation(analysis_agent)
report_task = tasks.report_violation(reporting_agent, intersection_id)

# Assemble the main operational crew
# This crew handles the primary flow: monitor -> analyze -> report
traffic_crew = Crew(
    agents=[monitor_agent, analysis_agent, reporting_agent],
    tasks=[monitor_task, analyze_task, report_task],
    process=Process.sequential,
    verbose= True
)

def run_crew():
    """
    Kicks off the main operational crew to perform one cycle of monitoring and reporting.
    In a real-world scenario, this function would be triggered by a scheduler
    (e.g., running every few seconds) or a continuous loop.
    """
    print(f"🚀 Starting Traffic Violation Crew for Intersection: {intersection_id}")
    
    # The `inputs` dictionary can be used to pass initial data to the first task.
    # Here, we're assuming the `monitor_traffic` task will use its tool to get the latest data.
    result = traffic_crew.kickoff()
    
    print("\n✅ Crew execution finished. Result:")
    print(result)

if __name__ == "__main__":
    run_crew()
    
    # --- Example of Triggering the Learning Loop ---
    # In a real system, this would be triggered by a separate process,
    # perhaps a nightly job or after receiving feedback from human reviewers.
    #
    # print("\n🔄 Kicking off the model management task for periodic check...")
    # learning_crew = Crew(
    #     agents=[model_management_agent],
    #     tasks=[tasks.manage_and_improve_models(model_management_agent)],
    #     verbose=2
    # )
    # learning_result = learning_crew.kickoff()
    # print("\n✅ Model management task finished. Result:")
    # print(learning_result)

