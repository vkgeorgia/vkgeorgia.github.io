import asyncio
import websockets
import ssl

async def test_avatar():
    uri = "wss://ai-avatar-fgv7vwypqq-uc.a.run.app/ws/chat"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        # Test question to trigger M-Shape persona
        message = "Tell me about your M-Shape philosophy. What is your 'Ant-Colony' principle?"
        print(f"Sending: {message}")
        await websocket.send(message)
        
        response = await websocket.recv()
        print(f"Received: {response}")

if __name__ == "__main__":
    asyncio.run(test_avatar())
