from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever
from export import ExportManager

model = OllamaLLM(model="llama3.2")
export_manager = ExportManager()

template = """
You are a helpful assistant.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

print("\n" + "="*50)
print("LOCAL AI AGENT - RESTAURANT CHATBOT")
print("="*50)
print("Commands: help, export txt, export pdf, clear, q\n")

while True:
    question = input("Question (or 'help'): ").strip()
    
    if question.lower() == "q":
        break
    elif question.lower() == "help":
        print("export txt - Export to text\nexport pdf - Export to PDF\nclear - Clear history\nq - Quit")
        continue
    elif question.lower() == "export txt":
        export_manager.export_to_text()
        continue
    elif question.lower() == "export pdf":
        export_manager.export_to_pdf()
        continue
    elif question.lower() == "clear":
        export_manager.clear_history()
        continue
    elif not question:
        continue

    try:
        reviews = retriever.invoke(question)
        answer = chain.invoke({"reviews": reviews, "question": question})
        export_manager.add_conversation(question, reviews, answer)
        print(f"\n{answer}\n")
    except Exception as e:
        print(f"Error: {e}\n")

print("Thank you! 👋")


