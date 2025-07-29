import asyncio
import discord

HISTORY_LIMIT = 20
EMOJI = "‼"

class DiscordBot(discord.Client):
    """
    A simple Discord bot that forwards the bug reports to a given Discord channel.

    Attributes:
        token (str): bot token
        channel_id (int): the ID of the channel to send messages to
        _message (str): message to send
        _alreadySent (bool): whether the message has already been sent
        _done_future (asyncio.Future): a future that is set when the bot is done
    """
    def __init__(self, token: str, channelId: str | int) -> None:
        """
        Initializes the Discord bot with the given token and channel ID.

        Args:
            token (str): bot token
            channel_id (int): the ID of the channel to send messages to
        """
        self.token = token
        self.channelId = int(channelId)
        self._message = None
        self._alreadySent = False
        self._doneFuture = None

        intents = discord.Intents(emojis = True,
                                  guild_reactions = True,
                                  message_content = True,
                                  guild_messages = True,
                                  guilds = True)
        super().__init__(intents=intents)

    async def send_message(self, message, alreadySent = False):
        """
        Sends a message to the specified channel by setting the variables and starting the bot, then turning it off when finished.

        Args:
            message (str): The message to send.
            alreadySent (bool): Whether the message has already been sent.
        """
        self._message = message
        self._alreadySent = alreadySent
        self._doneFuture = asyncio.get_running_loop().create_future()
        print("Starting bot...")
        # Start the bot as a background task
        asyncio.create_task(self.start(self.token))
        # Wait until the message is sent and the bot is closed
        await self._doneFuture

    async def on_ready(self):
        """
        Called when the bot is ready. Also sends the message to the specified channel, or reacts if it's been sent.
        """
        try:
            channel = await self.fetch_channel(self.channelId)
            if channel and not self._alreadySent:
                await channel.send(self._message)
                print(f"Sent message to channel {self.channelId}")
            elif channel and self._alreadySent:
                async for message in channel.history(limit=HISTORY_LIMIT):
                    if message.content == self._message:
                        await message.add_reaction(EMOJI)
                        break
            else:
                print(f"Channel with ID {self.channelId} not found.")
        except Exception as e:
            print(f"Error sending message: {e}")
        finally:
            print("Shutting down bot...")
            await self.close()
            # Mark the future as done so send_message can return
            if self._doneFuture and not self._doneFuture.done():
                self._doneFuture.set_result(True)