# ❓ Frequently Asked Questions (FAQ)

Common questions about Greens Digital Simulator.

---

## 📋 General Questions

### What is Greens Digital Simulator?

Greens Digital Simulator is an advanced framework for creating personalized neural network-based digital twins that simulate glucose dynamics in individuals with Type 1 Diabetes (T1D). It uses physiologically-constrained neural networks to predict how blood glucose levels respond to meals, insulin, exercise, and other factors.

---

### Who should use this tool?

**This tool is designed for**:
- 🔬 Researchers studying diabetes management and glucose dynamics
- 🎓 Students learning about diabetes modeling and machine learning
- 💡 Developers building diabetes management applications
- 📊 Data scientists analyzing CGM and diabetes data

**⚠️ Important**: This is a **research and educational tool only**. It is NOT approved for clinical use or medical decision-making.

---

### Is this FDA approved?

**No.** This software is for research and educational purposes only. It is not FDA approved, CE marked, or certified for clinical use. Always consult with healthcare providers for diabetes management decisions.

---

### Can I use this to manage my diabetes?

**No.** While the simulator can provide insights into glucose dynamics, it should **never** replace:
- Medical advice from healthcare providers
- Clinical CGM systems
- Professional diabetes management tools
- Insulin dosing recommendations from your care team

Use this tool to learn and explore, not for actual treatment decisions.

---

## 🔬 Technical Questions

### What data do I need to use the simulator?

**Minimum required data**:
- **CGM readings**: Continuous glucose monitor data (mg/dL)
- **Insulin data**: Insulin delivery rates (U/h)
- **Meal data**: Carbohydrate intake (grams)

**Optional but recommended**:
- Heart rate data (BPM)
- Sleep efficiency data (0-1 scale)
- Physical activity data

**Data format**: CSV file with 5-minute intervals. See `example/data_example/data_example.csv` for reference.

---

### How accurate are the predictions?

The pre-trained digital twins achieve:
- **RMSE**: < 20 mg/dL on test data
- **Time-in-range correlation**: R² > 0.85
- **Individual variability**: Captures both inter- and intra-individual differences

Accuracy depends on:
- Quality of input data
- How well the digital twin matches the individual
- Whether custom training was performed with personal data

---

### What is a "digital twin"?

A digital twin is a personalized computational model that mimics an individual's glucose-insulin dynamics. It's trained on that person's historical data to capture their unique metabolic responses to meals, insulin, exercise, and other factors.

**Think of it as**: A virtual version of a person's glucose regulation system that can be used to test "what if" scenarios.

---

### How many digital twins are available?

The framework includes **5 pre-trained digital twins** (IDs 0-4), each representing different glucose-insulin response patterns from real patient data:

- Twin 0: T1DEXI-01-0102
- Twin 1: T1DEXI-01-0692
- Twin 2: T1DEXI-01-0794
- Twin 3: T1DEXI-01-0880
- Twin 4: T1DEXI-01-1047

You can also train **custom digital twins** using your own data.

---

### What makes this different from other diabetes simulators?

**Unique features**:
1. **Neural network-based**: Uses deep learning instead of traditional differential equations
2. **Physiologically-constrained**: Architecture enforces known glucose-insulin dynamics
3. **Interpretable**: State-space structure allows understanding of predictions
4. **Adaptive**: Can be personalized with individual data
5. **Fast**: Real-time simulation on CPU
6. **Multi-factor**: Considers meals, insulin, sleep, heart rate, and more

---

## 💻 Usage Questions

### How do I run my first simulation?

**Quick start**:
```bash
# 1. Install
git clone https://github.com/Xplosion-Team/greensdigitalsimulator.git
cd greensdigitalsimulator
pip install -e .
pip install -r requirments.txt

# 2. Run example
cd example
python runDigitalTwin.py
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

---

### Can I use my own CGM data?

**Yes!** You need to format your data to match the required structure:

**Required columns**:
- `output_cgm`: CGM readings (mg/dL)
- `input_insulin`: Insulin delivery (U/h)
- `input_meal_carbs`: Carbs (g)
- `heart_rate`: Heart rate (BPM)
- `sleep_efficiency`: Sleep quality (0-1)
- Time features (hour of day, weekend flag)

See [EXAMPLES.md](EXAMPLES.md) - Example 5A for data formatting guide.

---

### How do I train a custom digital twin with my data?

**Basic steps**:
1. Prepare your data in the correct format
2. Split into training/test sets (80/20)
3. Use the training pipeline (requires full framework)
4. Evaluate on test data
5. Save model for future use

See [EXAMPLES.md](EXAMPLES.md) - Example 5 for details.

**Note**: Full training capabilities require the complete T1DSim_AI framework.

---

### Does the voice module work offline?

**No.** The voice recognition feature uses Google's Speech Recognition API, which requires an internet connection.

**Alternatives**:
- Use manual food entry (works offline)
- Use quick-add food buttons
- Type food descriptions instead of speaking

---

### Can I deploy this as a web app?

**Yes!** The framework includes a Flask-based web application that can be deployed to:
- Local server (development)
- Render (cloud platform)
- Heroku, AWS, Google Cloud, etc.

See `example/README_DEPLOYMENT.md` for deployment instructions.

---

## 🎯 Feature Questions

### What foods does the voice logger recognize?

**50+ common foods** including:

**Fruits**: apple, banana, orange, grapes, strawberry, etc.

**Grains**: bread, rice, pasta, cereal, oatmeal, etc.

**Proteins**: chicken, beef, fish, eggs, etc.

**Dairy**: milk, yogurt, cheese

**Fast food**: pizza, burger, fries, sandwich

**Snacks**: cookie, cake, chips, nuts

See `example/voice_module.py` for the complete food database.

---

### Can I add new foods to the database?

**Yes!** Edit the food database in `example/voice_module.py`:

```python
FOOD_DATABASE = {
    "my_custom_food": {
        "carbs_per_serving": 30,
        "protein_per_serving": 5,
        "fat_per_serving": 2,
        "fiber_per_serving": 3,
        "calories_per_serving": 150,
        "glycemic_index": "medium",
        "serving_size": "1 cup"
    }
}
```

---

### Can I export simulation results?

**Yes!** Results are Pandas DataFrames:

```python
from t1dsim_ai.individual_model import DigitalTwin

twin = DigitalTwin(n_digitalTwin=1)
results = twin.simulate(data)

# Export to CSV
results.to_csv('simulation_results.csv', index=False)

# Export to Excel
results.to_excel('simulation_results.xlsx', index=False)

# Export to JSON
results.to_json('simulation_results.json')
```

---

### What statistics can I calculate?

**Built-in metrics**:
- Mean glucose
- Standard deviation
- Coefficient of variation (CV%)
- Time in range (70-180 mg/dL)
- Time below/above range
- RMSE (vs actual CGM)

**Advanced metrics** (see [EXAMPLES.md](EXAMPLES.md)):
- MAGE (Mean Amplitude of Glycemic Excursions)
- J-Index
- LBGI/HBGI (Low/High Blood Glucose Index)
- Glycemic variability analysis

---

## 🛠️ Development Questions

### What programming language is this written in?

**Primary language**: Python 3.9+

**Key libraries**:
- PyTorch (neural networks)
- Pandas (data processing)
- Flask (web framework)
- Matplotlib/Plotly (visualization)
- NumPy (numerical computing)

---

### Can I contribute to the project?

**Absolutely!** We welcome contributions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Open a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Areas for contribution**:
- New features
- Bug fixes
- Documentation improvements
- Example scripts
- Testing

---

### What license is this under?

**MIT License** - Free and open source.

You can:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

You must:
- Include copyright notice
- Include license

See [LICENSE](LICENSE) file for details.

---

### How do I report a bug?

1. Check [existing issues](https://github.com/Xplosion-Team/greensdigitalsimulator/issues)
2. If not reported, open a new issue
3. Include:
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages
   - System information (OS, Python version)

---

## 🔐 Privacy & Security Questions

### Is my data shared with anyone?

**No.** The simulator:
- Runs entirely on your local machine
- Does not upload data to external servers
- Does not share data with third parties

**Exception**: Voice recognition uses Google's API, which processes audio to convert speech to text. No other data is sent.

---

### Where is my food log stored?

Food logs are stored **locally** in:
- `example/food_log.json` (local file)
- Not uploaded to any server
- You control the data

---

### Is this HIPAA compliant?

The software itself does not store or transmit PHI (Protected Health Information) by default. However:

**For research use**: Follow your institution's IRB requirements

**For deployment**: Implement appropriate security measures if handling real patient data

**Recommendation**: Anonymize any real patient data before use

---

## 📊 Research Questions

### Can I use this for my research?

**Yes!** This is designed for research. You can:
- Study glucose dynamics
- Test control algorithms
- Analyze population variability
- Validate new technologies
- Generate synthetic data

**Please cite** if you use in publications (see [README.md](README.md) for citation).

---

### Can I publish results from this simulator?

**Yes**, but with important caveats:

1. **Cite the framework**: Include proper attribution
2. **Describe limitations**: Clearly state this is a simulation
3. **Validate results**: Compare with clinical data when possible
4. **Ethical approval**: Get IRB approval if using real patient data
5. **Transparency**: Share methods and parameters

---

### What research has been done with this?

The underlying framework is based on:

*"Physiologically-constrained Neural Network Digital Twin Framework for Replicating Glucose Dynamics in Type 1 Diabetes"*

Authors: Valentina Roquemen-Echeverri, Taisa Kushner, Peter G. Jacobs, and Clara Mosquera-Lopez

---

## 🌐 Deployment Questions

### Can I use this on a mobile device?

**Web interface**: Yes, through mobile browser
- Responsive design
- Works on iOS/Android
- Touch-friendly controls

**Native app**: Not currently available
- Could be wrapped with React Native/Flutter
- Voice features may have limitations

---

### Does this work on Raspberry Pi?

**Yes**, but with considerations:

**Pros**:
- Python-based (compatible)
- CPU simulation (no GPU needed)

**Cons**:
- May be slower on older Pi models
- Limited RAM on Pi Zero
- PyTorch installation can be tricky

**Recommended**: Raspberry Pi 4 with 4GB+ RAM

---

### How much does it cost to run in the cloud?

**Render (recommended)**:
- Free tier: $0/month (with limitations)
- Starter: $7/month
- Standard: $25/month

**AWS/Google Cloud**: $10-50/month depending on usage

**Note**: Simulations are computationally light, free tier often sufficient for development/research.

---

## 🆘 Support Questions

### Where can I get help?

**Documentation**:
- [README.md](README.md) - Overview
- [QUICKSTART.md](QUICKSTART.md) - Getting started
- [API.md](API.md) - API reference
- [EXAMPLES.md](EXAMPLES.md) - Tutorials
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

**Community**:
- [GitHub Issues](https://github.com/Xplosion-Team/greensdigitalsimulator/issues) - Bug reports
- [GitHub Discussions](https://github.com/Xplosion-Team/greensdigitalsimulator/discussions) - Questions

---

### What if my question isn't answered here?

1. **Search documentation**: Use Ctrl+F to search all docs
2. **Check issues**: Someone may have asked already
3. **Ask in discussions**: Community can help
4. **Open an issue**: We'll add common questions to this FAQ

---

## 📚 Learning Resources

### I'm new to Python. Can I still use this?

**Yes**, but you'll need:
- Basic Python knowledge
- Understanding of data structures (lists, dictionaries)
- Familiarity with Pandas (for data handling)

**Learning resources**:
- [Python.org Tutorial](https://docs.python.org/3/tutorial/)
- [Pandas Documentation](https://pandas.pydata.org/docs/getting_started/index.html)
- [PyTorch Tutorials](https://pytorch.org/tutorials/)

**Tip**: Start with the web interface (no coding required!)

---

### I'm new to diabetes. Where can I learn more?

**Resources**:
- [ADA - What is Diabetes?](https://www.diabetes.org/diabetes)
- [JDRF - Type 1 Diabetes Resources](https://www.jdrf.org/)
- [NIH - Diabetes Information](https://www.niddk.nih.gov/health-information/diabetes)

**Key concepts to understand**:
- CGM (Continuous Glucose Monitoring)
- Insulin delivery (basal/bolus)
- Carbohydrate counting
- Time in range (TIR)

---

### Where can I learn about neural network models?

**Beginner**:
- [3Blue1Brown - Neural Networks](https://www.youtube.com/watch?v=aircAruvnKk)
- [Fast.ai Course](https://course.fast.ai/)

**Advanced**:
- [Deep Learning Book](http://www.deeplearningbook.org/)
- [PyTorch Documentation](https://pytorch.org/docs/)

**This framework specifically**:
- See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

---

## 💡 Best Practices

### What's the recommended workflow?

1. **Exploration**: Use pre-trained twins with example data
2. **Experimentation**: Try custom scenarios
3. **Analysis**: Calculate metrics and visualize results
4. **Customization**: Train with your own data (optional)
5. **Deployment**: Share via web interface (optional)

---

### How often should I retrain my digital twin?

**Depends on**:
- Data availability (need sufficient new data)
- Changes in physiology (growth, weight change)
- Treatment changes (new pump, different insulin)
- Model accuracy (if predictions degrade)

**Recommendation**: Every 3-6 months with new data, or when accuracy drops.

---

### What are common mistakes to avoid?

❌ **Don't**:
- Use for actual medical decisions
- Ignore data quality issues
- Extrapolate beyond training range
- Share real patient data without consent
- Deploy without security measures

✅ **Do**:
- Validate predictions against real data
- Document your methodology
- Use appropriate train/test splits
- Keep software updated
- Follow ethical guidelines

---

<div align="center">

**Have more questions?** 

[Open a Discussion](https://github.com/Xplosion-Team/greensdigitalsimulator/discussions) • [Report an Issue](https://github.com/Xplosion-Team/greensdigitalsimulator/issues)

[Back to README](README.md)

</div>
