import click

from . import models, structures, adapters
from .tools import Scrapper, Extractor

adapters.control.cli = True


# core group
@click.group()
def cli():
    pass


@click.command("list", help="show list of songs")
def list_songs():
    songs = models.session.query(models.Song).all()
    for song in songs:
        print(f"{song.id: >8}: {song}")


@click.command("add", help="add song from url to db")
# @click.option("--provider", default=None, type=structures.Providers)
@click.argument("url", type=str)
def add_song(url: str):
    for song in Scrapper.scrap(url):
        print(
            f"> {song.id: >8}. {song}",
            f"{chr(171)}{song.description}{chr(187)}",
            f"provided from {structures.Providers(song.provider).name.lower()}",
            f"tags: {', '.join(song.tags) if song.tags else '(None)'}",
            "",
            sep="\n"
        )
    models.session.commit()


@click.command("play", help="play music")
@click.argument("song_id", type=int, metavar="id")
def play_song(song_id: int):
    song = models.session.query(models.Song).get(song_id)
    url = Extractor.extract(song)
    adapters.system.play(url)


@click.command("stats", help="view organizer stats")
def organizer_stats():
    ...  # TODO


cli.add_command(list_songs)
cli.add_command(add_song)
cli.add_command(play_song)
cli.add_command(organizer_stats)
