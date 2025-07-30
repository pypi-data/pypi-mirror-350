"""
Test script to demonstrate improved streaming with proper finish_reason handling.
"""

from thinagents import Agent


def test_streaming_finish_reason():
    """Test that streaming properly handles and emits finish_reason."""
    
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    # Create agent with tools
    agent = Agent(
        name="Test Agent",
        model="gpt-3.5-turbo",  # Use a common model for testing
        tools=[add],
        max_steps=5,
    )
    
    print("Testing streaming with finish_reason tracking...")
    print("=" * 50)
    
    # Test 1: Simple text response (should end with finish_reason="stop")
    print("\n1. Testing simple text response:")
    print("-" * 30)
    
    finish_reasons_seen = []
    content_chunks = []
    
    for chunk in agent.run("Hello, how are you?", stream=True):
        content_chunks.append(chunk.content)
        if chunk.finish_reason is not None:
            finish_reasons_seen.append(chunk.finish_reason)
            print(f"[FINISH_REASON: {chunk.finish_reason}] Content: '{chunk.content}' (Type: {chunk.content_type})")
        else:
            print(f"[STREAMING] Content: '{chunk.content}' (Type: {chunk.content_type})")
    
    print(f"\nSummary:")
    print(f"- Total chunks: {len(content_chunks)}")
    print(f"- Finish reasons seen: {finish_reasons_seen}")
    print(f"- Final content: {''.join(content_chunks)}")
    
    # Test 2: Tool usage (should show tool_calls finish_reason, then stop)
    print("\n\n2. Testing tool usage:")
    print("-" * 30)
    
    finish_reasons_seen = []
    content_chunks = []
    
    for chunk in agent.run("What is 5 + 3?", stream=True, stream_intermediate_steps=True):
        content_chunks.append(chunk.content)
        if chunk.finish_reason is not None:
            finish_reasons_seen.append(chunk.finish_reason)
            print(f"[FINISH_REASON: {chunk.finish_reason}] Content: '{chunk.content}' (Type: {chunk.content_type})")
        else:
            print(f"[STREAMING] Content: '{chunk.content}' (Type: {chunk.content_type})")
    
    print(f"\nSummary:")
    print(f"- Total chunks: {len(content_chunks)}")
    print(f"- Finish reasons seen: {finish_reasons_seen}")
    
    print("\n" + "=" * 50)
    print("Streaming test completed!")


def demonstrate_finish_reason_usage():
    """Demonstrate how to use finish_reason in streaming responses."""
    
    agent = Agent(
        name="Demo Agent", 
        model="gpt-3.5-turbo",
        max_steps=3,
    )
    
    print("Demonstrating finish_reason usage patterns:")
    print("=" * 50)
    
    accumulated_content = ""
    
    for chunk in agent.run("Write a short poem about coding", stream=True):
        # Accumulate content
        accumulated_content += chunk.content
        
        # Handle different finish reasons
        if chunk.finish_reason == "stop":
            print(f"\n✅ Stream completed successfully!")
            print(f"📝 Final content: {accumulated_content}")
            break
        elif chunk.finish_reason == "max_steps_reached":
            print(f"\n⚠️  Stream stopped due to max steps reached")
            print(f"📝 Partial content: {accumulated_content}")
            break
        elif chunk.finish_reason == "error":
            print(f"\n❌ Stream stopped due to error: {chunk.content}")
            break
        elif chunk.finish_reason is None:
            # Still streaming
            print(chunk.content, end="", flush=True)
        else:
            print(f"\n🔧 Tool call or other action: {chunk.finish_reason}")


if __name__ == "__main__":
    # Note: You'll need to set your API key for these tests to work
    # export OPENAI_API_KEY="your-key-here"
    
    try:
        test_streaming_finish_reason()
        print("\n" + "=" * 60)
        demonstrate_finish_reason_usage()
    except Exception as e:
        print(f"Test failed (likely due to missing API key): {e}")
        print("\nTo run this test, set your OPENAI_API_KEY environment variable.") 