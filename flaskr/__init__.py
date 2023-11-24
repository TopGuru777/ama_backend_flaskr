import os
import requests
from langchain.chains import GraphSparqlQAChain
from langchain.chat_models import ChatOpenAI
from langchain.graphs import RdfGraph

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Metered Domain
# METERED_DOMAIN = os.environ.get("METERED_DOMAIN")
graph = RdfGraph(
    source_file="http://localhost:3030/ama/data",
    standard="rdf",
    local_copy="test.ttl",
)
graph.load_schema()
graph.get_schema

#model_kwargs={"open_ai_key": "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"}

chain = GraphSparqlQAChain.from_llm(
    ChatOpenAI(model_name="gpt-4", temperature=0, openai_api_key="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"), graph=graph, verbose=True
)


# API Route to create a meeting room
@app.route("/test", methods=['POST'])
def test():
    return {
        "message" : "success"
    }

@app.route("/sparql", methods=['POST'])
def sparql():
    print(request.form)
    message = request.form['message']
    try:
        return {
            "data": chain.run(message)
        }
    except Exception as e:
        print("An error occured", str(e))
        return {
            "error": "Failed"
        }


@app.route("/")
def index():
    return "Backend"
