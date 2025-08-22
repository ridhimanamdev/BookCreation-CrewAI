import asyncio
from typing import List
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from write_a_book_with_flows.crew.write_book_chapter_crew.write_book_chapter_crew import (WriteBookChapterCrew)
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
        output=(
            OutlineCrew()
            ,crew()
            ,kickoff(input={"topic": self.topic, "goal": self.goal})
        )


        chapter = output["chapter"]
        print ("Chapter:", chapter)

        self.state.book_outline = chapters
        return chapters
    
    @listen(generate_book_outline)
    async def write_chapters(self):
        print("Kick off the WriteBookChapterCrew and Writing book chapters...")
        tasks = []

        async def write_single_chapter(chapter_outline):
            output = (
                WriteBookChapterCrew(), 
                crew(),
                kickoff(input=
                        {
                            "goal": self.state.goal,
                            "topic": self.state.topic,
                            "chapter_title": chapter_outline.title,
                            "chapter_description": chapter_outline.description,
                            "book_outline": [
                                chapter_outline.model_dump_json()
                                for chapter_outline in self.state.book_outline
                            ],
                        }
                    ) 
                )
            title = output["title"]
            content= output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter
        
        for chapter_outline in self.state.book_outline:
            print(f"Writing chapter: {chapter_outline.title}")
            print(f"Chapter description: {chapter_outline.description}")
            #Schedule the writing of each chapter

            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        #await for all chapter writing tasks to complete
        chapters = await asyncio.gather(*tasks)
        print("Newly generated chapters:", chapters)
        self.state.book.extend(chapters)

        print ("Book Chapters:", self.state.book)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        print("Joining and saving chapters...")
        # Here you can implement the logic to join and save the chapters
        # For example, you can save them to a file or database
        book_content = ""

        for chapter in self.state.book:
            book_content += f"Chapter: {chapter.title}\n"
            book_content += f"Content: {chapter.content}\n\n"

        book_title =self.state.title
        filename = f"{book_title.replace(' ', '_')}.md"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(book_content)
        print(f"Book saved as {filename}")
        return book_content

def kickoff(input: dict):
    """
    Kick off the flow with the provided input.
    """
    poem_flow = BookFlow()
    poem_flow.kickoff()

def plot():
    poem_flow = BookFlow()
    poem_flow.plot()

if __name__ == "__main__":
    kickoff()

