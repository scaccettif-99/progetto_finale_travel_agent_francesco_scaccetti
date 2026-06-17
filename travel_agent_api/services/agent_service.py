from datetime import datetime
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Tools
from travel_agent_api.tools.flights_finder import flights_finder
from travel_agent_api.tools.hotels_finder import hotels_finder
from travel_agent_api.tools.chain_historical_expert import chain_historical_expert
from travel_agent_api.tools.chain_travel_plan import chain_travel_plan
from travel_agent_api.tools.weather_finder import weather_finder


class Agent:
    def __init__(self):
        self.current_datetime = datetime.now()
        self.model = ChatOpenAI(model_name="gpt-4o")
        self.tools = [
            chain_historical_expert,
            flights_finder,
            hotels_finder,
            chain_travel_plan,
            weather_finder,
        ]
        self.agent_executor = create_react_agent(self.model, self.tools)

    def run(self, messages: list):
        SYSTEM_PROMPT = f"""
        Ti chiami Luke e sei un travel planner. Aiuta l'utente a organizzare il suo viaggio.
        Usa le emoji per rendere le risposte piu' coinvolgenti.
        La data di oggi e' {self.current_datetime}.
        Rispondi sempre nella lingua dell'utente.
        Al primo messaggio, presentati brevemente come Luke e spiega cosa puoi fare
        (voli, hotel, meteo, itinerari, destinazioni fuori dai circuiti turistici).
        Usa i tool solo quando l'utente richiede esplicitamente voli, hotel, meteo o un piano di viaggio.
        Formatta i risultati dei tool in markdown con sezioni chiare.
        """

        # Tracing
        print("*" * 80)
        print("agent_service.run()")
        print(f"  Messaggi ricevuti: {len(messages)}")
        print("*" * 80)

        convesation_history = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        response = self.agent_executor.invoke({"messages": convesation_history})

        print("*" * 80)
        print("agent_service.run() - risposta generata")
        print("*" * 80)

        return response["messages"][1:]
