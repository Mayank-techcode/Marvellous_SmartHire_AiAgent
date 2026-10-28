# Marvellous_SmartHire – AI Mock Interview Agent

A **text-based AI Mock Interview Agent** that conducts technical interviews in the terminal, evaluates answers with a **locally running Llama3 model (via Ollama)**, remembers the interview, and generates a detailed report.

**Python 3.8+ · Llama3 · Ollama · MIT License**

Everything runs **locally**: no API keys, no cloud costs, and your answers never leave your machine.

---

## Overview

The agent asks a question, accepts your answer, builds a structured prompt, sends it to Llama3, extracts a score from the reply, stores the answer, score and feedback in memory, and finally writes a full report to the `reports/` folder.

## Features

- **Two modes:** full interview or topic-wise interview
- **Structured LLM feedback** for every answer: Score, Evaluation, Missing Points, Improved Answer, Interview Suggestion
- **Automatic score extraction** (`Score: 7/10` → `7`)
- **Interview memory** via `self.history`
- **Final report:** total score, average score, performance band, question-wise analysis
- **Timestamped reports** saved as `.txt` files
- **Continue-or-stop prompt** after each question
- **Easily extendable** question bank

## Learning Outcomes

Generative AI · AI Agents · LLM integration · Prompt engineering · Interview automation · Answer evaluation · Report generation · Memory using interview history

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Main language |
| Ollama | Runs the LLM locally |
| Llama3 | Evaluates student answers |
| `requests` | Sends HTTP requests to the Ollama API |
| `os` | Creates the `reports/` folder |
| `datetime` | Timestamps for report filenames |

Only `requests` is a third-party package (`pip install requests`); `os` and `datetime` ship with Python.

## Project Structure

```
Marvellous_SmartHire_AI_Agent/
├── main.py               # Entry point: menu, interview loop, saves report
├── interview_agent.py    # MockInterviewAgent: prompt, evaluation, scoring, memory, report
├── llm_engine.py         # ask_llm(): bridge to Ollama / Llama3
├── questions.py          # Question bank
├── report_generator.py   # save_report(): writes the .txt report
├── NOTES.md
└── LICENSE
```

## Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/download)
- The `llama3` model (about 4.7 GB download; a machine with 8 GB+ RAM is recommended)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Marvellous_SmartHire_AI_Agent.git
cd Marvellous_SmartHire_AI_Agent

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install the only Python dependency
pip install requests

# 4. Download the model
ollama pull llama3

# 5. Make sure Ollama is running (listens on http://localhost:11434)
ollama serve
```

> If Ollama is already running as a background app/service, step 5 is not needed.

### Run

```bash
python main.py
```

## Usage

```
======================================================================
              AI Mock Interview Agent
              Text Based Version
======================================================================

Enter student name: Mayank

Select Interview Mode:
1. Start Full Interview
2. Start Topic-wise Interview
3. Exit
```

1. Enter your name (blank defaults to `Student`).
2. Choose **1** for all questions, **2** to pick a single topic, or **3** to exit.
3. Type your answer. An empty answer is recorded as *"Student did not provide any answer."*
4. Read the AI evaluation, then type `yes` to continue (anything else ends the interview).
5. The final report is printed and saved to:

```
reports/Marvellous_AI_Agent_<Name>_Interview_Report_<DD_MM_YYYY_HH_MM_SS>.txt
```

### What the LLM returns for each answer

```
Score: <number out of 10>
Evaluation:         correct / partially correct / incorrect
Missing Points:     important technical points left out
Improved Answer:    a better, student-friendly answer
Interview Suggestion: one practical tip
```

### Performance bands (based on average score)

| Average | Result |
|---------|--------|
| 8 and above | Excellent performance |
| 6 to < 8 | Good performance |
| 4 to < 6 | Average performance |
| below 4 | Needs improvement |

## Question Bank

Currently one question for each of: **Python, OOP, Machine Learning, Deep Learning, Transformer, LLM, RAG, AI Agent**.

To add questions, append dictionaries to the `questions` list in `questions.py`:

```python
{
    "topic": "Python",
    "question": "Explain the difference between list, tuple and set in Python."
}
```

New topics appear automatically in the topic-wise menu.

## Module Reference

| File | Key items | Responsibility |
|------|-----------|----------------|
| `main.py` | `print_header()`, `show_menu()`, `get_available_topics()`, `start_interview(agent, selected_questions)`, `main()` | CLI, menu and interview loop |
| `interview_agent.py` | `MockInterviewAgent`, `evaluate_answer()`, `extract_score()`, `generate_final_report()` | Prompt building, scoring, memory, report text |
| `llm_engine.py` | `ask_llm(prompt)` | POST to Ollama, returns the response text |
| `questions.py` | `questions` | Topic-wise question bank |
| `report_generator.py` | `save_report(student_name, report)` | Creates `reports/`, builds filename, writes file |

**Agent state:** `self.student_name`, `self.history` (list of dicts with topic, question, answer, evaluation, score), `self.total_score`

## How It Works

```text
Student starts project (python main.py)
        |
        v
Header is displayed  ->  Student enters name
        |
        v
Student selects interview mode
        |
        v
Questions are loaded from questions.py
        |
        v
+--> Student answers question
|           |
|           v
|    MockInterviewAgent creates prompt
|           |
|           v
|    llm_engine.py sends request to Ollama (Llama3)
|           |
|           v
|    Llama3 evaluates answer  ->  evaluation returned to agent
|           |
|           v
|    Score is extracted
|           |
|           v
|    Answer, score and feedback stored in history
|           |
|           v
+--- "Do you want to continue?"  (yes = next question)
            |  no / all questions done
            v
Final report is generated

```

**LLM call:**

```python
POST http://localhost:11434/api/generate
{"model": "llama3", "prompt": prompt, "stream": False}
```

`Python Application → Ollama API → Llama3 Model`

## AI Agent Concepts

| AI Agent Component | Implementation |
|--------------------|----------------|
| User Input | Student answer |
| Goal | Evaluate the interview answer |
| LLM Brain | Llama3 |
| Tool / API | Ollama API |
| Memory | `self.history` |
| Decision | Score and feedback |
| Output | Evaluation and final report |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "LLM CONNECTION ERROR" shown as the evaluation | Ollama isn't reachable. Start it (`ollama serve`), confirm `ollama list` shows `llama3`, and check port `11434` |
| Score is always `0` | The reply didn't contain a plain `Score: X/10` line. See *Known Limitations* in `NOTES.md` |
| Marathi header text shows as `?` on Windows | Run `chcp 65001` first or set `PYTHONUTF8=1` |
| First answer is very slow | The model loads into memory on first use; later answers are faster |

## Known Limitations

- If Ollama is down, the error message is treated as the evaluation and scored `0`, so don't continue an interview in that state.
- LLM scores can vary run to run.
- Score parsing is simple: replies like `**Score: 8/10**` or `Score: 7.5/10` can be mis-scored. Details and suggested fixes are in [NOTES.md](NOTES.md).

## Future Enhancements

Voice interviews · Web UI (Streamlit/Flask) · PDF reports · Difficulty levels · JSON/CSV question bank · Configurable model name and URL · Unit tests

## Author

**Mayank Salunkhe**, built at **Marvellous Infosystems** (Python – Automation & Machine Learning).

## License

MIT. See [LICENSE](LICENSE).
