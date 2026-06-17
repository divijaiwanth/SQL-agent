import os
from dotenv import load_dotenv

# Load environment variables before anything else
load_dotenv()

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from model import model

# 1. Connect to the SQLite Database
db_path = "Chinook.db"
if not os.path.exists(db_path):
    print(f"Error: Database {db_path} not found. Please ensure it exists.")
    exit(1)

db = SQLDatabase.from_uri(f"sqlite:///{db_path}")

# 2. Create the SQL Agent
# This built-in toolkit automatically provides tools for listing tables, 
# getting schemas, executing queries, and checking queries.
print("Initializing SQL Agent...")
agent_executor = create_sql_agent(
    llm=model,
    db=db,
    verbose=True,
)

# 3. Test the agent
if __name__ == "__main__":
    question = "Which genre on average has the longest tracks?"
    print(f"\nQuestion: {question}\n")
    
    try:
        # We invoke the agent with the question.
        # If LangSmith tracing is enabled in .env, this will be traced automatically!
        result = agent_executor.invoke({"input": question})
        print(f"\nFinal Answer: {result.get('output', result)}")
    except Exception as e:
        print(f"\nError running agent: {e}")