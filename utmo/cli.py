from typing import Optional
from pathlib import Path
import pickle

import click

from . import models, structures, adapters
from .tools import Scrapper, Extractor


adapters.control.mode = structures.ControlMode.CLI
models.init()


# core group
@click.group()
def cli():
    pass


@cli.command("list", help="show list of songs")
def list_songs():
    songs = models.session.query(models.Song).all()
    for song in songs:
        print(f"{song.id: >4}: {song}")


@cli.command("add", help="add song from url to db")
# @click.option("--provider", default=None, type=structures.Provider)
@click.argument("url", type=str)
def add_song(url: str):
    for song in Scrapper.scrap(url):
        print(song.id)
        print(
            f"> {song.id: >4}. {song}",
            f"{chr(171)}{song.description}{chr(187)}",
            f"provided from {structures.Provider(song.provider).name.lower()}",
            f"tags: {', '.join(map(str, song.tags)) or '(None)'}",
            "",
            sep="\n"
        )
    models.session.commit()


@cli.command("play", help="play music")
@click.argument("song_id", type=int, metavar="id")
def play_song(song_id: int):
    song = models.session.query(models.Song).get(song_id)
    url = Extractor.extract(song)
    adapters.system.play_by_url(url)


@cli.command("stats", help="view organizer stats")
def organizer_stats():
    ...  # TODO


@cli.command("export", help="export songs")
@click.option("-o", "--output", default="songs.pickle", type=click.Path())
@click.option("-p", "--save-plays", is_flag=True)
@click.option("-l", "--export-locals", is_flag=True)
def export_songs(
    output: str,
    save_plays: bool,
    export_locals: bool
):
    output = Path(output)
    data = models.Song.export_songs(save_plays, export_locals)
    output.write_bytes(pickle.dumps(data))
    print("export done")  # FIXME: rework echo


@cli.command("import", help="import songs")
@click.argument("file", type=click.Path(exists=True))
def import_songs(file: str):
    file = Path(file)
    data = pickle.loads(file.read_bytes())
    models.Song.import_songs(data)
    print("import done")  # FIXME: rework echo


@cli.command("search", help="search for songs by tags and names")
def search_song():
    ...  # TODO


@cli.command("remove", help="removes songs")
def remove_songs(*ids: int):  # FIXME
    ...  # TODO


@cli.command("edit", help="edit song data")
def edit_song():
    ...  # TODO
