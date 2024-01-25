# Steam Palette Extractor

This repository contains Python code to find the dominant / most common colors in Steam banners.

![Illustration cover][img-cover]

## Usage

Run [`extract_steam_palette.ipynb`][colab-notebook]
[![Open In Colab][colab-badge]][colab-notebook]

## Approach

A palette is an ordered list of N colors.
In our case, N is arbitrarily set to 8.

We consider:
- a source palette, typically the palette of the gift wrapping,
- a database of target palettes, typically the palettes of every Steam game.

### Match colors

In order to match palettes, we first need to be able to match colors.

Colors can be represented in the following spaces:
- RGB,
- HSV:
  - raw,
  - linearized,
- CIE LAB,
- CIE LUV.

The distance between colors is the L2 norm in this space.

It is possible to take into account:
- the index of the color in the target palette,
- the difference between the indices of the colors in the source and target palettes.

The objective is to incentivize the matching to colors which are respetively:
- predominant in the target palettes, i.e. with low indices,
- at lease more predominant in the target than in the source palette, i.e. with lower indices.

In the latter case, thresholds can be used in order not to distinguish between target colors which have an index lower than the color in the source palette.

### Match palettes

The distance between colors can be:
- the Mean Pairwise Distance,
- the Hausdorff distance,
- a modified Hausdorff "distance",
- a custom Hausdorff distance, similar to Minimum Color Difference.

It is possible to take into account:
- the index of the color in the source palette.

The objective is to re-weigh the color distances in order to give more importance to the errors for colors which are predominant in the **source** palette.
The weights can be normalized so that they sum to 1, as the idea is only to re-balance the terms in the error.

As with the matching of colors, it is possible to take into account:
- the index of the color in the target palette,
- the difference between the indices of the colors in the source and target palettes.

Here, in contrast to what was done with the matching of colors, the idea is to penalize rather than incentivize.

As with the matching of colors, thresholds can be used for more subtle touches.

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
- Compare palettes, i.e. **ordered** lists of a few colors:
  - Mean Pairwise Distance [1, 2]
  - Wikipedia: [Hausdorff distance][wiki-hausdorff] [2]
  - Wikipedia: [Modified Hausdorff "distance" (MHD)][wiki-hausdorff-modified] [2, 3] (in French):
    - which is a modification where the **sup** is replaced by an **average**,
    - which is not actually a distance as it does not exhibit the triangle inequality property,
  - Minimum Color Difference (MCD) [1, 2]:
    - which is a modification of the Hausdorff distance where the **sup and max** are replaced by an **average**,
  - In retrospect, in my code, the distance between palettes is assessed by:
    - a modification of the Hausdorff distance where the **sup and max** are replaced by a (weighted) **sum**,
    - **NB**: Using a sum or an average is equivalent if the number of colors in each palette, i.e. the cardinality of each set, is constant.
    - **NB²**: The weights allow to take advantage of the **order** of colors in the palettes. If one of `exponent` and `factor` is equal to 0, then the weights are all equal to 1, i.e. the weighted sum is simply a sum.
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
