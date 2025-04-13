import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import configs.DefaultConfig as defaultConfig
import utils.DiscordUtils as discordUtils

from discord.ext import commands

# from google import genai
import google.generativeai as genai

genai.configure(api_key=defaultConfig.gemini_ai_api)

# TODO: Want to truncate TO MAKE 2000 messag length
DISCORD_MAX_MSG_LEN=2000

ERR_MSG="I'm sorry. There was an issue with the question. Please try again..."

models = ['gemini-1.5-flash', 'gemini-pro', 'gemini-2.0-flash']

class GeminiAgent(commands.Cog):
    def __init__(self, bot):
        super().__init__()

        self.bot = bot
        self.model = genai.GenerativeModel(models[2])

    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if msg.content == 'ping gemini-agent':
                await msg.channel.send('Agent is connected...')
        except Exception as ex:
            return ERR_MSG + str(ex)

    @commands.command()
    async def query(self, ctx, question):
        try:
            print('query received')
            raw_response = self.gemini_generate_content(question)
            await self.send_message_in_chunks(ctx, raw_response)

        except Exception as ex:
            return ERR_MSG + str(ex)
        
    @commands.command()
    async def pm(self, ctx):
        dmchannel = await ctx.author.create_dm()
        await dmchannel.send('Hi how can I help you today?')
        
    def gemini_generate_content(self, content):
        try:
            return self.model.generate_content(content, stream=True)
        except Exception as ex:
            return ERR_MSG + str(ex)

    async def send_message_in_chunks(self, ctx, raw_response):
        curr_message = ""

        # raw_response is of type GenerateContentResponse with stream=True
        # Hence, we need to look at each text individually
        for chunk in raw_response:
            curr_message += chunk.text

            # Based on the new added text, send only truncated part
            while len(curr_message) > DISCORD_MAX_MSG_LEN:
                truncated_message = curr_message[:DISCORD_MAX_MSG_LEN]
                rest_of_message = curr_message[DISCORD_MAX_MSG_LEN:]
                
                await ctx.send(truncated_message)
                curr_message = rest_of_message

        # Fence posting
        if len(curr_message) > DISCORD_MAX_MSG_LEN:
            truncated_message = curr_message[:DISCORD_MAX_MSG_LEN]
            rest_of_message = curr_message[DISCORD_MAX_MSG_LEN:]
            
            await ctx.send(truncated_message)
            curr_message = rest_of_message

        await ctx.send(curr_message)
        

        ### NAIVE
        # for i in range(0, len(raw_response), DISCORD_MAX_MSG_LEN):
        #     curr_response = raw_response[i: min(len(raw_response), i + DISCORD_MAX_MSG_LEN)]
        #     # Send each part individually to discord server
        #     await ctx.send(curr_response)

        ### OLD
        # ctx.send(raw_response.text)
