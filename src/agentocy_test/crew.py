from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
# My imports
from pydantic import BaseModel, Field
from typing import List
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from dotenv import load_dotenv

load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class SocialMediaPost(BaseModel):
    platform: str = Field(..., description="The social media platform where the post will be published (e.g., Twitter, LinkedIn).")
    content: str = Field(..., description="The content of the social media post, including any hashtags or mentions.")

class ContentOutput(BaseModel):
    article: str = Field(..., description="The article, formatted in markdown.")
    social_media_posts: List[SocialMediaPost] = Field(..., description="A list of social media posts related to the article.")

@CrewBase
class AgentocyTest():
	"""ContentCreationAtScale crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def market_news_monitor_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['market_news_monitor_agent'],
   			tools=[SerperDevTool(n_results=5), ScrapeWebsiteTool()],
			verbose=True
		)

	@agent
	def data_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['data_analyst_agent'],
			tools=[SerperDevTool(n_results=5), WebsiteSearchTool()], # WebsiteSearchTool() - Performs RAG searches
			verbose=True,
		)
  
	@agent
	def content_creator_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['content_creator_agent'],
			tools=[SerperDevTool(n_results=5), WebsiteSearchTool()],
			verbose=True
		)
  
	@agent
	def quality_assurance_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['quality_assurance_agent'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def monitor_news(self) -> Task:
		return Task(
			config=self.tasks_config['monitor_news'],
		)

	@task
	def analyze_market_data(self) -> Task:
		return Task(
			config=self.tasks_config['analyze_market_data'],
		)
  
	@task
	def create_content(self) -> Task:
		return Task(
			config=self.tasks_config['create_content'],
		)
  
	@task
	def quality_assurance(self) -> Task:
		return Task(
			config=self.tasks_config['quality_assurance'],
			output_pydantic=ContentOutput
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the ContentCreationAtScale crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
 
 
	# @crew
	# def crew(self) -> Crew:
	# 	"""Creates the ContentCreationAtScale crew"""
	# 	# To learn how to add knowledge sources to your crew, check out the documentation:
	# 	# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

	# 	result = Crew(
	# 		agents=self.agents, # Automatically created by the @agent decorator
	# 		tasks=self.tasks, # Automatically created by the @task decorator
	# 		process=Process.sequential,
	# 		verbose=True,
	# 		# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
	# 	)
	
	# 	print(f"RESULT:::>>>{result}")

