# Required stuff
from pytube import YouTube, Stream

# CLI stuff
from progressbar import Bar, FileTransferSpeed, UnknownLength, DataTransferBar, Percentage, DataSize
from pick import pick
from humanfriendly import format_size
import click

@click.command()
@click.option('-u', '--url', prompt=True, type=str)
@click.option('-i', '--itag', type=int, help='The itag for using a stream', required=False)
def main(url: str, itag: int):
    widgets = [
        Percentage(),
        Bar(),
        FileTransferSpeed(),
        DataSize()
    ]

    bar = DataTransferBar(max_value=UnknownLength, widgets=widgets)

    file_size: int

    def updateBar(stream, chunk, remaining):
        percent = file_size - remaining + 1000000

        try:
            # updates the progress bar
            bar.update(round(percent / 1000000, 2))
        except:
            # progress bar dont reach 100% so a little trick to make it 100
            bar.update(round(file_size / 1000000, 2))

    print('Going down da tube...')
    yt = YouTube(url, on_progress_callback=updateBar)

    def mapStream(stream: Stream):
        return f'{stream.mime_type} | {format_size(stream.filesize)} | {stream.resolution} | itag: {stream.itag}'

    streams = yt.streams

    s: Stream

    if itag is not None:
        s = streams.get_by_itag(itag=itag)
    else:
        if len(streams) >= 17:
            if click.confirm(f'Seems like that there are {len(streams)} streams, It will take a while to fetch all '
                             f'streams. If you have speedy internet, you may ignore that. Do you want to wait for the '
                             f'picker or find by itag instead?'):
                s = pick(streams, 'Which stream?', options_map_func=mapStream)[0]
            else:
                print('Lemme print all the available streams')
                [print(mapStream(s)) for s in streams]
                s = streams.get_by_itag(itag=click.prompt('Which itag?', type=int))


    print(mapStream(s))

    file_size = s.filesize | s.filesize_approx
    bar.max_value = s.filesize | s.filesize_approx

    print('Downloading...')

    s.download(filename=s.title)

if __name__ == '__main__':
    main()