# valgrind-codequality

[![badge-pypi](https://img.shields.io/pypi/v/valgrind-codequality.svg?logo=pypi)](https://pypi.python.org/pypi/valgrind-codequality/)
&nbsp;
[![badge-pypi-downloads](https://img.shields.io/pypi/dm/valgrind-codequality)](https://pypi.org/project/valgrind-codequality/)


[![badge-pipeline](https://gitlab.com/echopouet/valgrind-codequality/badges/main/pipeline.svg)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)
&nbsp;
[![badge-coverage](https://gitlab.com/echopouet/valgrind-codequality/badges/main/coverage.svg)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)
&nbsp;
[![badge-pylint](https://gitlab.com/echopouet/valgrind-codequality/-/jobs/artifacts/main/raw/badge.svg?job=pylint)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)
&nbsp;
[![badge-formatting](https://gitlab.com/echopouet/valgrind-codequality/-/jobs/artifacts/main/raw/badge.svg?job=format_black)](https://gitlab.com/echopouet/valgrind-codequality/-/pipelines?scope=branches)
&nbsp;
[![badge-issues-cnt](https://img.shields.io/badge/dynamic/json?label=issues&query=statistics.counts.opened&url=https%3A%2F%2Fgitlab.com%2Fapi%2Fv4%2Fprojects%2F19114200%2Fissues_statistics%3Fscope%3Dall)](https://gitlab.com/echopouet/valgrind-codequality/-/issues)


## About

I wanted reports from [Valgrind](https://valgrind.org/) to appear in GitLab Merge Requests as [Code Quality reports](https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html#implementing-a-custom-tool), which is a JSON file defined by the Code Quality's GitLab.

That's all this does: convert Valgrind XML report to Code Quality JSON.

Contributions are welcome.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/EchoPouet)

### Usage

It is primarily used as a console script. As such, ensure you have Python 3's "scripts" directory in your `PATH` variable.
For example, on Linux, that might be `$HOME/.local/bin`.

To test, try the `--help` or `--version` flags:
```bash
valgrind-codequality --help
```

This script follows that example and provides similar command-line options.
A typical workflow might look like this:

```bash
# Generate valgrind report as XML
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --xml=yes --xml-file=valgrind_out.xml your_exe
# Convert to a Code Climate JSON report
valgrind-codequality --input-file valgrind_out.xml --output-file valgrind.json
```

If you wanted, you could invoke the script directly as a module, like this:

```bash
# Run as a module instead (note the underscore in the module name here)
python -m valgrind_codequality --input-file=valgrind_out.xml --output-file=valgrind.json
```

Now, in your GitLab CI script, [upload this file](https://docs.gitlab.com/ee/ci/pipelines/job_artifacts.html#artifactsreportscodequality)
as a Code Quality report.

```yaml
my-code-quality:
  script:
    - [...]
  artifacts:
    reports:
      codequality: valgrind.json
```

### Contributing

* Format with [black](https://pypi.org/project/black/)
* Check with [pylint](https://pypi.org/project/pylint/)

### Credits & Trademarks

valgrind is an open-source project with a GPL v3.0 license.
* https://valgrind.org/

"GitLab" is a trademark of GitLab B.V.
* https://gitlab.com
* https://docs.gitlab.com/ci/testing/code_quality/#import-code-quality-results-from-a-cicd-job

All other trademarks belong to their respective owners.
