# itunes.py
"""
Higher-level wrapper layer on top of appscript.
appscript just provides a raw wrapper on top of Apple Script.  These are
meant to be clean, friendly, object wrappers.
"""

import appscript as _appscript
#from appscript import k as _KIND

def _property(name, read_only=False, doc=None):
    def _get_attr(self):
        return self._self.__getattr__(name).get()
    def _set_attr(self, value):
        self._self.__getattr__(name).set(value)
    docstring = None
    if doc and read_only:
        docstring = "%s\nRead-only." % doc
    elif doc:
        docstring = doc
    elif read_only:
        docstring = "Read-only."
    if read_only: return property(_get_attr, None, doc=docstring)
    return property(_get_attr, _set_attr, doc=docstring)


class iTunes(object):
    """
    iTunes, your friendly Mac Music Player.
    """
    class Library(object):
        def __init__(self, _library):
            self._self = _library

        _playlists = _property('playlists')

        def find_playlist(self, name):
            """
            Finds a user playlist of the specified name.
            """
            for playlist in self._playlists:
#                if playlist.special_kind.get() != _appscript.k.none:
#                    continue
                if playlist.name.get() == name:
                    return iTunes.Playlist(playlist)

        def _get_special_playlist(self, kind):
            for playlist in self._playlists:
                if playlist.special_kind.get() == kind:
                    return iTunes.Playlist(playlist)

        def library_playlist(self):
            return self.find_playlist('Library')

        def music_playlist(self):
            return self._get_special_playlist(_appscript.k.Music)

        def __str__(self):
            return self.name


    class Playlist(object):
        def __init__(self, _playlist):
            self._self = _playlist

        duration = _property('duration', read_only=True)
        index = _property('index', read_only=True)
        name = _property('name')
        _parent = _property('name', read_only=True)
        shuffle = _property('shuffle')
        size = _property('size', read_only=True)
        song_repeat = _property('song_repeat')
        _special_kind = _property('special_kind', read_only=True)
        time = _property('time', read_only=True)
        visible = _property('visibile', read_only=True)

        def __str__(self):
            return self.name

        def play(self):
            self._self.play()

        _tracks = _property('tracks')
        def tracks(self):
            """
            Returns a list of all tracks in the playlist.
            """
            return [iTunes.Track(track) for track in self._tracks]

        def search(self, text):
            """
            Finds tracks in the playlist which contain 'text' somewhere in
            their title, artist, album, etc.
            """
            return [iTunes.Track(track)
                    for track in self._self.search(self._self, for_=text)]

        def reveal(self):
            return self._self.reveal()

    class Track(object):
        def __init__(self, _track):
            self._self = _track

        album = _property('album')
        album_artist = _property('album_artist')
        album_rating = _property('album_rating')
        _album_rating_kind = _property('album_rating_kind', read_only=True)
        artist = _property('artist')
        bit_rate = _property('bit_rate', read_only=True)
        bookmark = _property('bookmark')
        bookmarkable = _property('bookmarkable')
        bpm = _property('bpm')
        category = _property('category')
        comment = _property('comment')
        compilation = _property('compilation')
        composer = _property('composer')
        database_ID = _property('database_ID', read_only=True)
        date_added = _property('date_added', read_only=True)
        description = _property('description', read_only=True)
        disc_count = _property('disc_count')
        disc_number = _property('disc_number')
        duration = _property('duration', read_only=True)
        enabled = _property('enabled')
        episode_ID = _property('episode_ID')
        episode_number = _property('episode_number')
        EQ = _property('EQ')
        finish = _property('finish')
        gapless = _property('gapless')
        genre = _property('genre')
        grouping = _property('grouping')
        kind = _property('kind', read_only=True)
        long_description = _property('long_description')
        lyrics = _property('lyrics')
        modification_date = _property('modification_date', read_only=True)
        played_count = _property('played_count')
        played_date = _property('played_date')
        podcast = _property('podcast', read_only=True)
        rating = _property('rating')
        _rating_kind = _property('rating_kind', read_only=True)
        sample_rate = _property('sample_rate', read_only=True)
        season_number = _property('season_number')
        shufflable = _property('shufflable')
        skipped_count = _property('skipped_count')
        skipped_date = _property('skipped_date')
        show = _property('show')
        sort_album = _property('sort_album')
        sort_artist = _property('sort_artist')
        sort_album_artist = _property('sort_album_artist')
        sort_name = _property('sort_name')
        sort_composer = _property('sort_composer')
        sort_show = _property('sort_show')
        size = _property('size', read_only=True)
        start = _property('start')
        time = _property('time', read_only=True)
        track_count = _property('track_count')
        track_number = _property('track_number')
        unplayed = _property('unplayed')
        _video_kind = _property('video_kind')
        volume_adjustment = _property('volume_adjustment')
        year = _property('year')
        name = _property('name')
        location = _property('location', read_only=True)

        def __str__(self):
            return self.name

        def play(self, once=True):
            """
            Plays the track.
            If once=True (default), plays just this track, and then stops.
            If once=False, continues playing afterwards.
            """
            self._self.play(once=once)

        def reveal(self):
            return self._self.reveal()


    def __init__(self):
        self._self = _appscript.app('iTunes')
        for track in self.search("Never Gonna Give You Up"):
            if track.artist == "Rick Astley":
#                track.play(once=True)
                break

    _current_playlist = _property('current_playlist', read_only=True)
    current_stream_title = _property('current_stream_title', read_only=True)
    current_stream_URL = _property('current_stream_url', read_only=True)
    _current_track = _property('current_track', read_only=True)
    _current_visual = _property('current_visual', read_only=True)
    frontmost = _property('frontmost')
    full_screen = _property('full_screen')
    mute = _property('mute', doc="True/False mute-status, set to mute/unmute.")
    sound_volume = _property('sound_volume', doc="Integer, [0-100]")

    def current_playlist(self):
        return iTunes.Playlist(self._current_playlist)
    def current_track(self):
        return iTunes.Track(self._current_track)

    _sources = _property('sources')
    def library(self):
        for src in self._sources:
            if src.kind.get() == _appscript.k.library:
                return iTunes.Library(src)

    def find_playlist(self, name):
        return self.library().find_playlist(name)

    def play_playlist(self, name):
        self.library().find_playlist(name).play()

    def library_playlist(self):
        return self.library().library_playlist()

    def music_playlist(self):
        return self.library().music_playlist()

    def search(self, text):
        return self.library_playlist().search(text)

    def add(self, filename):
        return self._self.add(filename)
    def back_track(self):
        self._self.back_track()
    def _convert(self, tracks):
        return self._self.convert(tracks)
    def fast_forward(self):
        self._self.fast_forward()
    def next_track(self):
        self._self.next_track()
    def pause(self):
        self._self.pause()
    def play(self):
        self._self.play()
    def playpause(self):
        self._self.playpause()
    def previous_track(self):
        self._self.previous_track()
    def resume(self):
        self._self.resume()
    def _reveal(self, item):
        self._self.reveal(item)
    def reveal(self, item):
        self._reveal(item._self)
    def rewind(self):
        self._self.rewind()
    def stop(self):
        self._self.stop()
    def _update(self, ipod):
        self._self.update(ipod)
    def _eject(self, ipod):
        self._self.eject(ipod)
    def subscribe(self, url):
        self._self.subscribe(url)
    def updateAllPodcasts(self):
        self._self.updateAllPodcasts()
    def _download(self, track):
        self._self.download(track)


