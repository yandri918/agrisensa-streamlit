# Test ChatbotService locally
import os
import sys

# Set API key
os.environ['GEMINI_API_KEY'] = "AIzaSyBC-BBiqdpYNVZ97U_jp-NLAOw87kKLcg8"

# Add parent directory to path
sys.path.insert(0, os.path.abspath('..'))

print("=" * 50)
print("Testing AgriBot ChatbotService")
print("=" * 50)

try:
    from app.services.chatbot_service import ChatbotService
    print("✅ ChatbotService imported successfully")
    
    # Initialize chatbot
    print("\n🔄 Initializing chatbot...")
    bot = ChatbotService()
    
    if bot.chat is None:
        print(f"❌ Chatbot initialization failed: {bot.init_error}")
        sys.exit(1)
    
    print("✅ Chatbot initialized successfully")
    
    # Test chat
    print("\n💬 Testing chat...")
    test_message = "Halo AgriBot, apa kabar?"
    print(f"User: {test_message}")
    
    response = bot.get_response(test_message)
    print(f"AgriBot: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")
    print("=" * 50)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
