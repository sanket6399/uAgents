import logging
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from utils import get_job_summary, send_whatsapp_message

# Set up logging
logging.basicConfig(level=logging.INFO)

class Request(Model):
    query: str


class Response(Model):
    response: str


SearchAgent = Agent(
    name="SearchAgent",
    port=8000,
    seed="google searchhikbjjvhiyh",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(SearchAgent.wallet.address())


@SearchAgent.on_event("startup")
async def agent_details(ctx: Context):
    ctx.logger.info(f"Search Agent Address is {SearchAgent.address}")


@SearchAgent.on_query(model=Request, replies={Response})
async def query_handler(ctx: Context, sender: str, msg: Request):
    ctx.logger.info("Query received")
    try:
        ctx.logger.info(f"Fetching job details for query: {msg.query}")
        response = await get_job_summary(
            msg.query, "United Kingdom"
        )
        ctx.logger.info(f"Response: {response}")
        
        # Send the response via WhatsApp
        whatsapp_sid = await send_whatsapp_message("Checking whatsapp message delivery")
        ctx.logger.info(f"WhatsApp message sent with SID: {whatsapp_sid}")
        
        # Send response back to the agent
        await ctx.send(sender, Response(response=response))

    except Exception as e:
        error_message = f"Error fetching job details: {str(e)}"
        ctx.logger.error(error_message)
        
        # Send the error message via WhatsApp
        await send_whatsapp_message(error_message)


if __name__ == "__main__":
    SearchAgent.run()
