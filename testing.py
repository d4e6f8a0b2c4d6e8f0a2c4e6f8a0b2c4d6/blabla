import discord
from openai import OpenAI

DISCORD_BOT_TOKEN = "MTU0Nzk2NzIxMjQyNDI3Mzk3Mg.GPCHt4.4Hf2PEsNDuI98CD_a10_c7v_DDDYvQO_bIO1r8"
AGENTROUTER_API_KEY = "sk-lBrrg92YvEroJ1FQj6umcrUFta9nxA0VBXt91ORKsIBpwF1b"

AI_MODEL = "glm-5.3" 

ai_client = OpenAI(
    api_key=AGENTROUTER_API_KEY,
    base_url="http://localhost:8318/v1"
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        user_prompt = message.content.replace(f'<@{client.user.id}>', '').strip()
        
        if not user_prompt:
            await message.channel.send("Hello! How can I help you?")
            return

        async with message.channel.typing():
            try:
                response = ai_client.chat.completions.create(
                    model=AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful Discord assistant."},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                
                ai_reply = response.choices[0].message.content
                
                if len(ai_reply) > 2000:
                    for i in range(0, len(ai_reply), 2000):
                        await message.channel.send(ai_reply[i:i+2000])
                else:
                    await message.channel.send(ai_reply)
                    
            except Exception as e:
                await message.channel.send(f"Sorry, I encountered an error: {e}")

client.run(DISCORD_BOT_TOKEN)
