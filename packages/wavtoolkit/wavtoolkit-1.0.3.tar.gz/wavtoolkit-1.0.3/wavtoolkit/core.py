import os
from datetime import datetime as dt
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from wave_chunk_parser.chunks import RiffChunk

class WavFile:
    def __init__(self, filepath):
        if not os.path.isfile(filepath):
            raise OSError("File not found")
        self.filepath = os.path.realpath(filepath)
        self.filename = os.path.basename(self.filepath)
        self._stat = os.stat(filepath)
        self.size = self._stat.st_size
        self.created = self._stat.st_ctime
        self.modified = self._stat.st_mtime

        with open(filepath, 'rb') as f:
            self.riff = RiffChunk.from_file(f)

        self.fmt_chunk = self.riff.get_chunk("fmt ")
        self.data_chunk = self.riff.get_chunk("data")
        self.duration = None
        if self.data_chunk and self.fmt_chunk:
            self.duration = len(self.data_chunk.samples) / self.fmt_chunk.sample_rate

        self.loudness = self._analyze_loudness()

        self._metadata_info = None
        self._cart_metadata = None

    def _analyze_loudness(self):
        try:
            data, rate = sf.read(self.filepath)
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            meter = pyln.Meter(rate)
            lufs = meter.integrated_loudness(data)
            peak = np.max(np.abs(data))
            return {
                'IntegratedLUFS': lufs,
                'Peak': peak
            }
        except Exception as e:
            return {'Error': str(e)}

    @property
    def metadata_info(self):
        if self._metadata_info is None:
            self._metadata_info = {}
            try:
                list_chunk = self.riff.get_chunk("LIST", chunk_type=b"INFO")
                if list_chunk:
                    for sub_chunk in list_chunk.sub_chunks:
                        key = sub_chunk.get_name.decode(errors="replace").strip()
                        value = sub_chunk.info.strip()
                        self._metadata_info[key] = value
            except Exception:
                pass
        return self._metadata_info

    @property
    def cart_metadata(self):
        if self._cart_metadata is None:
            self._cart_metadata = {}
            try:
                cart = self.riff.get_chunk("cart")
                if cart:
                    self._cart_metadata = {
                        'title': cart.title,
                        'artist': cart.artist,
                        'category': cart.category,
                        'cut_id': cart.cut_id,
                        'client_id': cart.client_id,
                        'url': cart.url,
                        'tags': cart.tag_text,
                        'timers': [(timer.name, timer.time) for timer in cart.timers]
                    }
            except Exception:
                pass
        return self._cart_metadata

    @property
    def title(self):
        return self.metadata_info.get('INAM') or self.cart_metadata.get('title') or self.filename

    @property
    def artist(self):
        return self.metadata_info.get('IART') or self.cart_metadata.get('artist')

    @property
    def category(self):
        return self.metadata_info.get('ICAT') or self.cart_metadata.get('category')

    def __repr__(self):
        class_info_str = f"WavFile {self.filename}"
        structure_repr = f"{self.fmt_chunk.channels}ch @ {self.fmt_chunk.sample_rate}Hz"
        lufs = self.loudness.get('IntegratedLUFS', '?')
        try:
            lufs_str = f"{lufs:.2f} dB"
        except (TypeError, ValueError):
            lufs_str = str(lufs)
        lufs_repr = f"LUFS: {lufs_str}"
        _strf = '%m/%d/%Y %l:%M:%S %p'
        created_str = dt.fromtimestamp(self.created).strftime(_strf)

        parts = [
            class_info_str,
            structure_repr,
            lufs_repr,
            created_str
        ]
        return f"<{' | '.join(parts)}>"

    def __str__(self):
        dur_str = f"{self.duration:.2f}s" if self.duration else "Unknown duration"
        return f"{self.title} | {dur_str}"