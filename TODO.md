# CardIQ - TODO List

## ✅ Completed
- [x] Project structure setup
- [x] Configuration module
- [x] Data models (Pydantic)
- [x] Data loading (CardLoader)
- [x] Text chunking for RAG
- [x] Embeddings generation
- [x] FAISS vector store
- [x] RAG retriever interface
- [x] Claude API client
- [x] Agent prompts
- [x] Utility functions for calculations
- [x] Vector DB build script
- [x] README documentation

## 🚧 To Implement (Priority Order)

### High Priority - Core Functionality
1. **Agent Implementations**
   - [ ] `src/agents/base_agent.py` - Base agent class
   - [ ] `src/agents/spending_analyzer.py` - Agent 1
   - [ ] `src/agents/card_evaluator.py` - Agent 2  
   - [ ] `src/agents/recommendation_synthesizer.py` - Agent 3
   - [ ] `src/agents/orchestrator.py` - Main orchestrator

2. **Main Entry Point**
   - [ ] `main.py` - CLI interface for running system
   - [ ] Example usage with test profiles

3. **Test Profiles**
   - [ ] Create 5-10 test user profiles in `data/test_profiles/`
   - [ ] `scripts/generate_test_profiles.py` - Script to generate profiles

### Medium Priority - Testing & Evaluation
4. **Jupyter Notebooks**
   - [ ] `notebooks/01_data_exploration.ipynb` - Explore card data
   - [ ] `notebooks/02_test_rag_retrieval.ipynb` - Test RAG search
   - [ ] `notebooks/03_test_individual_agents.ipynb` - Test each agent
   - [ ] `notebooks/04_test_full_system.ipynb` - End-to-end test

5. **Evaluation Framework**
   - [ ] `evaluation/metrics.py` - Calculate accuracy metrics
   - [ ] `evaluation/llm_as_judge.py` - Quality evaluation

6. **Unit Tests**
   - [ ] `tests/test_data_loading.py`
   - [ ] `tests/test_rag_retrieval.py`
   - [ ] `tests/test_agents/` - Individual agent tests

### Low Priority - Nice to Have
7. **Streamlit UI** (Optional)
   - [ ] `app/streamlit_app.py` - Interactive web interface
   - [ ] Input form component
   - [ ] Recommendation display component

8. **Documentation**
   - [ ] `docs/architecture.md` - System architecture details
   - [ ] `docs/agent_design.md` - Agent responsibilities
   - [ ] `docs/evaluation_plan.md` - Evaluation methodology

9. **Additional Scripts**
   - [ ] `scripts/validate_data.py` - Data quality checks
   - [ ] `scripts/benchmark_models.py` - Compare Haiku vs Sonnet

## 🎯 Next Steps

**Week 1:**
1. Implement all 4 agents
2. Create main.py entry point
3. Test with 2-3 example queries
4. Create 5 test profiles

**Week 2:**
5. Build test notebooks
6. Run end-to-end testing
7. Debug and fix issues
8. Implement evaluation metrics

**Week 3:**
9. Run comprehensive evaluation
10. Compare multi-agent vs baseline
11. Optimize prompts if needed
12. Create presentation materials

**Week 4:**
13. Final testing and polishing
14. Prepare demo
15. Write final report
16. Practice presentation

## 📝 Notes

- Focus on core functionality first
- Agents are the most critical component
- Can skip Streamlit UI if time is tight
- Evaluation is important for final presentation
- Test with diverse spending profiles

## 🐛 Known Issues & Fixes

### Fixed Issues ✅
1. **Double-counting bug in travel spending** (FIXED)
   - Issue: When users entered travel=$300, flights=$150, hotels=$150, the system counted all three separately
   - Impact: Total spending was inflated by $300 and reward calculations were incorrect
   - Fix: Modified `calculate_category_rewards()` to subtract subcategories (flights, hotels, transit) from general travel
   - File: `src/utils/calculations.py:5-38`

2. **Missing config.py file** (FIXED)
   - Issue: `src/config.py` was missing, causing import errors
   - Fix: Created config file with proper environment variable loading
   - File: `src/config.py`

3. **Incomplete rewards type filtering** (FIXED)
   - Issue: Interactive prompt only showed 3 rewards types (cash_back, travel, flexible_points) but DB has 6
   - Impact: Users couldn't filter by business, dining_rewards, or hotel_points cards
   - Fix: Updated prompt to dynamically load all rewards types from database with validation
   - File: `interactive_main.py:71-88`

4. **Signup bonus bias in recommendations** (FIXED)
   - Issue: Cards ranked solely by Year 1 value, causing high signup bonus cards to always rank #1
   - Impact: Amex Platinum, Citi Strata Elite, Chase Sapphire Reserve recommended regardless of spending
   - Fix: Implemented blended ranking score: (Year_1 * 0.3) + (Year_2 * 0.4) + (Year_3 * 0.3)
   - File: `src/agents/card_evaluator.py:39-46, 121-136`
   - Result: Now balances signup bonuses with long-term value, better matches spending patterns

### Open Issues
- `calculate_spending_percentages()` still has double-counting issue but is not currently used anywhere
- Premium cards with high annual credits (e.g., Amex Platinum $2,484/year) may still rank highly even for low spenders
  - This could be addressed by adding a "credit utilization likelihood" factor in future
  - For now, the blended score significantly improves recommendations

## 💡 Ideas for Future Improvements

- Add more credit cards to database
- Support for business vs personal cards
- Credit score impact simulation
- Multi-card portfolio optimization
- Historical spending data upload
- Integration with actual bank APIs
