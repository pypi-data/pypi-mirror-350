<!-- H1 title omitted because our logo acts as the title. -->
<div align="center">

<img width="300px" alt="Qubitron logo" src="https://raw.githubusercontent.com/amyssnippet/Qubitron/refs/heads/main/docs/images/Qubitron_logo_color.svg">

Python package for writing, manipulating, and running [quantum
circuits](https://en.wikipedia.org/wiki/Quantum_circuit) on quantum computers
and simulators.

[![Licensed under the Apache 2.0
license](https://img.shields.io/badge/License-Apache%202.0-3c60b1.svg?logo=opensourceinitiative&logoColor=white&style=flat-square)](https://github.com/amyssnippet/Qubitron/blob/main/LICENSE)
[![Compatible with Python versions 3.11 and
higher](https://img.shields.io/badge/Python-3.11+-fcbc2c.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![OpenSSF Best Practices](https://img.shields.io/badge/dynamic/json?label=OpenSSF&logo=springsecurity&logoColor=white&style=flat-square&colorA=gray&colorB=d56420&suffix=%25&query=$.badge_percentage_0&uri=https://bestpractices.coreinfrastructure.org/projects/10063.json)](https://www.bestpractices.dev/projects/10063)
[![Qubitron project on
PyPI](https://img.shields.io/pypi/v/qubitron.svg?logo=python&logoColor=white&label=PyPI&style=flat-square&color=fcbc2c)](https://pypi.org/project/qubitron)
[![Archived in
Zenodo](https://img.shields.io/badge/10.5281%2Fzenodo.4062499-gray.svg?label=DOI&logo=doi&logoColor=white&style=flat-square&colorA=gray&colorB=3c60b1)](https://doi.org/10.5281/zenodo.4062499)

[Features](#features) &ndash;
[Installation](#installation) &ndash;
[Quick Start](#quick-start--hello-qubit-example) &ndash;
[Documentation](#qubitron-documentation) &ndash;
[Integrations](#integrations) &ndash;
[Community](#community) &ndash;
[Citing Qubitron](#citing-qubitron) &ndash;
[Contact](#contact)

</div>

## Features

Qubitron provides useful abstractions for dealing with today’s [noisy
intermediate-scale quantum](https://arxiv.org/abs/1801.00862) (NISQ) computers,
where the details of quantum hardware are vital to achieving state-of-the-art
results. Some of its features include:

*   Flexible gate definitions and custom gates
*   Parameterized circuits with symbolic variables
*   Circuit transformation, compilation and optimization
*   Hardware device modeling
*   Noise modeling
*   Multiple built-in quantum circuit simulators
*   Integration with [qsim](https://github.com/amyssnippet/qsim) for
    high-performance simulation
*   Interoperability with [NumPy](https://numpy.org) and
    [SciPy](https://scipy.org)
*   Cross-platform compatibility

## Installation

Qubitron supports Python version 3.11 and later, and can be used on Linux, MacOS,
and Windows, as well as [Google Colab](https://colab.google). For complete
installation instructions, please refer to the
[Install](https://quantumai.google/qubitron/start/install) section of the online
Qubitron documentation.

## Quick Start – “Hello Qubit” Example

Here is a simple example to get you up and running with Qubitron after you have
installed it. Start a Python interpreter, and then type the following:

```python
import qubitron

# Pick a qubit.
qubit = qubitron.GridQubit(0, 0)

# Create a circuit.
circuit = qubitron.Circuit(
    qubitron.X(qubit)**0.5,  # Square root of NOT.
    qubitron.measure(qubit, key='m')  # Measurement.
)
print("Circuit:")
print(circuit)

# Simulate the circuit several times.
simulator = qubitron.Simulator()
result = simulator.run(circuit, repetitions=20)
print("Results:")
print(result)
```

Python should then print output similar to this:

```text
Circuit:
(0, 0): ───X^0.5───M('m')───
Results:
m=11000111111011001000
```

Congratulations! You have run your first quantum simulation in Qubitron. You can
continue to learn more by exploring the [many Qubitron tutorials](#tutorials)
described below.

## Qubitron Documentation

The primary documentation site for Qubitron is the [Qubitron home page on the Quantum
AI website](https://quantumai.google/qubitron). There and elsewhere, a variety of
documentation for Qubitron is available.

### Tutorials

*   [Video tutorials] on YouTube are an engaging way to learn Qubitron.
*   [Jupyter notebook-based tutorials] let you learn Qubitron from your browser – no
    installation needed.
*   [Text-based tutorials] on the Qubitron home page are great when combined with a
    local [installation] of Qubitron on your computer. After starting with the
    [basics], you'll be ready to dive into tutorials on circuit building and
    circuit simulation under the [Build] and [Simulate] tabs, respectively. Check
    out the other tabs for more!

[Video tutorials]: https://www.youtube.com/playlist?list=PLpO2pyKisOjLVt_tDJ2K6ZTapZtHXPLB4
[Jupyter notebook-based tutorials]: https://colab.research.google.com/github/amyssnippet/Qubitron
[Text-based tutorials]: https://quantumai.google/qubitron
[installation]: https://quantumai.google/qubitron/start/install
[basics]: https://quantumai.google/qubitron/start/basics
[Build]: https://quantumai.google/qubitron/build
[Simulate]: https://quantumai.google/qubitron/simula

### Reference Documentation

*   Docs for the [current stable release] correspond to what you get with
    `pip install qubitron`.
*   Docs for the [pre-release] correspond to what you get with
    `pip install --upgrade qubitron~=1.0.dev`.

[current stable release]: https://quantumai.google/reference/python/qubitron/all_symbols
[pre-release]: https://quantumai.google/reference/python/qubitron/all_symbols?version=nightly

### Examples

*   The [examples subdirectory](./examples/) of the Qubitron GitHub repo has many
    programs illustrating the application of Qubitron to everything from common
    textbook algorithms to more advanced methods.
*   The [Experiments page](https://quantumai.google/qubitron/experiments/) on the
    Qubitron documentation site has yet more examples, from simple to advanced.

### Change log

*   The [Qubitron releases](https://github.com/amyssnippet/qubitron/releases) page on
    GitHub lists the changes in each release.

## Integrations

Google Quantum AI has a suite of open-source software that lets you do more
with Qubitron. From high-performance simulators, to novel tools for expressing and
analyzing fault-tolerant quantum algorithms, our software stack lets you
develop quantum programs for a variety of applications.

<div align="center">

| Your interests                                  | Software to explore  |
|-------------------------------------------------|----------------------|
| Quantum algorithms?<br>Fault-tolerant quantum computing (FTQC)? | [Qualtran] |
| Large circuits and/or a lot of simulations?     | [qsim] |
| Circuits with thousands of qubits and millions of Clifford operations? | [Stim] |
| Quantum error correction (QEC)?                 | [Stim] |
| Chemistry and/or material science?              | [OpenFermion]<br>[OpenFermion-FQE]<br>[OpenFermion-PySCF]<br>[OpenFermion-Psi4] |
| Quantum machine learning (QML)?                 | [TensorFlow Quantum] |
| Real experiments using Qubitron?                    | [ReQubitron] |

</div>

[Qualtran]: https://github.com/amyssnippet/qualtran
[qsim]: https://github.com/amyssnippet/qsim
[Stim]: https://github.com/amyssnippet/stim
[OpenFermion]: https://github.com/amyssnippet/openfermion
[OpenFermion-FQE]: https://github.com/amyssnippet/OpenFermion-FQE
[OpenFermion-PySCF]: https://github.com/amyssnippet/OpenFermion-PySCF
[OpenFermion-Psi4]: https://github.com/amyssnippet/OpenFermion-Psi4
[TensorFlow Quantum]: https://github.com/tensorflow/quantum
[ReQubitron]: https://github.com/amyssnippet/ReQubitron

## Community

<a href="https://github.com/amyssnippet/Qubitron/graphs/contributors"><img
width="150em" alt="Total number of contributors to Qubitron"
src="https://img.shields.io/github/contributors/amyssnippet/qubitron?label=Contributors&logo=github&color=ccc&style=flat-square"/></a>

Qubitron has benefited from [contributions] by over 200 people and
counting. We are dedicated to cultivating an open and inclusive community to
build software for quantum computers, and have a community [code of conduct].

[contributions]: https://github.com/amyssnippet/Qubitron/graphs/contributors
[code of conduct]: https://github.com/amyssnippet/qubitron/blob/main/CODE_OF_CONDUCT.md

### Announcements

Stay on top of Qubitron developments using the approach that best suits your needs:

*   For releases and major announcements: sign up to the low-volume mailing list
    [`qubitron-announce`].
*   For releases only:
    *   Via GitHub notifications: configure [repository notifications] for Qubitron.
    *   Via Atom/RSS from GitHub: subscribe to the GitHub [Qubitron releases Atom feed].
    *   Via RSS from PyPI: subscribe to the [PyPI releases RSS feed] for Qubitron.

Qubitron releases take place approximately every quarter.

[`qubitron-announce`]: https://groups.google.com/forum/#!forum/qubitron-announce
[repository notifications]: https://docs.github.com/github/managing-subscriptions-and-notifications-on-github/configuring-notifications
[Qubitron releases Atom feed]: https://github.com/amyssnippet/Qubitron/releases.atom
[PyPI releases RSS feed]: https://pypi.org/rss/project/qubitron/releases.xml

### Questions and Discussions

*   Have questions about Qubitron? Post them to the [Quantum Computing
    Stack Exchange] and tag them with [`qubitron`]. You can also search past
    questions using that tag – it's a great way to learn!
*   Want meet other Qubitron developers and participate in discussions? Join
    _Qubitron Cynq_, our biweekly virtual meeting of contributors. Sign up
    to [_qubitron-dev_] to get an automatic meeting invitation!

[Quantum Computing Stack Exchange]: https://quantumcomputing.stackexchange.com
[`qubitron`]: https://quantumcomputing.stackexchange.com/questions/tagged/qubitron
[_qubitron-dev_]: https://groups.google.com/forum/#!forum/qubitron-dev

### Contributions

*   Have a feature request or bug report? [Open an issue on GitHub]!
*   Want to develop Qubitron code? Look at the [list of good first issues] to
    tackle, read our [contribution guidelines], and then start opening
    [pull requests]!

[Open an issue on GitHub]: https://github.com/amyssnippet/Qubitron/issues/new/choose
[list of good first issues]: https://github.com/amyssnippet/Qubitron/contribute
[contribution guidelines]: https://github.com/amyssnippet/qubitron/blob/main/CONTRIBUTING.md
[pull requests]: https://help.github.com/articles/about-pull-requests

## Citing Qubitron<a name="how-to-cite-qubitron"></a><a name="how-to-cite"></a>

When publishing articles or otherwise writing about Qubitron, please cite the Qubitron
version you use – it will help others reproduce your results. We use Zenodo to
preserve releases. The following links let you download the bibliographic
record for the latest stable release of Qubitron in some popular formats:

<div align="center">

[![Download BibTeX bibliography record for latest Qubitron
release](https://img.shields.io/badge/Download%20record-e0e0e0.svg?style=flat-square&logo=LaTeX&label=BibTeX&labelColor=106f6e)](https://citation.doi.org/format?doi=10.5281/zenodo.4062499&style=bibtex)&nbsp;&nbsp;
[![Download CSL JSON bibliography record for latest Qubitron
release](https://img.shields.io/badge/Download%20record-e0e0e0.svg?style=flat-square&label=CSL&labelColor=2d98e0&logo=json)](https://citation.doi.org/metadata?doi=10.5281/zenodo.4062499)

</div>

For formatted citations and records in other formats, as well as records for
all releases of Qubitron past and present, please visit the [Qubitron page on
Zenodo](https://doi.org/10.5281/zenodo.4062499).

## Contact

For any questions or concerns not addressed here, please email
quantum-oss-maintainers@google.com.

## Disclaimer

This is not an officially supported Google product. This project is not
eligible for the [Google Open Source Software Vulnerability Rewards
Program](https://bughunters.google.com/open-source-security).

Copyright 2019 The Qubitron Developers.

<div align="center">
  <a href="https://quantumai.google">
    <img width="15%" alt="Google Quantum AI"
         src="https://raw.githubusercontent.com/amyssnippet/Qubitron/refs/heads/main/docs/images/quantum-ai-vertical.svg">
  </a>
</div>
