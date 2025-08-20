import asyncio
from typing import List
from crewai.flow.flow import flow, listen, Start
from pydantic import BaseModel
from write_a_book_with_flows.crew.write_book_chapter_crew.write_book_chapter_crew import (WriteBookChapterCrew,)
from write_a_book_with_flows.types import Chapter, ChapterOutline
from write_a_book_with_flows.crew.outline_book_crew.outline_book_crew import OutlineCrew

class BookState(BaseModel):
    id: str="1"
    title: str="The Current State of AI"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = ("Exploring the Latest Impact of AI across different industries in 2025 and its Future Prospects")
    
    goal: str = """The goal of this book is to provide a comprehensive overview of the current state of AI, its applications across various industries, and its future prospects. 
    The book will explore how AI is transforming industries such as healthcare, finance, transportation, and more, while also addressing the ethical implications and challenges associated with its rapid advancement.
    The book aims to educate readers about the potential of AI, its benefits, and the challenges it poses, ultimately providing a balanced perspective on this transformative technology and preparing them for the future of AI."""


class BookFlow(BookState):
    initial_state = BookState
    """
    Flow for writing a book using the WriteBookChapterCrew and OutlineCrew.
    """
    @start()
    def generate_book_outline(self):
        """
        Start the book writing flow by generating the book outline.
        """
        print("Kick off the Book Outline Crew and Generating book outline...")
        output=(OutlineCrew(), crew(), kickoff(input={"topic": self.topic, "goal": self.goal}))


        chapter = output["chapter"]
        print ("Chapter:", chapter)

        self.state.book_outline = chapters
        return chapters
    
    @listen(generate_book_outline)
    async def write_chapters(self):
        print("Kick off the WriteBookChapterCrew and Writing book chapters...")
    
