# Changelog

## 1.9.0

* [GH-13](https://github.com/Digiratory/StatTools/issues/13) fix: posible unbalances tuple unpacking from method dpcca.
* [GH-13](https://github.com/Digiratory/StatTools/issues/13) docs: update documentation for dpcca method.
* [GH-13](https://github.com/Digiratory/StatTools/issues/13) refactor: update code for dpcca method to improve performance and readability.
* [GH-18](https://github.com/Digiratory/StatTools/issues/18) feat: Enhanced Kalman filter with auto calculation of transition matrix and measurement covariance matrix based on Kasdin model.
* [GH-18](https://github.com/Digiratory/StatTools/issues/18) fix: Add normalization to the Kasdin generator.

## 1.8.0

* [GH-9](https://github.com/Digiratory/StatTools/issues/9) repo: setup pre-commit hooks.
* [GH-12](https://github.com/Digiratory/StatTools/issues/12) docs: fix format violation in CHANGELOG.md.
* [GH-15](https://github.com/Digiratory/StatTools/issues/15) feat&fix: LBFBm generator update: generate with input value and return an increment instead of the absolute value of the signal.
* [GH-23](https://github.com/Digiratory/StatTools/issues/23) feat: add Kasdin generator. fix: change first arg in lfilter in LBFBm generator.
* [GH-25](https://github.com/Digiratory/StatTools/issues/25) feat: Detrended Fluctuation Analysis (DFA) for a nonequidistant dataset.
* [GH-28](https://github.com/Digiratory/StatTools/issues/28) repo: Exclude Jupyter Notebooks from GitHub Programming Language Stats.

## 1.7.0

* [GH-5](https://github.com/Digiratory/StatTools/issues/5) feat: add LBFBm generator, that generates a sequence based on the Hurst exponent.
* [PR-8](https://github.com/Digiratory/StatTools/pull/8) refactor: rework filter-based generator.
* [PR-8](https://github.com/Digiratory/StatTools/pull/8) tests: add new tests for DFA and generators.
* [GH-10](https://github.com/Digiratory/StatTools/issues/10) build: enable wheel building with setuptools-scm.
* [GH-10](https://github.com/Digiratory/StatTools/issues/10) doc: enchance pyproject.toml with urls for repository, issues, and changelog.

## 1.6.1

* [PR-3](https://github.com/Digiratory/StatTools/pull/3) feat: add conventional FA

## 1.6.0

* [GH-1](https://github.com/Digiratory/StatTools/issues/1) Add argument `n_integral=1` in `StatTools.analysis.dpcca.dpcca` to provide possibility to control integretion in the beggining of the dpcca(dfa) analysis pipeline.
* fix: failure is processes == 1 and 1d array
* fix: remove normalization from dpcca processing

## 1.0.1 - 1.0.9

* Minor updates

## 1.1.0

* Added C-compiled modules
