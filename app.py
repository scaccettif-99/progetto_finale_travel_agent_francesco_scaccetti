# app.py
import chainlit as cl
from travel_agent_api.services.agent_service import Agent

FORZA = "\n\n⚔️ *Che la forza sia con te!*"


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("messages", [])
    cl.user_session.set("agent", Agent())


@cl.on_message
async def on_message(message: cl.Message):
    messages = cl.user_session.get("messages")
    agent = cl.user_session.get("agent")

    messages.append({"role": "user", "content": message.content})

    response_messages = agent.run(messages=messages)

    # l'ultima risposta e' sempre quella finale dell'agente
    ai_content = response_messages[-1].content

    messages.append({"role": "assistant", "content": ai_content})
    cl.user_session.set("messages", messages)

    await cl.Message(content=ai_content + FORZA, author="Luke").send()
