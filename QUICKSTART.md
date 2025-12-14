# CardIQ - Quick Start Guide

## 📦 What's Included

This zip contains the **CardIQ Multi-Agent Credit Card Recommendation System** with:

✅ Complete project structure
✅ RAG pipeline (embeddings, FAISS vector store)
✅ Data models and utilities
✅ Claude API client wrapper
✅ Agent prompts and configuration
✅ 25 credit cards database
✅ Vector DB build script
✅ Comprehensive documentation

## ⚠️ What's NOT Included (You Need to Implement)

The following core components need to be built:

🚧 **Agent Implementations** (src/agents/)
- base_agent.py
- spending_analyzer.py
- card_evaluator.py
- recommendation_synthesizer.py
- orchestrator.py

🚧 **Main Entry Point**
- main.py

🚧 **Test Notebooks** (notebooks/)

See TODO.md for complete list.

## 🚀 Setup Instructions

### 1. Extract and Navigate
```bash
unzip cardiq.zip
cd cardiq
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- anthropic (Claude API)
- langchain & langchain-anthropic
- faiss-cpu (vector database)
- sentence-transformers (embeddings)
- pydantic (data validation)
- And more...

### 4. Configure API Key
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Anthropic API key
nano .env  # or use any text editor

# Add this line:
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### 5. Build Vector Database
```bash
python scripts/build_vector_db.py
```

This will:
- Load 25 credit cards from data/raw/
- Create text chunks for each card
- Generate embeddings using sentence-transformers
- Build FAISS index
- Save to data/vector_db/

Expected output:
```
Building CardIQ Vector Database
[1/4] Loading credit cards...
✅ Loaded 25 cards
[2/4] Creating text chunks...
✅ Created 25 text chunks
[3/4] Generating embeddings...
✅ Generated embeddings with shape (25, 384)
[4/4] Building FAISS index...
✅ Vector database successfully saved
```

## 🧪 Test the Setup

### Test 1: RAG Retrieval
```python
from src.rag.retriever import CardRetriever

# Initialize retriever
retriever = CardRetriever()

# Test search
results = retriever.search("cards with airport lounge access", k=3)
for card in results:
    print(f"- {card['card_name']}")
```

### Test 2: Load Card Data
```python
from src.data.card_loader import CardLoader

loader = CardLoader()
cards = loader.load_cards()
print(f"Loaded {len(cards)} cards")
print(f"First card: {cards[0]['card_name']}")
```

### Test 3: Claude API
```python
from src.api.claude_client import ClaudeClient

client = ClaudeClient()
response = client.call_haiku(
    system_prompt="You are a helpful assistant.",
    user_message="Say hello!"
)
print(response)
```

## 📝 Next Steps

### Week 1: Implement Agents

1. **Create Base Agent Class** (src/agents/base_agent.py)
```python
class BaseAgent:
    def __init__(self, claude_client):
        self.claude_client = claude_client
    
    def process(self, input_data):
        raise NotImplementedError
```

2. **Implement Spending Analyzer** (src/agents/spending_analyzer.py)
- Use Haiku model
- Takes user spending, returns analysis JSON
- Use prompts from src/prompts/agent_prompts.py

3. **Implement Card Evaluator** (src/agents/card_evaluator.py)
- Use Haiku model
- Takes spending analysis + cards, returns evaluations
- Use calculation utils from src/utils/calculations.py

4. **Implement Recommendation Synthesizer** (src/agents/recommendation_synthesizer.py)
- Use Sonnet model (better quality)
- Takes evaluations + cards, returns rich recommendations
- Uses RAG retriever for card features

5. **Implement Orchestrator** (src/agents/orchestrator.py)
- Coordinates all agents
- Manages workflow
- Returns final formatted output

### Week 2: Testing

Create test notebooks in notebooks/:
- Test individual agents
- Test full workflow
- Create test user profiles

### Week 3: Evaluation

Implement evaluation framework:
- Accuracy metrics
- LLM-as-judge
- Compare multi-agent vs baseline

### Week 4: Polish & Present

- Final testing
- Demo preparation
- Presentation slides

## 📚 Key Files to Reference

**Configuration:**
- `.env` - API keys and settings
- `src/config/settings.py` - All configuration constants

**Data:**
- `data/raw/credit_cards_llm_special_features_filled.json` - 25 cards
- `src/models/` - Pydantic models for type safety

**Prompts:**
- `src/prompts/agent_prompts.py` - System prompts for each agent

**Utilities:**
- `src/utils/calculations.py` - Reward calculation functions
- `src/api/claude_client.py` - Claude API wrapper

**Documentation:**
- `README.md` - Full project overview
- `TODO.md` - Complete task list
- This file - Quick start guide

## 💰 Cost Management

With $50 Anthropic credits:
- Embeddings: ~$0.001 (negligible)
- Per recommendation: ~$0.04 (hybrid Haiku/Sonnet)
- Total budget: ~1,250 recommendations possible
- Expected usage: ~$25-30 for full project

## 🆘 Troubleshooting

**Issue: Module not found errors**
```bash
# Make sure you're in the cardiq directory
cd cardiq

# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

**Issue: API key not working**
```bash
# Check .env file exists
ls -la .env

# Verify API key is set correctly (no quotes needed)
cat .env | grep ANTHROPIC_API_KEY
```

**Issue: Vector database not found**
```bash
# Rebuild vector database
python scripts/build_vector_db.py

# Check it was created
ls data/vector_db/
```

## 📞 Support

Check these resources:
1. README.md - Full documentation
2. TODO.md - What needs to be implemented
3. Code comments - Inline documentation
4. Anthropic docs - https://docs.anthropic.com

## 🎓 Academic Notes

This is a course project demonstrating:
- Multi-agent system architecture
- Retrieval-Augmented Generation (RAG)
- Hybrid model selection
- Cost optimization strategies

Focus on:
✅ Agent coordination and workflow
✅ RAG integration and effectiveness
✅ Evaluation methodology
✅ Clear demonstration of LLM techniques

Good luck with your implementation! 🚀
