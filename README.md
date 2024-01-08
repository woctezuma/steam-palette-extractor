# Steam Palette Extractor

This repository contains Python code to find the dominant / most common colors in Steam banners.

![Illustration cover][img-cover]

## Usage

Run [`extract_steam_palette.ipynb`][colab-notebook]
[![Open In Colab][colab-badge]][colab-notebook]

## Results

A benchmark of the parameters used for the palette distance is shown [on the Wiki][benchmark-wiki].

## References

- [`woctezuma/steam-popular-appids`][steam-popular-appids]: popular Steam appIDs,
- [`woctezuma/steam-store-snapshots`][steam-store-snapshots]: a comprehensive list of appIDs downloaded in January 2021,
- [Stack Overflow][stackoverflow]: different approaches to extract the palette of an image.
- Compare colors:
  - Wikipedia: [Hue, Saturation, Value (HSV)][wiki-hsv]
  - Wikipedia: [CIELAB color space (L*a*b*)][wiki-cielab]
  - Wikipedia: [CIELUV color space (L*u*v*)][wiki-cieluv]
- Compare palettes, i.e. ordered lists of a few colors:
  - see my formulas in the code 
  - Kim, Suzi, et al. [*Dynamic Closest Color Warping to Sort and Compare Palettes*][paper-DCCW]. SIGGRAPH 2021. ([code][github-DCCW])

<!-- Definitions -->

[img-cover]: <https://github.com/woctezuma/steam-palette-extractor/wiki/img/cover.jpg>
[colab-notebook]: <https://colab.research.google.com/github/woctezuma/steam-palette-extractor/blob/main/extract_steam_palette.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>
[benchmark-wiki]: <https://github.com/woctezuma/steam-palette-extractor/wiki>
[steam-popular-appids]: <https://github.com/woctezuma/steam-popular-appids>
[steam-store-snapshots]: <https://github.com/woctezuma/steam-store-snapshots>
[stackoverflow]: <https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image/61730849#61730849>
[wiki-hsv]: <https://en.wikipedia.org/wiki/HSL_and_HSV>
[wiki-cielab]: <https://en.wikipedia.org/wiki/CIELAB_color_space>
[wiki-cieluv]: <https://en.wikipedia.org/wiki/CIELUV>
[paper-DCCW]: <https://doi.org/10.1145/3450626.3459776>
[github-DCCW]: <https://github.com/SuziKim/DCCW>
