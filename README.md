PROGETTO FINALE FRANCESCO SCACCETTI 
TRAVEL AGENT

- Progetto inizializzato con e dipendenze scaricate correttamente

- Creato main e chat_router

- Sistemata struttura del progetto

- Completato chat_router.py

- creato il file flights_finder

- creato il file hotels_finder

- creato il file chain_travel_plan

- creato il file chain_historical_expert

- creata cartella services con agent_service.py

- modificato il system_prompt con un messaggio di benvenuto personalizzato

- dato il comando poetry run uvicorn travel_agent_api.main:app --reload --port8080 per verificare il corretto funzionamento

- progetto corretto con le indicazioni date in revisione, quindi system prompt semplificato evitando anche tool-call inutili che provocavano latenza

-PydanticOutputParser richiedeva che nel prompt ci fosse {format_instructions}, affinchè il modello risponda in JSON. Quindi sostituito con model.with_structured_output(TravelPlanOutput).

- implementato nuovo tool meteo

- Installato chainlit per portare l'agent su una chat

- agent personalizzato come Luke Skywalker

- personalizzato css di chainlit con colori e icone

- progetto completato

