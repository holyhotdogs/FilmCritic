import discord
from discord.ext import commands
import requests
import logging
from datetime import datetime

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with intents and command prefix '/'
bot = commands.Bot(command_prefix='/', intents=intents)

# Set up logging
logging.basicConfig(filename='bot_errors.log', level=logging.ERROR)

# Dictionary to store movies with their addition date/time
movies = {}

# OMDB API base URL
OMDB_API_BASE_URL = "http://www.omdbapi.com/"
OMDB_API_KEY = "YOUR_OMDB_API_KEY"  # Replace with your OMDB API key

# Function to check if the movie exists on OMDB using OMDB API
def movie_exists(title):
    try:
        # Prepare the request parameters
        params = {
            "apikey": OMDB_API_KEY,
            "t": title,
            "type": "movie"
        }
        
        # Send GET request to OMDB API
        response = requests.get(OMDB_API_BASE_URL, params=params)
        
        # Check if request was successful and movie exists
        if response.status_code == 200 and response.json().get("Response") == "True":
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error occurred while checking movie existence for '{title}': {e}")
        return False

# Function to search for movie details using OMDB API
def search_movie_details(title):
    try:
        # Prepare the request parameters
        params = {
            "apikey": OMDB_API_KEY,
            "t": title,
            "plot": "full"  # Get full plot description
        }

        # Send GET request to OMDB API
        response = requests.get(OMDB_API_BASE_URL, params=params)
        movie_data = response.json()

        # Check if request was successful and movie exists
        if response.status_code == 200 and movie_data.get("Response") == "True":
            return movie_data
        else:
            return None
    except Exception as e:
        logging.error(f"Error occurred while searching for movie details for '{title}': {e}")
        return None

# Command to search for movie details
@bot.command()
async def moviedetails(ctx, *, title):
    movie_data = search_movie_details(title)
    if movie_data:
        # Format and display movie details
        embed = discord.Embed(title=movie_data['Title'], description=movie_data['Plot'], color=discord.Color.blue())
        embed.set_thumbnail(url=movie_data['Poster'])
        embed.add_field(name="Director", value=movie_data['Director'], inline=True)
        embed.add_field(name="Release Date", value=movie_data['Released'], inline=True)
        embed.add_field(name="Cast", value=movie_data['Actors'], inline=False)
        embed.add_field(name="IMDB Rating", value=movie_data['imdbRating'], inline=True)
        embed.add_field(name="Genre", value=movie_data['Genre'], inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Sorry, '{title}' details could not be found.")

# Add movie command
@bot.command()
async def addmovie(ctx, *, title):
    if movie_exists(title):
        # Add movie to the dictionary with current date/time
        movies[title] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await ctx.send(f"Movie '{title}' added successfully!")
    else:
        await ctx.send(f"Sorry, '{title}' doesn't seem to exist on OMDB.")

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
        del movies[title]
    else:
        await ctx.send(f"Sorry, '{title}' is not in the movie list.")

# Watched command
@bot.command()
async def watched(ctx):
    if movies:
        try:
            sorted_movies = sorted(movies.items(), key=lambda x: x[0]) # Sort movies alphabetically
            movie_list = [f"{movie[0]} (Added: {movie[1]})" for movie in sorted_movies]
            await ctx.send("List of watched movies:\n" + '\n'.join(movie_list))
        except Exception as e:
            logging.error(f"Error occurred while processing watched command: {e}")
            await ctx.send("Oops! Something went wrong while fetching the watched movies.")
    else:
        await ctx.send("No movies have been added yet.")

# Watchlist command
@bot.command()
async def watchlist(ctx):
    if movies:
        try:
            sorted_movies = sorted(movies.items(), key=lambda x: x[0]) # Sort movies alphabetically
            movie_list = [f"{movie[0]} (Added: {movie[1]})" for movie in sorted_movies]
            await ctx.send("Current watchlist:\n" + '\n'.join(movie_list))
        except Exception as e:
            logging.error(f"Error occurred while processing watchlist command: {e}")
            await ctx.send("Oops! Something went wrong while fetching the watchlist.")
    else:
        await ctx.send("The watchlist is empty.")

# Recent command
@bot.command()
async def recent(ctx):
    if movies:
        try:
            latest_movie = max(movies, key=movies.get)
            await ctx.send(f"The most recent addition to the movie list is '{latest_movie}' (Added: {movies[latest_movie]}).")
        except Exception as e:
            logging.error(f"Error occurred while processing recent command: {e}")
            await ctx.send("Oops! Something went wrong while fetching the most recent movie.")
    else:
        await ctx.send("No movies have been added yet.")

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')
