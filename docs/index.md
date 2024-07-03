# softboiler_github_io

[![All Contributors](https://img.shields.io/github/all-contributors/softboiler/softboiler.github.io?color=ee8449&style=flat-square)](../README.md#contributors)

My dissertation projects facilitate the study of nucleate pool boiling with a focus on bubble visualization and analysis:

- [`boilercv`](https://softboiler.org/boilercv): Computer vision routines.
- [`boilerdata`](https://softboiler.org/boilerdata): Data processing pipeline.
- [`boilerdaq`](https://softboiler.org/boilerdaq): Data acquisition for the experimental apparatus.
- [`boilercore`](https://softboiler.org/boilercore): Utility and test code common to the above. Modules may be split into independent libraries, and may be generally useful for other research. For instance, `captivate` facilitates video and image viewing.
- [`boilercine`](https://softboiler.org/boilercine): Read and process CINE files for the [`boilercv`](https://github.com/softboiler/boilercv) pipeline. Will probably migrate to [`pims`](https://pypi.org/project/PIMS/), time permitting.
- [`copier-python`](https://github.com/blakeNaccarato/copier-python): General-purpose Python project template. I intend to furnish a science-focused version of this template in `softboiler`.

Another goal of this organization's [website](https://softboiler.org/) will be to aggregate and highlight other thermal science research software in the field, with a focus on open-source projects that follow the FAIR Guiding Principles. Such projects focus on improving the **F**indability, **A**ccessibility, **I**nteroperability, and **R**euse of their data, methods, and research.

:::{toctree}
:hidden:
contributing
examples/index
changelog
contributors
apidocs/index
references
:::
