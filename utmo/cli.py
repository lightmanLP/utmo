import click
import vk_api

from . import models, enums
from .scrapper import Scrapper


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
@click.option("--provider", default=None, type=enums.Providers)
@click.argument("url", type=str)
def add_song(provider: enums.Providers, url: str):
    # TODO
    scrapper = Scrapper()
    song = scrapper.scrap(url, provider)

    models.session.add(song)
    models.session.commit()


@click.command("stats", help="view organizer stats")
def organizer_stats():
    ...  # TODO


cli.add_command(list_songs)
cli.add_command(add_song)
cli.add_command(organizer_stats)