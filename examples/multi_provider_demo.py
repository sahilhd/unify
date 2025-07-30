#!/usr/bin/env python3
"""
Multi-Provider Demo: Building a Smart Content Analysis System

This example demonstrates how to use UniLLM with multiple providers:
- Anthropic (Claude) for complex reasoning and analysis
- OpenAI (GPT-4) for creative content generation
- Google Gemini for fast processing and summarization

The demo builds a content analysis system that:
1. Analyzes a text using Claude for deep insights
2. Generates creative content using GPT-4
3. Summarizes results using Gemini
"""

import os
import sys
import json
from typing import List, Dict, Any
from datetime import datetime

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unillm import UniLLM
from unillm.models import ChatRequest, ChatMessage

class ContentAnalysisSystem:
    """A smart content analysis system using multiple LLM providers."""
    
    def __init__(self):
        """
        Initialize the content analysis system.
        Uses the default SaaS UniLLM platform.
        """
        self.client = UniLLM(
            api_key="your_api_key_here"  # Replace with your actual API key
        )
        
        # Define provider-specific models
        self.models = {
            "anthropic": "claude-3-sonnet",  # For deep analysis
            "openai": "gpt-4o",             # For creative generation
            "gemini": "gemini-1.5-flash"    # For fast processing
        }
        
        print("🚀 Content Analysis System initialized!")
        print(f"📊 Using models: {self.models}")
    
    def analyze_text_with_claude(self, text: str) -> Dict[str, Any]:
        """
        Use Claude (Anthropic) for deep text analysis.
        
        Args:
            text: The text to analyze
            
        Returns:
            Analysis results including sentiment, themes, and insights
        """
        print("\n🔍 Step 1: Deep Analysis with Claude...")
        
        prompt = f"""
        Please provide a comprehensive analysis of the following text:
        
        "{text}"
        
        Please analyze:
        1. Overall sentiment and tone
        2. Key themes and topics
        3. Writing style and complexity
        4. Potential audience
        5. Key insights and observations
        6. Areas for improvement (if applicable)
        
        Provide your analysis in a structured, detailed manner.
        """
        
        try:
            response = self.client.chat(
                model=self.models["anthropic"],
                messages=[ChatMessage(role="user", content=prompt)],
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=1000
            )
            
            print("✅ Claude analysis completed!")
            return {
                "provider": "anthropic",
                "model": self.models["anthropic"],
                "analysis": response.content,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error in Claude analysis: {e}")
            return {"error": str(e)}
    
    def generate_content_with_gpt4(self, analysis: str, original_text: str) -> Dict[str, Any]:
        """
        Use GPT-4 (OpenAI) for creative content generation based on analysis.
        
        Args:
            analysis: The analysis results from Claude
            original_text: The original text that was analyzed
            
        Returns:
            Generated content including improvements and variations
        """
        print("\n🎨 Step 2: Creative Generation with GPT-4...")
        
        prompt = f"""
        Based on the following analysis of a text, please generate creative content:
        
        Original Text:
        "{original_text}"
        
        Analysis:
        {analysis}
        
        Please generate:
        1. An improved version of the original text
        2. A creative variation with a different tone/style
        3. A summary that captures the essence in 2-3 sentences
        4. 3 alternative titles for the content
        5. Suggestions for visual elements that could accompany this content
        
        Be creative and provide diverse, high-quality outputs.
        """
        
        try:
            response = self.client.chat(
                model=self.models["openai"],
                messages=[ChatMessage(role="user", content=prompt)],
                temperature=0.8,  # Higher temperature for creativity
                max_tokens=1200
            )
            
            print("✅ GPT-4 generation completed!")
            return {
                "provider": "openai",
                "model": self.models["openai"],
                "generated_content": response.content,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error in GPT-4 generation: {e}")
            return {"error": str(e)}
    
    def summarize_with_gemini(self, analysis: str, generated_content: str) -> Dict[str, Any]:
        """
        Use Gemini for fast summarization and key point extraction.
        
        Args:
            analysis: The analysis from Claude
            generated_content: The generated content from GPT-4
            
        Returns:
            Concise summary and key insights
        """
        print("\n⚡ Step 3: Fast Summarization with Gemini...")
        
        prompt = f"""
        Please provide a concise summary and extract key insights from the following:
        
        Analysis:
        {analysis}
        
        Generated Content:
        {generated_content}
        
        Please provide:
        1. A 3-sentence executive summary
        2. Top 5 key insights
        3. Actionable recommendations
        4. Overall quality score (1-10) with brief justification
        
        Keep it concise and actionable.
        """
        
        try:
            response = self.client.chat(
                model=self.models["gemini"],
                messages=[ChatMessage(role="user", content=prompt)],
                temperature=0.2,  # Low temperature for consistent summarization
                max_tokens=500
            )
            
            print("✅ Gemini summarization completed!")
            return {
                "provider": "gemini",
                "model": self.models["gemini"],
                "summary": response.content,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error in Gemini summarization: {e}")
            return {"error": str(e)}
    
    def run_complete_analysis(self, text: str) -> Dict[str, Any]:
        """
        Run the complete content analysis pipeline using all three providers.
        
        Args:
            text: The text to analyze
            
        Returns:
            Complete analysis results from all providers
        """
        print(f"\n📝 Starting complete analysis of text: '{text[:50]}...'")
        print("=" * 60)
        
        # Step 1: Deep analysis with Claude
        claude_results = self.analyze_text_with_claude(text)
        
        # Step 2: Creative generation with GPT-4
        gpt4_results = self.generate_content_with_gpt4(
            claude_results.get("analysis", ""), 
            text
        )
        
        # Step 3: Summarization with Gemini
        gemini_results = self.summarize_with_gemini(
            claude_results.get("analysis", ""),
            gpt4_results.get("generated_content", "")
        )
        
        # Compile final results
        final_results = {
            "original_text": text,
            "timestamp": datetime.now().isoformat(),
            "providers_used": list(self.models.keys()),
            "results": {
                "claude_analysis": claude_results,
                "gpt4_generation": gpt4_results,
                "gemini_summary": gemini_results
            },
            "total_tokens": (
                claude_results.get("tokens_used", 0) +
                gpt4_results.get("tokens_used", 0) +
                gemini_results.get("tokens_used", 0)
            )
        }
        
        print("\n" + "=" * 60)
        print("🎉 Complete analysis finished!")
        print(f"📊 Total tokens used: {final_results['total_tokens']}")
        print(f"⏱️  Timestamp: {final_results['timestamp']}")
        
        return final_results
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Save analysis results to a JSON file.
        
        Args:
            results: The analysis results
            filename: Optional filename, defaults to timestamp-based name
            
        Returns:
            The filename where results were saved
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {filename}")
        return filename
    
    def print_summary(self, results: Dict[str, Any]):
        """
        Print a formatted summary of the analysis results.
        
        Args:
            results: The analysis results
        """
        print("\n" + "=" * 60)
        print("📋 ANALYSIS SUMMARY")
        print("=" * 60)
        
        print(f"📝 Original Text: {results['original_text'][:100]}...")
        print(f"🔧 Providers Used: {', '.join(results['providers_used'])}")
        print(f"📊 Total Tokens: {results['total_tokens']}")
        print(f"⏱️  Timestamp: {results['timestamp']}")
        
        # Print Gemini summary if available
        gemini_summary = results['results']['gemini_summary']
        if 'summary' in gemini_summary:
            print(f"\n📋 Final Summary (Gemini):")
            print("-" * 40)
            print(gemini_summary['summary'])
        
        print("\n" + "=" * 60)


def main():
    """Main function to demonstrate the content analysis system."""
    
    # Sample texts for analysis
    sample_texts = [
        "The rapid advancement of artificial intelligence has transformed how we approach problem-solving in modern society. From healthcare diagnostics to autonomous vehicles, AI systems are becoming increasingly sophisticated and integrated into our daily lives. However, this technological revolution also raises important questions about ethics, privacy, and the future of human work.",
        
        "Climate change represents one of the most pressing challenges of our time. Rising global temperatures, extreme weather events, and shifting precipitation patterns are affecting ecosystems and human communities worldwide. Addressing this crisis requires coordinated international action, innovative technologies, and fundamental changes to how we produce and consume energy.",
        
        "The rise of remote work has fundamentally changed the modern workplace. Companies are discovering that productivity can remain high while employees enjoy greater flexibility and work-life balance. This shift has implications for urban planning, real estate markets, and the future of office culture."
    ]
    
    # Initialize the system
    print("🚀 Initializing Content Analysis System...")
    analyzer = ContentAnalysisSystem()
    
    # Run analysis on each sample text
    for i, text in enumerate(sample_texts, 1):
        print(f"\n{'='*20} SAMPLE {i} {'='*20}")
        
        # Run complete analysis
        results = analyzer.run_complete_analysis(text)
        
        # Print summary
        analyzer.print_summary(results)
        
        # Save results
        filename = analyzer.save_results(results, f"sample_{i}_analysis.json")
        
        print(f"\n✅ Analysis for sample {i} completed and saved!")
        
        # Add a small delay between analyses
        if i < len(sample_texts):
            print("\n⏳ Waiting 2 seconds before next analysis...")
            import time
            time.sleep(2)
    
    print("\n🎉 All analyses completed successfully!")
    print("📁 Check the generated JSON files for detailed results.")


if __name__ == "__main__":
    # Check if API key is set
    if "your_api_key_here" in open(__file__).read():
        print("⚠️  Please update the API key in the script before running!")
        print("   Replace 'your_api_key_here' with your actual UniLLM API key.")
        sys.exit(1)
    
    main() 