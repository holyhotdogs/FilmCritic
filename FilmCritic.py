import discord
from discord.ext import commands
import requests

# Define intents
intents = discord.Intents.default()
intents.message_content = True


# Initialize bot with intents and command prefix '!'
bot = commands.Bot(command_prefix='/', intents=intents)

# List to store movies
movies = []
# Variable to store the most recent addition
recently_added = None

# IMDb API base URL
IMDB_API_BASE_URL = "http://www.omdbapi.com/"

# Function to check if the movie exists on OMDb using IMDb API
def movie_exists(title):
    try:
        # Prepare the request parameters
        params = {
            "apikey": "YOUR_OMDB_API_KEY",  # Replace with your OMDb API key
            "t": title,                      # Title of the movie
            "type": "movie"                  # Search for movies only
        }
        
        # Send GET request to IMDb API
        response = requests.get(IMDB_API_BASE_URL, params=params)
        
        # Check if request was successful and movie exists
        if response.status_code == 200 and response.json().get("Response") == "True":
            return True
        else:
            return False
    except Exception as e:
        print("Error occurred while checking movie existence:", e)
        return False

# Add movie command
@bot.command()
async def addmovie(ctx, *, title):
    if movie_exists(title):
        # Add movie to the list
        movies.append(title)
        await ctx.send(f"Movie '{title}' added successfully!")
    else:
        await ctx.send(f"Sorry, '{title}' doesn't seem to exist on IMDb.")

# Watch movie command
@bot.command()
async def watchmovie(ctx, *, title):
    if title in movies:
        await ctx.send(f"Alright @everyone get your popcorn and take a seat, we're watching {title}!")
    else:
        await ctx.send(f"Sorry, '{title}' is not in the movie list.")

# Finished command
@bot.command()
async def finished(ctx, *, title):
    if title in movies:
        await ctx.send(f"Movie '{title}' has been marked as finished.")
        index = movies.index(title)
        movies[index] = f"~~{title}~~"
    else:
        await ctx.send(f"Sorry, '{title}' is not in the movie list.")

# Watched command
@bot.command()
async def watched(ctx):
    watched_list = [movie for movie in movies if movie.startswith('~~')]
    if watched_list:
        await ctx.send("List of watched movies:\n" + '\n'.join(watched_list))
    else:
        await ctx.send("No movies have been marked as watched yet.")

# Watchlist command
@bot.command()
async def watchlist(ctx):
    watchlist = [movie for movie in movies if not movie.startswith('~~')]
    if watchlist:
        await ctx.send("Current watchlist:\n" + '\n'.join(watchlist))
    else:
        await ctx.send("The watchlist is empty.")

# Recent command
@bot.command()
async def recent(ctx):
    global recently_added
    if recently_added:
        await ctx.send(f"The most recent addition to the movie list is '{recently_added}'.")
    else:
        await ctx.send("No movies have been added recently.")

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')
