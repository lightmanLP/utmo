import click

from .models import Song, Session
from .scrapper import Scrapper
from .enums import Providers
from .scrapper import VkAudio


# core group
@click.group()
def cli():
    pass


@click.command("list", help="show list of songs")
def list_songs():
    session = Session()
    songs = session.query(Song).all()
    for song in songs:
        print(f"{song.id: >8}: {song}")


@click.command("add", help="add song from url to db")
@click.option("--provider", default=None, type=Providers)
@click.argument("url", type=str)
def add_song(provider: Providers, url: str):
    # TODO
    scrapper = Scrapper()
    song = scrapper.scrap(url, provider)

    session = Session()
    session.add(song)
    session.commit()


@click.command("stats", help="view organizer stats")
def organizer_stats():
    ...  # TODO


cli.add_command(list_songs)
cli.add_command(add_song)
cli.add_command(organizer_stats)
