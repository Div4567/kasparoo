from ollama_client import chat

def run_loop():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    print("Type a message (Ctrl+C to quit).")
    try:
        while True:
            user = input("User: ").strip()
            if not user:
                continue
            messages.append({"role": "user", "content": user})
            reply = chat(messages, model="qwen2.5:3b", temperature=0.2)
            print("Assistant:", reply)
            messages.append({"role": "assistant", "content": reply})
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    run_loop()