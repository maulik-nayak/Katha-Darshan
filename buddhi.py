import ollama
from ahamkar import ASSISTANT_PROFILE
from aatma import add_memory, get_relevant_memories
from actions import handle_action

short_term_memory = []

def think(user_input):
    global short_term_memory

    # 1. Deterministic actions first
    action_result = handle_action(user_input)
    if action_result:
        return action_result

    # 2. Add to short term memory
    short_term_memory.append({"role": "user", "content": user_input})

    # 3. Retrieve long-term summaries
    past_memories = get_relevant_memories()

    system_prompt = f"""
You are {ASSISTANT_PROFILE['name']}.

Speak concisely.
If user input is short, respond in 1 or 2 sentences maximum.
Do not ramble.
Be precise.

Relevant past memories:
{past_memories}
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(short_term_memory)

    response = ollama.chat(
        model=ASSISTANT_PROFILE["model"],
        messages=messages,
        options={
            "temperature": ASSISTANT_PROFILE["temperature"],
            "num_predict": ASSISTANT_PROFILE["max_tokens"]
        }
    )



    reply = response["message"]["content"]

    short_term_memory.append({"role": "assistant", "content": reply})

    # 4. Consolidate memory if too long
    if len(short_term_memory) > ASSISTANT_PROFILE["short_term_limit"]:
        summarize_and_store()

    return reply

def warmup():
    ollama.chat(
        model=ASSISTANT_PROFILE["model"],
        messages=[{"role": "user", "content": "Hi"}],
        options={"num_predict": 1}
    )

def summarize_and_store():
    global short_term_memory

    text_block = "\n".join(
        [f"{m['role']}: {m['content']}" for m in short_term_memory[:5]]
    )

    summary_prompt = f"Summarize this conversation briefly:\n{text_block}"

    summary = ollama.chat(
        model=ASSISTANT_PROFILE["model"],
        messages=[{"role": "user", "content": summary_prompt}]
    )["message"]["content"]

    add_memory(summary)

    short_term_memory = short_term_memory[5:]