# jinja2_fnmatch_extension

[//]: # (automatically generated from https://github.com/metwork-framework/github_organization_management/blob/master/common_files/README.md)

**Status (master branch)**

[![GitHub CI](https://github.com/metwork-framework/jinja2_fnmatch_extension/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/metwork-framework/jinja2_fnmatch_extension/actions?query=workflow%3ACI+branch%3Amaster)
[![Maintenance](https://raw.githubusercontent.com/metwork-framework/resources/master/badges/maintained.svg)](https://github.com/metwork-framework/resources/blob/master/badges/maintained.svg)




## What is it ?

This is a [jinja2](http://jinja.pocoo.org/) extension to expose [fnmatch](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch) function.

## Syntax

The syntax is `|fnmatch(pattern)`.

## Example

```python

from jinja2 import Template, Environment

# We load the extension in a jinja2 Environment
env = Environment(extensions=["jinja2_fnmatch_extension.FnMatchExtension"])

# For the example, we use a template from a simple string
template = env.from_string("{{ 'foo-bar'|fnmatch('foo-*') }}")
result = template.render()

assert result == "True"
# [...]

```






## Contributing guide

See [CONTRIBUTING.md](CONTRIBUTING.md) file.



## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) file.



## Sponsors

*(If you are officially paid to work on MetWork Framework, please contact us to add your company logo here!)*

[![logo](https://raw.githubusercontent.com/metwork-framework/resources/master/sponsors/meteofrance-small.jpeg)](http://www.meteofrance.com)
