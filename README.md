## Overview

Pipewire-py is a project created to generate python bindings for [libpipewire](https://gitlab.freedesktop.org/pipewire/pipewire) C library.

It is using [pcpp](https://pypi.org/project/pcpp/), [pycparserext](https://pypi.org/project/pycparserext/) and [cffi](https://pypi.org/project/cffi/) to preprocess, parse C headers and provide python binding. 

## OS package dependency:
needs to be installed by hand

> libpipewire-0.3-dev

## Examples
Python examples based on original [API Tutorial
](https://docs.pipewire.org/page_tutorial.html)

- Part 1: [Getting Started](tutorial1.py) ([original](https://docs.pipewire.org/page_tutorial1.html))
- Part 2: [Enumerating Objects](tutorial2.py) ([original](https://docs.pipewire.org/page_tutorial2.html))
- Part 3: [Forcing A Roundtrip](tutorial3.py) ([original](https://docs.pipewire.org/page_tutorial3.html))
- Part 4: [Playing A Tone](tutorial4.py) ([original](https://docs.pipewire.org/page_tutorial4.html))
- Part 5: [Capturing Video Frames](tutorial5.py) ([original](https://docs.pipewire.org/page_tutorial5.html))
- Part 6: [Binding Objects](tutorial6.py) ([original](https://docs.pipewire.org/page_tutorial6.html))