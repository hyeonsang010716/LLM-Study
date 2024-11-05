from langchain_community.llms import Ollama
ollama = Ollama(
    base_url='http://localhost:11434',
    model="llama3.2"
)

answer = ollama.invoke("why is the sky blue")

print(answer)
# print(type(answer))
