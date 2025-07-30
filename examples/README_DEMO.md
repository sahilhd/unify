# 🚀 UniLLM Multi-Provider Demo

This demo showcases how to use UniLLM with multiple LLM providers (Anthropic, OpenAI, and Google Gemini) to build a sophisticated content analysis system.

## 📋 What This Demo Does

The demo creates a **Smart Content Analysis System** that:

1. **🔍 Deep Analysis with Claude (Anthropic)**
   - Analyzes text sentiment, themes, and writing style
   - Provides comprehensive insights and observations
   - Identifies areas for improvement

2. **🎨 Creative Generation with GPT-4 (OpenAI)**
   - Creates improved versions of the original text
   - Generates creative variations with different tones
   - Suggests alternative titles and visual elements

3. **⚡ Fast Summarization with Gemini (Google)**
   - Provides concise executive summaries
   - Extracts key insights and actionable recommendations
   - Gives quality scores with justifications

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8 or higher
- An API key from the UniLLM SaaS platform
- Internet connection

### Step 1: Clone and Navigate
```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd singlemodel/examples

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Run Setup Script
```bash
python setup_demo_environment.py
```

This script will:
- ✅ Check Python version compatibility
- 📦 Install required packages
- 🌐 Test API connectivity
- 📋 Verify available models
- 📝 Create environment file template

### Step 3: Configure API Key
1. Get your API key from the UniLLM SaaS platform
2. Edit `multi_provider_demo.py`
3. Replace `"your_api_key_here"` with your actual API key
4. No base URL needed - uses the default SaaS platform

### Step 4: Run the Demo
```bash
python multi_provider_demo.py
```

## 📊 Expected Output

The demo will process 3 sample texts and produce:

```
🚀 Initializing Content Analysis System...
📊 Using models: {'anthropic': 'claude-3-sonnet', 'openai': 'gpt-4o', 'gemini': 'gemini-1.5-flash'}

==================== SAMPLE 1 ====================

📝 Starting complete analysis of text: 'The rapid advancement of artificial intelligence...'
============================================================

🔍 Step 1: Deep Analysis with Claude...
✅ Claude analysis completed!

🎨 Step 2: Creative Generation with GPT-4...
✅ GPT-4 generation completed!

⚡ Step 3: Fast Summarization with Gemini...
✅ Gemini summarization completed!

============================================================
🎉 Complete analysis finished!
📊 Total tokens used: 2847
⏱️  Timestamp: 2024-01-15T10:30:45.123456

============================================================
📋 ANALYSIS SUMMARY
============================================================
📝 Original Text: The rapid advancement of artificial intelligence has transformed...
🔧 Providers Used: anthropic, openai, gemini
📊 Total Tokens: 2847
⏱️  Timestamp: 2024-01-15T10:30:45.123456

📋 Final Summary (Gemini):
----------------------------------------
[Gemini's summary will appear here]

============================================================

✅ Analysis for sample 1 completed and saved!
💾 Results saved to: sample_1_analysis.json
```

## 📁 Generated Files

The demo creates several JSON files with detailed results:

- `sample_1_analysis.json` - Analysis of AI advancement text
- `sample_2_analysis.json` - Analysis of climate change text  
- `sample_3_analysis.json` - Analysis of remote work text

Each file contains:
- Original text
- Complete analysis from Claude
- Generated content from GPT-4
- Summary from Gemini
- Token usage statistics
- Timestamps

## 🔧 Customization

### Using Your Own Text
Edit the `sample_texts` list in `main()`:

```python
sample_texts = [
    "Your custom text here...",
    "Another text to analyze...",
    # Add more texts as needed
]
```

### Changing Models
Modify the `models` dictionary in `__init__()`:

```python
self.models = {
    "anthropic": "claude-3-haiku",  # Faster, cheaper
    "openai": "gpt-4o-mini",        # Faster, cheaper
    "gemini": "gemini-1.5-pro",     # More capable
}
```

### Adjusting Parameters
Modify temperature and max_tokens in each method:

```python
response = self.client.chat(
    model=self.models["anthropic"],
    messages=[ChatMessage(role="user", content=prompt)],
    temperature=0.5,  # Adjust creativity (0.0-2.0)
    max_tokens=800    # Adjust response length
)
```

## 🧪 Testing Individual Components

You can test each provider separately:

```python
analyzer = ContentAnalysisSystem()

# Test Claude only
claude_results = analyzer.analyze_text_with_claude("Your text here")

# Test GPT-4 only  
gpt4_results = analyzer.generate_content_with_gpt4("Analysis text", "Original text")

# Test Gemini only
gemini_results = analyzer.summarize_with_gemini("Analysis", "Generated content")
```

## 🔍 Troubleshooting

### API Key Issues
- Ensure your API key is correctly set in the script
- Check that you have sufficient credits in your UniLLM account
- Verify the API key is active and not expired

### Connection Issues
- Check your internet connection
- Verify the API base URL is correct
- Try the setup script to test connectivity

### Model Availability
- Some models might not be available in your region
- Check the models endpoint: `https://web-production-70deb.up.railway.app/models`
- Use alternative models if needed

### Rate Limiting
- The demo includes delays between requests
- If you hit rate limits, increase the delay in the main loop
- Consider running fewer samples at once

## 📈 Performance Notes

- **Claude**: Best for deep analysis and reasoning
- **GPT-4**: Best for creative content generation
- **Gemini**: Fastest for summarization and quick tasks

Typical token usage per sample:
- Claude analysis: ~800-1200 tokens
- GPT-4 generation: ~1000-1500 tokens  
- Gemini summary: ~300-500 tokens
- **Total per sample**: ~2100-3200 tokens

## 🎯 Learning Objectives

This demo teaches you:

1. **Multi-Provider Integration**: How to use different LLM providers in one system
2. **Provider Strengths**: When to use each provider for optimal results
3. **Error Handling**: How to handle provider-specific errors gracefully
4. **Result Management**: How to save, organize, and present results
5. **API Usage**: How to work with the UniLLM API effectively

## 🚀 Next Steps

After running this demo, try:

1. **Building Your Own Pipeline**: Create custom analysis workflows
2. **Adding More Providers**: Integrate Mistral, Cohere, or other providers
3. **Streaming Responses**: Use streaming for real-time processing
4. **Batch Processing**: Process multiple texts simultaneously
5. **Web Interface**: Create a web app using the analysis system

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the setup script to verify your environment
3. Check the UniLLM platform for API status
4. Review the generated JSON files for detailed error information

---

**Happy coding! 🎉** 