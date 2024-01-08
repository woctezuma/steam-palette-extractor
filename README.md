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
  - Wikipedia: [Red, Green, Blue (RGB)][wiki-rgb]
  - Wikipedia: [Hue, Saturation, Value (HSV)][wiki-hsv] **Caveat**: this is a cylindrical-coordinate representation!
  - Wikipedia: [CIELAB color space (L\*a\*b\*)][wiki-cielab]
  - Wikipedia: [CIELUV color space (L\*u\*v\*)][wiki-cieluv]
- Compare palettes, i.e. ordered lists of a few colors:
  - Mean Pairwise Distance [1, 2]
  - Wikipedia: [Hausdorff distance][wiki-hausdorff] [2]
  - Wikipedia: [Modified Hausdorff "distance" (MHD)][wiki-hausdorff-modified] [2, 3] (in French):
    - which is a modification where the **sup** is replaced by an **average**,
    - which is not actually a distance as it does not exhibit the triangle inequality property,
  - Minimum Color Difference (MCD) [1, 2]:
    - which is a modification of the Hausdorff distance where the **sup and max** are replaced by an **average**,
  - In retrospect, in my code, the distance between palettes is assessed by:
    - a modification of the Hausdorff distance where the **sup and max** are replaced by a (possibly weighted) **sum**,
    - **NB**: Using a sum is equivalent to using an average, as the number of colors in each palette, i.e. the cardinality of each set, is constant.
- Articles:
  - [1] Pan, Qianqian, et al. [*Comparative Evaluation of Color Differences between Color Palettes*][paper-pan]. Color and Imaging Conference 2018.
  - [2] Kim, Suzi, et al. [*Dynamic Closest Color Warping to Sort and Compare Palettes*][paper-DCCW]. [SIGGRAPH][siggraph-DCCW] 2021. ([code][github-DCCW])
  - [3] Dubuisson, M-P., et al. [*A modified Hausdorff distance for object matching*][paper-mhd]. ICPR 1994.

<!-- Definitions -->

[img-cover]: <https://github.com/woctezuma/steam-palette-extractor/wiki/img/cover.jpg>
[colab-notebook]: <https://colab.research.google.com/github/woctezuma/steam-palette-extractor/blob/main/extract_steam_palette.ipynb>
[colab-badge]: <https://colab.research.google.com/assets/colab-badge.svg>
[benchmark-wiki]: <https://github.com/woctezuma/steam-palette-extractor/wiki>
[steam-popular-appids]: <https://github.com/woctezuma/steam-popular-appids>
[steam-store-snapshots]: <https://github.com/woctezuma/steam-store-snapshots>
[stackoverflow]: <https://stackoverflow.com/questions/3241929/python-find-dominant-most-common-color-in-an-image/61730849#61730849>
[wiki-rgb]: <https://en.wikipedia.org/wiki/RGB_color_model>
[wiki-hsv]: <https://en.wikipedia.org/wiki/HSL_and_HSV>
[wiki-cielab]: <https://en.wikipedia.org/wiki/CIELAB_color_space>
[wiki-cieluv]: <https://en.wikipedia.org/wiki/CIELUV>
[wiki-hausdorff]: <https://en.wikipedia.org/wiki/Hausdorff_distance>
[wiki-hausdorff-modified]: <https://fr.wikipedia.org/wiki/Distance_de_Hausdorff_modifi%C3%A9e>
[paper-pan]: <https://www.stephenwestland.co.uk/pdf/pan_westland_CIC_2018.pdf>
[paper-DCCW]: <https://doi.org/10.1145/3450626.3459776>
[siggraph-DCCW]: <https://history.siggraph.org/learning/dynamic-closest-color-warping-to-sort-and-compare-palettes-by-kim-and-choi/>
[github-DCCW]: <https://github.com/SuziKim/DCCW>
[paper-mhd]: <https://doi.org/10.1109/ICPR.1994.576361>
