# Softboiler

[![All Contributors](https://img.shields.io/github/all-contributors/softboiler/softboiler.github.io?color=ee8449&style=flat-square)](contributors)

My dissertation projects facilitate the study of nucleate pool boiling with a focus on bubble visualization and analysis:

- [`boilercv`](https://github.com/softboiler/boilercv): Computer vision routines and data processing pipeline. DVC pipeline and equation generation.
- [`copier-pipeline`](https://github.com/softboiler/copier-pipeline): Project template for engineering research data pipelines.
- [`boilerdata`](https://github.com/softboiler/boilerdata): Thermal data processing pipeline.
- [`context_models`](https://github.com/softboiler/context_models): Core functionality for DVC pipeline generation.
- [`boilerdaq`](https://github.com/softboiler/boilerdaq): Data acquisition for the experimental apparatus.
- [`boilercore`](https://github.com/softboiler/boilercore): Utility and test code common to the above. Modules may be split into independent libraries, and may be generally useful for other research. For instance, `captivate` facilitates video and image viewing.
- [`boilercine`](https://github.com/softboiler/boilercine): Read and process CINE files for the [`boilercv`](https://github.com/softboiler/boilercv) pipeline. Will probably migrate to [`pims`](https://pypi.org/project/PIMS/), time permitting.

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
