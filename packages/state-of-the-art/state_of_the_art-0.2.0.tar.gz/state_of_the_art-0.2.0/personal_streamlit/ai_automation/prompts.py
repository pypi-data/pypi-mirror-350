

from state_of_the_art.utils.llm.llm import LLM


class DefineTopic:

    def define(self, topic: str):
        prompt = f"""You are expert in '{{text}}'

Help me to get on top of the topic as well by giving me an overview of what is important.

Make sure to mention as well:
- What it is? What is its purpose, or mission (if applicable)?
- What are must knowns? 
- What are key pitfall areas etc?
- What are must reads or in this area (books, papers, etc. and how long they are) or resources like websites, audio, video, etc.
- Cite examples when applicable
- What are classical, foundational works in this area (books, papers, etc. and how long they are)
- What are the current state of the art and future directions
- Key companies, people, universities, etc.
"""

        llm = LLM()
        result = llm.call(prompt, topic)
        return result


    def related_topics(self, topic: str):
        prompt = f"""You are expert in the {{text}} field.

Return a list of related topics that are related to the following topic or go deeper into the topic: {topic}
Return no more than 15 topics.
"""

        llm = LLM()
        result = llm.call(prompt, topic)
        return result

class GermanDefition:

    def define(self, topic: str):
        prompt = f"""You are expert in german and english.

Translate the following text from one language to the other:

{{text}}

Return the translated text.
Also give more context to the topic but keep it short.
Give 1 or 2 examples of how it can be used and more details at b2 level.
if the word is a compound word, explain the meaning of each subword.
if there is likelly a misspelling flag it.
"""

        print("Calling LLM")
        llm = LLM()
        result = llm.call(prompt, topic)
        return result

class GermanEmail:

    def compose(self, topic: str):
        prompt = f"""You are an assistant that helps to write an  a formal email in german

I enter an input and you help to write an email in german
My name is Jean Machado 

{{text}}


Write below the email a translation into english.
"""

        llm = LLM()
        result = llm.call(prompt, topic)
        return result

class LearnEfficiently:

    def give_advice(self, topic: str):
        prompt = f"""You are an expert in learning efficiently.

You give mea advice on how to learn efficiently.
What are fundamental books and papers?
What is the state of the art?
What are the key concepts?
What are the key companies, people, universities, etc.
What are famous courses?
How to be engaged with the community around the topic?
What are the best open source projects?
WHat are key terms and what is the meaning of them?

For the topic: {{text}}
"""

        llm = LLM()
        result = llm.call(prompt, topic)
        return result
