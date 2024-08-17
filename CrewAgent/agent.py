from crewai import Agent

def create_researcher(tools):
    return Agent(
        role='Read the content of {topic}',
        goal='{prompt}',
        verbose=True,
        memory=True,
        backstory='Expert in understanding that {topic}',
        tools=[tools],
        allow_delegation=True
    )
