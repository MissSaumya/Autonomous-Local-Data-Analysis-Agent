from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import markdown
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_ollama import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent

app = Flask(__name__)
UPLOAD_FOLDER = 'data'
PLOT_FOLDER = 'static/plots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOT_FOLDER, exist_ok=True)

class QwenAgent:
    def __init__(self):
        # Temp 0 is critical to stop "creative" formatting errors
        self.llm = ChatOllama(model="qwen3:4b", temperature=0)
        self.df = None
        self.executor = None

    def init_executor(self):
        # We tell the model exactly how to format to avoid Parser Errors
        prefix = "You are a robotic data tool. Use Thought, Action, Action Input, and Observation format."
        self.executor = create_pandas_dataframe_agent(
            self.llm, self.df, verbose=True, allow_dangerous_code=True, 
            handle_parsing_errors=True, prefix=prefix
        )

agent = QwenAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    agent.df = pd.read_csv(path)
    # Python-side cleaning is instant
    agent.df.drop_duplicates(inplace=True)
    agent.init_executor()
    return jsonify({"msg": "Success"})

@app.route('/identify', methods=['POST'])
def identify():
    # Identify famous datasets like Titanic
    prompt = f"Analyze these columns: {agent.df.columns.tolist()}. Is this Titanic or a famous set? Explain."
    res = agent.llm.invoke(prompt).content
    return jsonify({"info": markdown.markdown(res)})

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Create plot using Standard Python (prevents LLM timeout)
        plt.figure(figsize=(8, 5))
        agent.df.iloc[:, :5].select_dtypes(include='number').boxplot()
        plt.title("Automated Data Distribution")
        plot_path = os.path.join(PLOT_FOLDER, 'plot.png')
        plt.savefig(plot_path)
        plt.close()

        # Attempt LLM EDA
        res = agent.executor.invoke("Summarize the dataset quality and trends in 3 bullet points.")
        return jsonify({"eda": markdown.markdown(res['output']), "plot": "/static/plots/plot.png"})
    except Exception:
        # FAIL-SAFE: If the LLM crashes, Python calculates it manually
        summary = f"**Manual Summary (LLM Timeout):** {len(agent.df)} rows, {len(agent.df.columns)} columns."
        return jsonify({"eda": markdown.markdown(summary), "plot": "/static/plots/plot.png"})

@app.route('/ask', methods=['POST'])
def ask():
    query = request.json.get("query")
    try:
        res = agent.executor.invoke(query)
        return jsonify({"answer": markdown.markdown(res['output'])})
    except:
        return jsonify({"answer": "I encountered a formatting error. Please try rephrasing."})

if __name__ == '__main__':
    app.run(debug=True)