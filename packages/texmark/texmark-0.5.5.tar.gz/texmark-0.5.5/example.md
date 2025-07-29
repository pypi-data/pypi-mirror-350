---
title: "This is an example title"
authors:
  - firstname: Mahé
    lastname: Perrette
    affiliation: 1
    email: mahe.perrette@gmail.com
  - firstname: Another
    lastname: Author
    affiliation: 2
affiliations:
  - "Alfred Wegener Institut fur Meeres und Polarforschung (AWI)"
  - "Another Institution in a Remote Country"
running:
    title: LGM data assimilation
    author: Perrette et al
date: "2025-07-15"
bibliography: references.bib
journal:
    short: cp
    template: copernicus
---

# Abstract

The abstract will be identified and moved to the metadata,
so that it can be used as in the journal templates.

Each journal has its own template. For now only Copernicus and Science are covered.

# Introduction

The journal templates can be edited in [texmark/templates](/texmark/templates)
and journal-specific filters can be added such as for [copernicus](/texmark/copernicus.py).
Lots of research has been done on that topic.
We focus mostly on @tierney_zhu2020
but also on \cite{tierney_zhu2020}

![My figure. The leading / in images and links is removed, but it is convenient for proper formatting in github.](/images/eof_mean.png){#fig:eofmean}

Figures can referred to as Fig. \ref{fig:eofmean}.
That's an inline equation $a + 1 = 3$.
And a block equation
$$
a + \Sigma_i i^2
$$
and an align environment
\begin{align} \label{eq:aligneq}
a &= 9 + 2 \\
b &= 3
\end{align}

| Names | Values |
| - | - |
| Domain | Ocean |
| Era | Anthropocene |
:A caption for my table {#tab:gulf}

Now equation Equation \ref{eq:aligneq}, Figure \ref{fig:eofmean}, and Table \ref{tab:gulf} can be referenced.
Both latex and markdown commands are supported.

# Conclusions

This is also a special section.

# Appendix

That is an appendix.
The figures can also point to an http(s) address. This is an appendix reference to Figure \ref{fig:appendix}.

![The gulf Stream (https link). Source: Jeremy White/The New York Times.](https://static01.nyt.com/images/2021/03/03/climate/gulf-stream-promo/gulf-stream-promo-superJumbo.jpg){#fig:appendix}