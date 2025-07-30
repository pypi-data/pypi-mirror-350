# wavtoolkit

**`wavtoolkit`** is a lightweight Python library for extracting and analyzing metadata from WAV files. Useful for inspecting audio files without diving into low-level byte handling.
It uses `wave_chunk_parser` for parsing complex RIFF structures and `pyloudnorm` for loudness analysis.

## Features

- **Extracts key metadata**:
  - Title, artist, category (from `INFO` and `cart` chunks)
  - Audio format (sample rate, channels, bit depth)
  - File properties (size, creation time, modification time)
  - Loudness metrics (Integrated LUFS, Peak)

- **Lazy-loading design**:
  - Metadata is parsed on-demand
  - Efficient and modular

- **Simple API**, ready for scripting

## Installation

```bash
pip install wavtoolkit
```

## Usage

```python
import os
from wavtoolkit import WavFile

wavs = [WavFile(f) for f in os.listdir() if f.endswith(".wav")]

for wav in wavs:
  # Filename
  print('\n', wav.filename)
  
  # Title and duration
  print(f"    {wav}")
  
  # Loudness metrics (LUFS, Peak)
  for k, v in wav.loudness.items():
    print(f"    {k}: {v.item()}")
  
  # Metadata from INFO chunks
  for k, v in wav.metadata_info.items():
    v = v.decode() if isinstance(v, bytes) else v
    print(f"    [{k}] {v}")
  
  # Metadata from CART chunks
  print(f"    {wav.cart_metadata or ''}\n")
  
```

Example output:

```plaintext
Chaos_a_la_Mode_RM_Mixdown_3.wav
  Chaos á la Mode (Re-Remastered) | 475.93s
  IntegratedLUFS: -14.537535931432476
  Peak: 0.8768768310546875
  [IPRD] Something Else
  [IART] DJ Stomp
  [ICRD] 2025
  [IGNR] Trap
  [INAM] Chaos á la Mode (Re-Remastered)
```

## Why `wavtoolkit`?

- **Leverages** existing libraries (`wave_chunk_parser`, `pyloudnorm`)
- **No low-level hacks** — just clean, high-level metadata access
- **Modular design** for integration into pipelines or tools


## License

MIT

## Credits

- [wave_chunk_parser](https://github.com/deeuu/wave-chunk-parser)
- [pyloudnorm](https://github.com/csteinmetz1/pyloudnorm)

## Coming Soon (?)

- Cue point parsing
- JSON metadata export
