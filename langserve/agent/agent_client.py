from langserve import RemoteRunnable
import asyncio

async def main():
    remote_runnable = RemoteRunnable("https://progressive-fionna-uh3135-d5472958.koyeb.app/")
    chat_history = []

    while True:
        human = input("Human (Q/q to quit): ")
        if human.lower() == "q":
            print('AI: Bye bye human')
            break
            
        ai = await remote_runnable.ainvoke({
            "input": human,
            "chat_history": chat_history
        })
        
        response = ai['output']
        print(f"AI: {response}")


if __name__ == "__main__":
    asyncio.run(main())