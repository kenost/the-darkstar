# The Darkstar

[Read the latest edition](https://kenost.github.io/the-darkstar/) · [Browse previous editions](https://kenost.github.io/the-darkstar/#archive)

**The Darkstar** is a daily, newspaper-style guide to research on black holes, neutron stars, and the people who study them. Each edition mixes accessible explainers with deeper analysis and a profile of a recent research team. Stories link to the original publications, usually arXiv preprints.

## What this repository contains

The default `main` branch is the **published static website**. The [source branch](https://github.com/kenost/the-darkstar/tree/source) holds the publisher and deployment code. Private credentials and local issue data are not stored in either branch.

| Path | Contents |
| --- | --- |
| `index.html` | The latest edition and archive index |
| `issues/YYYY-MM-DD/index.html` | Permanent pages for past daily editions |
| `assets/` | Cover and article illustrations, plus credited photography |
| `style.css`, `theme.js` | Mobile-friendly newspaper layout and light/dark switch |
| `.nojekyll` | Keeps GitHub Pages from altering the generated files |

The archive grows as new editions are published. The local publishing job prepares an issue from recent freely available research, checks it against previous coverage to reduce repetition, then uploads the complete static site here. GitHub Pages serves it at the stable address above. If research retrieval or generation fails, the previous edition stays available.

## Editorial approach

Articles aim to explain the physical question, the method, the result, and its limitations without treating a preprint as settled science. AI assists with research selection, drafting, source checks, and conceptual artwork; those automated checks are **not independent fact-checking**. Illustrations are not observational images or research figures unless specifically identified as such. Original-paper links and, where applicable, image credits appear with the stories. [Photo credits](assets/PHOTO-CREDITS.md) identify reused photography and its license.

This project is an independent research newspaper, not a publication of arXiv or the research teams it covers.
