#!/usr/bin/env python3
"""
UniLLM SDK Cool Demo - Multi-Model AI Assistant
===============================================

This demo showcases the power of UniLLM SDK with:
- Multi-model conversations
- Creative content generation
- Code analysis and improvement
- Interactive chat with memory
- Model comparison
"""

import unillm
import time
import json
from typing import List, Dict

# Initialize UniLLM client
# Set your API key and base URL here
API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key
BASE_URL = "https://web-production-70deb.up.railway.app"  # Your deployed backend URL

client = unillm.UniLLM(
    api_key=API_KEY,
    base_url=BASE_URL
)

class MultiModelAssistant:
    def __init__(self):
        self.conversation_history = []
        self.models = {
            "gpt-3.5-turbo": "Fast, efficient, good for general tasks",
            "gpt-4": "Most capable, best for complex reasoning",
            "claude-3-opus-20240229": "Creative, great for writing and analysis"
        }
    
    def add_to_history(self, role: str, content: str, model: str = None):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "model": model,
            "timestamp": time.time()
        })
    
    def get_response(self, message: str, model: str = "gpt-3.5-turbo") -> str:
        """Get response from specified model"""
        try:
            # Prepare messages for the API
            messages = [{"role": "user", "content": message}]
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            response_text = response.choices[0].message.content
            self.add_to_history("user", message, model)
            self.add_to_history("assistant", response_text, model)
            
            return response_text
            
        except Exception as e:
            return f"Error with {model}: {str(e)}"
    
    def compare_models(self, prompt: str) -> Dict[str, str]:
        """Compare responses from different models"""
        print(f"\n🤖 Comparing models for: '{prompt}'")
        print("=" * 60)
        
        results = {}
        for model_name in self.models.keys():
            print(f"\n📝 {model_name} ({self.models[model_name]}):")
            print("-" * 40)
            
            response = self.get_response(prompt, model_name)
            results[model_name] = response
            print(response)
            time.sleep(1)  # Be nice to the API
        
        return results
    
    def creative_writing_session(self):
        """Interactive creative writing with model switching"""
        print("\n🎨 Creative Writing Session")
        print("=" * 40)
        print("Let's write a story together! I'll switch between models for different parts.")
        
        # Start with GPT-4 for the initial concept
        concept_prompt = "Create a unique story concept about a time traveler who discovers they can only travel to moments when someone is making a life-changing decision."
        print(f"\n📖 Generating story concept with GPT-4...")
        concept = self.get_response(concept_prompt, "gpt-4")
        print(concept)
        
        # Use Claude for character development
        character_prompt = f"Based on this concept: {concept[:200]}...\n\nCreate 3 detailed character profiles for this story."
        print(f"\n👥 Developing characters with Claude...")
        characters = self.get_response(character_prompt, "claude-3-opus-20240229")
        print(characters)
        
        # Use GPT-3.5 for a quick plot outline
        plot_prompt = f"Create a 5-point plot outline for this story concept: {concept[:150]}..."
        print(f"\n📋 Creating plot outline with GPT-3.5...")
        plot = self.get_response(plot_prompt, "gpt-3.5-turbo")
        print(plot)
        
        # Final scene with Claude
        scene_prompt = "Write the opening scene of this time travel story, focusing on the moment the protagonist first discovers their ability."
        print(f"\n🎬 Writing opening scene with Claude...")
        scene = self.get_response(scene_prompt, "claude-3-opus-20240229")
        print(scene)
    
    def code_analysis_and_improvement(self, code: str):
        """Analyze and improve code using different models"""
        print("\n💻 Code Analysis & Improvement")
        print("=" * 40)
        
        # Analyze with GPT-4
        analysis_prompt = f"Analyze this Python code and provide detailed feedback on style, efficiency, and potential improvements:\n\n{code}"
        print(f"\n🔍 Code analysis with GPT-4...")
        analysis = self.get_response(analysis_prompt, "gpt-4")
        print(analysis)
        
        # Generate improved version with Claude
        improve_prompt = f"Based on this analysis: {analysis[:300]}...\n\nRewrite the following code with improvements:\n\n{code}"
        print(f"\n⚡ Generating improved version with Claude...")
        improved = self.get_response(improve_prompt, "claude-3-opus-20240229")
        print(improved)
    
    def interactive_chat(self):
        """Interactive chat with model switching"""
        print("\n💬 Interactive Multi-Model Chat")
        print("=" * 40)
        print("Commands:")
        print("- Type a message to chat")
        print("- Type 'switch <model>' to change models")
        print("- Type 'history' to see conversation")
        print("- Type 'quit' to exit")
        
        current_model = "gpt-3.5-turbo"
        
        while True:
            user_input = input(f"\n[{current_model}] You: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'history':
                self.show_history()
            elif user_input.lower().startswith('switch '):
                new_model = user_input[7:].strip()
                if new_model in self.models:
                    current_model = new_model
                    print(f"Switched to {current_model}")
                else:
                    print(f"Available models: {', '.join(self.models.keys())}")
            else:
                print(f"\n🤖 {current_model}:")
                response = self.get_response(user_input, current_model)
                print(response)
    
    def show_history(self):
        """Display conversation history"""
        print("\n📚 Conversation History:")
        print("=" * 40)
        for i, msg in enumerate(self.conversation_history[-10:], 1):  # Show last 10 messages
            model_info = f" ({msg['model']})" if msg.get('model') else ""
            print(f"{i}. {msg['role'].title()}{model_info}: {msg['content'][:100]}...")
    
    def save_conversation(self, filename: str = "conversation.json"):
        """Save conversation to file"""
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        print(f"\n💾 Conversation saved to {filename}")

def main():
    print("🚀 UniLLM SDK Cool Demo - Multi-Model AI Assistant")
    print("=" * 60)
    
    assistant = MultiModelAssistant()
    
    # Demo 1: Model Comparison
    print("\n1️⃣ Model Comparison Demo")
    assistant.compare_models("Explain quantum computing in simple terms, then give me a creative analogy for it.")
    
    # Demo 2: Creative Writing
    print("\n2️⃣ Creative Writing Demo")
    assistant.creative_writing_session()
    
    # Demo 3: Code Analysis
    print("\n3️⃣ Code Analysis Demo")
    sample_code = '''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def get_fibonacci_sequence(length):
    return [fibonacci(i) for i in range(length)]
    '''
    assistant.code_analysis_and_improvement(sample_code)
    
    # Demo 4: Interactive Chat
    print("\n4️⃣ Interactive Chat Demo")
    assistant.interactive_chat()
    
    # Save conversation
    assistant.save_conversation()
    
    print("\n🎉 Demo completed! Check out the saved conversation file.")

if __name__ == "__main__":
    main() 