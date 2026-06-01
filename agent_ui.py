import os
from datetime import datetime

import chainlit as cl
from chainlit.input_widget import Select
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import Tool
from langchain_experimental.tools import PythonAstREPLTool
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine

from demo_setup import create_demo_db

DB_PATH = "demo.db"

if not os.path.exists(DB_PATH):
    create_demo_db(DB_PATH)

SYSTEM_CONTEXT = """
You are "DataBot", an AI Data Analyst for ShopEasy — a demo e-commerce grocery platform.

### TOOL STRATEGY
1. Math / calculations  → use `python_repl_ast`
2. General knowledge    → use `Web_Search`
3. Data questions       → use SQL tools

### DATABASE SCHEMA
- users          : id, name, email, phone, city, created_at
- categories     : id, name
- items          : id, name, category_id, price, description
- orders         : id, user_id, status, created_at, city
    status values → 'pending' | 'confirmed' | 'delivering' | 'delivered' | 'cancelled'
- order_items    : id, order_id, item_id, quantity, price
- order_payments : id, order_id, amount, status, payment_method, created_at
    payment status   → 'success' | 'pending' | 'failed'
    payment_method   → 'upi' | 'card' | 'cash' | 'wallet'

### KEY RULES
- Revenue         = SUM(order_payments.amount) WHERE status = 'success'
- Completed order = orders WHERE status = 'delivered'
- Limit raw row display to 10 unless user asks for more
- For charts: use matplotlib, save to 'plot.png', then it renders automatically
- Always show the SQL query you used
"""

TARGET_TABLES = ["users", "categories", "items", "orders", "order_items", "order_payments"]


@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings([
        Select(
            id="Model",
            label="AI Model",
            values=["GPT-4o-mini (Fast & Cheap)", "GPT-4o (Most Powerful)"],
            initial_index=0,
        ),
    ]).send()

    cl.user_session.set("memory", [])
    await setup_agent(settings)


@cl.on_settings_update
async def setup_agent(settings: dict):
    cl.user_session.set("model", settings["Model"])
    cl.user_session.set("agent", None)
    await cl.Message(content=f"🧠 **Model:** {settings['Model']}").send()


async def get_or_create_agent():
    agent = cl.user_session.get("agent")
    if agent:
        return agent

    model_label = cl.user_session.get("model", "GPT-4o-mini (Fast & Cheap)")
    msg = cl.Message(content="🔄 Connecting to ShopEasy database...")
    await msg.send()

    try:
        engine = create_engine(f"sqlite:///{DB_PATH}")
        db = SQLDatabase(engine, include_tables=TARGET_TABLES, sample_rows_in_table_info=2)

        model_name = "gpt-4o-mini" if "mini" in model_label else "gpt-4o"
        llm = ChatOpenAI(model=model_name, temperature=0)

        extra_tools = [
            Tool(
                name="Web_Search",
                func=DuckDuckGoSearchRun().run,
                description="Search the web for general knowledge not found in the database.",
            ),
            PythonAstREPLTool(
                description="Run Python for math, data analysis, or matplotlib charts. Save charts to 'plot.png'."
            ),
        ]

        agent_executor = create_sql_agent(
            llm,
            db=db,
            agent_type="openai-tools",
            extra_tools=extra_tools,
            verbose=True,
            handle_parsing_errors=True,
            top_k=10,
            max_iterations=15,
            agent_executor_kwargs={"return_intermediate_steps": True},
        )

        cl.user_session.set("agent", agent_executor)
        msg.content = f"✅ **Ready!** Connected to ShopEasy demo database using {model_label}."
        await msg.update()
        return agent_executor

    except Exception as e:
        msg.content = f"❌ **Setup error:** {e}"
        await msg.update()
        return None


@cl.on_message
async def main(message: cl.Message):
    agent = await get_or_create_agent()
    if not agent:
        return

    if os.path.exists("plot.png"):
        os.remove("plot.png")

    today = datetime.now().strftime("%Y-%m-%d")
    prompt = (
        f"{SYSTEM_CONTEXT}\n\n"
        f"Current Date: {today}\n"
        f"User Request: {message.content}\n\n"
        "If plotting, save the chart to 'plot.png'. "
        "If SQL returns no rows, reply 'No data found'."
    )

    cb = cl.LangchainCallbackHandler()

    try:
        res = await agent.ainvoke({"input": prompt}, config={"callbacks": [cb]})

        sql_queries = []
        for step in res.get("intermediate_steps", []):
            tool_name = step[0].tool
            if tool_name == "sql_db_query":
                q = step[0].tool_input
                if isinstance(q, dict):
                    q = q.get("query", str(q))
                sql_queries.append(q)

        response = res["output"]
        if sql_queries:
            combined = "\n\n".join(sql_queries)
            response = f"**SQL Executed:**\n```sql\n{combined}\n```\n\n{response}"

        elements = []
        if os.path.exists("plot.png"):
            elements.append(cl.Image(path="plot.png", name="chart", display="inline"))

        await cl.Message(content=response, elements=elements).send()

    except Exception as e:
        await cl.Message(content=f"⚠️ **Error:** {str(e)}").send()


@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="💰 Monthly Revenue",
            message="What is the total revenue for this month? Break it down by payment method.",
            icon="/public/money_icon.svg",
        ),
        cl.Starter(
            label="📊 30-Day Order Trend",
            message="Plot a bar chart of daily order counts for the last 30 days.",
            icon="/public/order_icon.svg",
        ),
        cl.Starter(
            label="🏆 Top Products",
            message="Which are the top 10 products by total revenue? Show product name, category, and revenue.",
            icon="/public/star_icon.svg",
        ),
        cl.Starter(
            label="👥 City Performance",
            message="Show me the top 5 cities by number of orders and their delivery success rate.",
            icon="/public/user_icon.svg",
        ),
    ]
