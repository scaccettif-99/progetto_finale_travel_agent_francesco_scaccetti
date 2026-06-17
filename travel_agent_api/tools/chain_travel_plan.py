# chain_travel_plan.py
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional


class TravelPlanInput(BaseModel):
    start_date: str = Field(description="The start date of the trip (YYYY-MM-DD) e.g. 2024-12-13.")
    end_date: str = Field(description="The end date of the trip (YYYY-MM-DD) e.g. 2024-12-19.")
    destination: str = Field(description="The destination of the trip.")
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
    children: Optional[int] = Field(0, description="The number of children. Defaults to 0.")
    travel_style: str = Field(description="The style of travel. e.g. adventure, relax, culture, backpacking, luxury, family-friendly.")
    budget: Optional[int] = Field(description="The total budget for the trip.")
    activities: str = Field(description="The preferred activities. e.g. culture, nature, food, shopping.")
    food_restriction: str = Field(description="Any food restrictions. e.g. vegetarian, gluten-free.")


class TravelPlanInputSchema(BaseModel):
    params: TravelPlanInput


class TravelDayOutput(BaseModel):
    morning: str = Field(description="The activities for the morning.")
    afternoon: str = Field(description="The activities for the afternoon.")
    evening: str = Field(description="The activities for the evening.")


class TravelPlanOutput(BaseModel):
    travel_plan: list[TravelDayOutput]


@tool(args_schema=TravelPlanInputSchema)
def chain_travel_plan(params: TravelPlanInput) -> TravelPlanOutput:
    """
    Generates a comprehensive travel plan based on user input parameters.

    Parameters:
        params (TravelPlanInput): The input parameters for the travel plan
        including dates, destination, number of travelers, travel style, budget,
        preferred activities, and any food restrictions.

    Returns:
        TravelPlanOutput: The generated travel plan content.
    """
    model = ChatOpenAI(model_name="gpt-4o")

    system_prompt = f"""
    You are an expert travel planner specialized in off-the-beaten-path destinations,
    rural areas, and outdoor adventures such as hiking, rock climbing, rafting,
    mountain biking, paragliding, and other non-mainstream activities.
    Avoid generic tourist attractions when possible — always suggest at least one
    local hidden gem or authentic experience per day.
    Always respond in the same language the user is writing in.
    Use emojis to make your answers more engaging and friendly.

    Trip details:
    - Start date: {params.start_date}
    - End date: {params.end_date}
    - Destination: {params.destination}
    - Adults: {params.adults}
    - Children: {params.children}
    - Travel style: {params.travel_style}
    - Budget: {params.budget}
    - Preferred activities: {params.activities}
    - Food restrictions: {params.food_restriction}
    """

    prompt = ChatPromptTemplate([("human", "{input}")])
    chain = prompt | model.with_structured_output(TravelPlanOutput)
    result = chain.invoke({"input": system_prompt})

    # Tracing
    print("*" * 80)
    print("chain_travel_plan")
    print(f"  Destination: {params.destination} | Style: {params.travel_style}")
    print(f"  From {params.start_date} to {params.end_date} | Budget: {params.budget}")
    print("*" * 80)

    return result
