from crewai import Crew, Process

def create_crew(researcher, research_task):
    return Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        memory=True,
        cache=True,
        max_rpm=100,
        share_crew=True
    )
