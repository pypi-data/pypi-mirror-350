# MSHack

This repository allows you to download sheet music in PDF format from the MusicScore website.

### Usage

To use the package, you need to define a save path and then save the PDF.:

```python
from mshack import save_score, set_save_dir

# Defines where to save PDF
set_save_dir("PDF folder")

# Saves sheet music as PDF
path_to_saved_PDF = save_score("https://musescore.com/user/10919536/scores/2377386")

if path_to_score:
    pass
```

Be prepared to wait a long time (~1.5 minutes). Yeah... I don't know how to download sheets faster. Not yet.


