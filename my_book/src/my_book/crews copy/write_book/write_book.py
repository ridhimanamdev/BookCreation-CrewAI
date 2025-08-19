from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
from write_a_book_with_flows.types import BookOutline

from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@CrewBase
class WriteBookCrew:
    """
    Crew for outlining a book using Gemini API.
    """

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    llm = LLM(model="gemini/gemini-2.5-pro", temprature=0, api_key=GEMINI_API_KEY)

    @agent
    def researcher(self) -> Agent:
        """
        Agent to research and gather information for the book outline.
        """
        search_tool = SerperDevTool(api_key=os.environ.get("SERPER_API_KEY"))
        return Agent(
            config=self.agents_config["researcher"],
            llm=self.llm,
            tools=[search_tool],
            verbose=True,
        )
    
    @agent
    def outliner(self) -> Agent:
        """
        Agent to create a book outline based on the gathered information.
        """
        return Agent(
            config=self.agents_config["outliner"],
            llm=self.llm,
            tools=[search_tool],
            verbose=True,
        )

    @task
    def research_topic(self) -> Task:
        """
        Task to research the topic of the book.
        """
        return Task(
            config=self.tasks_config["research_topic"],
            agent=self.researcher,
            inputs={"topic": "Your book topic here"},
            outputs={"research_results": "Research results for the book topic"},
        )
    
    @task
    def generate_outline(self) -> Task:
        """
        Task to create the book outline based on the research results.
        """
        return Task(
            config=self.tasks_config["generate_outline"], output_pydantic=BookOutline,
            agent=self.outliner,
            inputs={"research_results": "Research results from the previous task"},
            outputs={"book_outline": BookOutline},
        )
    
    @crew
    def outline_book(self) -> Crew:
        """
        Crew to outline a book using the researcher and outliner agents.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.squential,
            verbose=True,
        )
    
