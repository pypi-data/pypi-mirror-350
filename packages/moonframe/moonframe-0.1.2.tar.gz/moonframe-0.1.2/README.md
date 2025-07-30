
# Moonframe 
<img src=https://gitlab.com/cerfacs/moonframe/raw/main/docs/images/moonframe.png width=80% alt="Moonframe's banner containing the logo, the title of the repo and a subtitle : d3.js visuals with Python."/>

Moonframe is an open-source Python library that helps you create interactive graphs using D3.js without writing a single line of JavaScript. It’s built for quick data exploration and aims to be as simple and accessible as possible.

Right now (v0.0.0), it only supports scatter plots; with more chart types on the way.

## Main features
### Easy to setup

Moonframe comes with a minimalist CLI: one command, one graph.
Your data just needs to be in CSV format; a widely used and simple standard in the data visualization community.
Just type `moonframe` in any terminal:

```bash
>moonframe
Usage: moonframe [OPTIONS] COMMAND [ARGS]...

  Package moonframe v0.0.0

  ---------------------------  Moonframe  ----------------------------

  You are now using the Command line interface of moonframe package, a set of
  tools created at CERFACS (https://cerfacs.fr).

  This is a python package currently installed in your python environement.

  All graphs are displayed in your default web browser.

Options:
  --help  Show this message and exit.

Commands:
  scatter  Scatter plot
```

### Customizable charts without coding

Moonframe provides a clear interface that handles all customization. You can easily navigate between graph views to explore your dataset.

<img src=https://gitlab.com/cerfacs/moonframe/raw/main/docs/images/readme/ex1.gif width=60% alt="Scatter plot demo. A menu on the left allows you to select the names of the columns you want to plot. You can change X,Y, size and color."/>

### Interact with the data

Tooltips are available on all charts. They show details from your data when you hover over a point, and you can fully customize what they display. This can be helpful for getting quick insights. You can also highlight color groups on hover to spot trends more easily in your dataset.

<img src=https://gitlab.com/cerfacs/moonframe/raw/main/docs/images/readme/ex2.gif width=60% alt="Scatter plot demo. When the mouse hovers over a point, text appears describing the data associated with that point."/>

## Installation

Install it from PyPI with : 

```
pip install moonframe
``` 

## Note

*The data set used for these examples comes from INSEE, a french institut focus on statistics and economics studies. Get the data [here](https://www.insee.fr/fr/statistiques/6652024?sommaire=6652160).*