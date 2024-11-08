from pychatgpt import ChatGPT

chat = ChatGPT(headless=False)
while True:
    res = chat.predict("Generate 100 words paragraph please")
    print("final response:", res["response"])
    input()