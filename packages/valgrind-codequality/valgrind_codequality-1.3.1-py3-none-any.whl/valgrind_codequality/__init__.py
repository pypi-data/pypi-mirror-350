# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""Convert Valgrind XML to Code Quality JSON

Valgrind is a useful tool detect memory leak in C/C++ code.
Developer tools, such as GitLab, can display useful insights about code quality,
when given a JSON report file defined by Code Quality's GitLab.

This tool convert Valgrind XML report to Code Quality JSON.

Example:
    # Generate valgrind report as XML
    valgrind --tool=memcheck --show-leak-kinds=all --track-origins=yes --verbose --xml=yes --xml-file=valgrind_out.xml your_exe
    # Convert to a Code Climate JSON report
    valgrind-codequality --input-file valgrind_out.xml --output-file valgrind.json

References:
  - https://valgrind.org/
  - https://docs.gitlab.com/ee/user/project/merge_requests/code_quality.html#implementing-a-custom-tool

SPDX-License-Identifier: MIT
"""

import hashlib
import json
import logging
import os
import typing
from copy import deepcopy

# third-party
import xmltodict

__version__ = "1.3.1"

log = logging.getLogger(__name__)

# Source: https://github.com/codeclimate/platform/blob/master/spec/analyzers/SPEC.md#data-types
CODE_QUAL_ELEMENT = {
    "severity": "",
    "description": "",
    "fingerprint": "",
    "location": {"path": "", "lines": {"begin": -1}},
}


def _get_codeclimate_severity(valgrind_severity: str) -> str:
    """Get Code Climate severity, from valgrind severity string.

    CodeQuality: info, minor, major, critical, blocker
    """
    severity = ""
    if "Leak_DefinitelyLost" == valgrind_severity:
        severity = "blocker"
    else:
        if valgrind_severity in [
            "UninitCondition",
            "UninitValue",
            "ClientCheck",
            "Overlap",
            "Leak_StillReachable",
        ]:
            severity = "minor"
        elif valgrind_severity in [
            "SyscallParam",
            "InvalidFree",
            "MismatchedFree",
            "InvalidJump",
            "InvalidMemPool",
            "Leak_PossiblyLost",
        ]:
            severity = "major"
        elif valgrind_severity in [
            "InvalidRead",
            "InvalidWrite",
            "Leak_IndirectlyLost",
        ]:
            severity = "critical"
        else:
            severity = "info"

    return severity


def convert_file(
    fname_in: str,
    fname_out: str,
    base_dirs: typing.List[str],
    file_concat: typing.Optional[str] = None,
    relative_dir: typing.Optional[str] = None,
    exclude_list: typing.Optional[typing.List[str]] = None,
) -> int:
    """Convert valgrind XML file to GitLab-compatible "Code Quality" JSON report.

    Args:
        fname_in (str):
          Input file path (valgrind XML). Like 'valgrind.xml'.
        fname_out (str):
          Output file path (code quality JSON). Like 'valgrind.json'.
        base_dirs (list):
          Base directories where source files with relative paths can be found.
        file_concat (str):
          File path (JSON) contains code quality informations from previous analyze.
        relative_dir (str):
          Absolute path to change absolute path to relative from this path.
        exclude_list (list):
          Folders name to exclude leaks from a folder containing these names.

    Returns:
        int: If processing failed, a negative value. If successful, number of
          valgrind issues processed.
    """
    fin = None
    dict_concat = None
    json_out_str = ""
    num_cq_issues_converted = 0

    # Read concat file
    if file_concat:
        file_concat = os.path.abspath(file_concat)
        if not os.path.isfile(file_concat):
            log.error(
                "Concat file (JSON) file does not exist or cannot be opened -- '%s'",
                file_concat,
            )
            return -1
        with open(file_concat, mode="r", encoding="utf-8") as fin_concat:
            dict_concat = json.loads(fin_concat.read())

    # Convert Input
    fname_in = os.path.abspath(fname_in)
    if not os.path.isfile(fname_in):
        log.error(
            "Input (valgrind XML) file does not exist or cannot be opened -- '%s'",
            fname_in,
        )
        return -1

    log.debug("Reading input file: %s", fname_in)
    with open(fname_in, mode="rt", encoding="utf-8", errors="backslashreplace") as fin:
        json_out_str, num_cq_issues_converted = _convert(
            fin.read(),
            base_dirs=base_dirs,
            relative_dir=relative_dir,
            dict_concat=dict_concat,
            exclude_list=exclude_list,
        )

    log.debug("Writing output file: %s", fname_out)
    with open(fname_out, "w", encoding="utf-8") as f_out:
        f_out.write(json_out_str)

    return num_cq_issues_converted


def _get_line_from_file(filename: str, line_number: int) -> str:
    """Return a specific line in a file as a string.

    I've found that linecache.getline() will end up raising a UnicodeDecodeError
    if the source file we're opening has non-UTF-8 characters in it. So, here,
    we're explicitly escaping those bad characters.

    Side note, it seems valgrind v2.0+ will generate a 'syntaxError' for
    "unhandled characters", so you could find these issues with your source code
    more easily.

    Args:
        filename (str):
          Name of file to open and read line from
        line_number (int):
          Number of the line to extract. Line number starts at 1.

    Returns:
        str: Contents of the specified line.
    """
    max_line_cnt = 0
    if line_number <= 0:
        return str(filename) + "<the whole file>"

    filename = os.path.abspath(filename)
    if not os.path.isfile(filename):
        raise FileNotFoundError(
            f"Source code file does not exist or cannot be opened. Missing a base directory?\n--> '{filename}'"
        )

    with open(filename, mode="rt", encoding="utf-8", errors="backslashreplace") as fin:
        for i, line in enumerate(fin):
            if (i + 1) == line_number:
                # log.debug("Extracted line %s:%d", filename, line_number)
                return line
            max_line_cnt += 1

    log.warning(
        "Only %d lines in file. Can't read line %d from '%s'",
        max_line_cnt,
        line_number,
        filename,
    )
    return f"Can't read line {line_number} from a {max_line_cnt} line file"


def _convert(
    xml_input: str,
    base_dirs: typing.List[str],
    relative_dir: typing.Optional[str] = None,
    dict_concat: typing.Optional[typing.Dict[str, str]] = None,
    exclude_list: typing.Optional[typing.List[str]] = None,
) -> typing.Tuple[str, int]:
    """Convert valgrind XML to Code Climate JSON.

    Note:
        There isn't a great 1:1 conversion from valgrind's "severity" level, to
        the Code Climate's "categories." To prevent information loss, the
        original valgrind severity is appended to the category list.

        In the future, maybe this conversion can be made using valgrind's "id"
        or check name.

    Args:
        xml_input (str): Filename of the XML from valgrind
        base_dirs (list):
          Base directories where source files with relative paths can be found.
        relative_dir (str):
          Absolute path to change absolute path to relative from this path.
        dict_concat:
          Dictionnary contains code quality informations from previous analyze.
        exclude_list (list):
          Folders name to exclude leaks from a folder containing these names.

    Returns:
        Tuple, where the first element, a string, is the JSON conversion result
        and the second element, an int, is the number of issues converted.
    """

    dict_in = xmltodict.parse(xml_input=xml_input)
    dict_out = []
    fingerprints = []

    # Add pevious analyze
    if dict_concat:
        dict_out = dict_concat

    # Ensure this XML report has errors to convert
    if len(dict_in) == 0 or not "error" in dict_in["valgrindoutput"]:
        log.warning("No <error> in XML file. Nothing to do.")
        return (json.dumps(dict_out), 0)

    errors = []
    if not isinstance(dict_in["valgrindoutput"]["error"], list):
        errors = [dict_in["valgrindoutput"]["error"]]
    else:
        errors = dict_in["valgrindoutput"]["error"]

    for error in errors:

        log.debug("Processing error -- %s", str(error["unique"]))

        # Some information messages are not related to the code.
        # Let's let the user know, then skip.
        if "stack" not in error:
            log.info("No stack. Skipping the below issue:\n  %s", error["unique"])
            continue

        # Extract frames
        stacks = error["stack"]
        if not type(stacks) is list:
            stacks = [stacks]
        if stacks[0] == None:
            log.info("No frames. Skipping the below issue:\n  %s", error["unique"])
            continue
        (tmp_dict, kind) = _extract_frames(error)

        # Extract error
        (path, line) = _extract_error(stacks, base_dirs, exclude_list)

        # Path found
        if path != "":
            if relative_dir:
                tmp_dict["location"]["path"] = os.path.relpath(path, relative_dir)
            else:
                tmp_dict["location"]["path"] = path
            tmp_dict["location"]["lines"]["begin"] = line

            log.debug("-- File -- %s", path)
            log.debug("-- Line -- %s", line)

            # GitLab requires the fingerprint field. Code Climate describes this as
            # being used to uniquely identify the issue, so users could "exclude it
            # from future analysis."
            #
            # The components of the fingerprint aren't well defined, but Code Climate
            # has some examples here:
            # https://github.com/codeclimate/codeclimate-duplication/blob/1c118a13b28752e82683b40d610e5b1ee8c41471/lib/cc/engine/analyzers/violation.rb#L83
            # https://github.com/codeclimate/codeclimate-phpmd/blob/7d0aa6c652a2cbab23108552d3623e69f2a30282/tests/FingerprintTest.php

            codeline = _get_line_from_file(filename=path, line_number=line).strip()

            fingerprint_str = "valgrind-" + kind + "-" + path + "-" + codeline
            log.debug("Fingerprint string: '%s'", fingerprint_str)
            tmp_dict["fingerprint"] = hashlib.md5(
                (fingerprint_str).encode("utf-8")
            ).hexdigest()

            # Append this record if not already exists
            if not fingerprint_str in fingerprints:
                dict_out.append(deepcopy(tmp_dict))
                fingerprints.append(fingerprint_str)

    if len(dict_out) == 0:
        log.warning("Result is empty")
    return (json.dumps(dict_out, indent=4), len(dict_out))


def _extract_frames(error: dict):
    """Extract frames from error.

    Args:
        error (str): Error where extract frames.

    Returns:
        Tuple, where the firs element, dictionary, with description and severity,
        and the second element, an string, is the kind of error.
    """
    tmp_dict = dict(CODE_QUAL_ELEMENT)
    kind = error["kind"]
    if "xwhat" in error:
        tmp_dict["description"] = error["xwhat"]["text"]
    else:
        tmp_dict["description"] = error["what"]

    tmp_dict["description"] = kind + ": " + tmp_dict["description"]
    tmp_dict["severity"] = _get_codeclimate_severity(kind)

    return (tmp_dict, kind)


def _extract_error(
    stacks: list,
    base_dirs: typing.List[str],
    exclude_list: typing.Optional[typing.List[str]] = None,
):
    """Extract line and file path from error.

    Args:
        error (str): Error where extract line and path.

    Returns:
        Tuple, where the key element, a string, is the path
        and the second element, an string, is the line.
    """
    line = -1
    path = ""
    for index in range(len(stacks[0]["frame"])):
        frame = stacks[0]["frame"][index]
        log.debug("- Analyse frames -- %s", str(frame["ip"]))

        # Check if path in "obj" contains name to exclude
        exclude_error = False
        if exclude_list:
            path_name = ""
            path_analyse = ""
            for path_name in exclude_list:
                if "obj" in frame:
                    path_analyse = frame["obj"]
                    if path_name in path_analyse:
                        exclude_error = True
                if "dir" in frame:
                    path_analyse = frame["dir"]
                    if path_name in path_analyse:
                        exclude_error = True
            if exclude_error:
                log.debug(f"- Exclude because '{path_name}' in {path_analyse}")
                break

        # Get line
        if "dir" in frame and "file" in frame:
            line = int(frame["line"])

            # Check in base dirs
            for d in base_dirs:
                if d in frame["dir"]:
                    path = os.path.join(frame["dir"], frame["file"])
                    break

            if path == "":
                continue
            break
    return (path, line)


if __name__ == "__main__":
    import warnings

    warnings.warn(
        "use 'python3 -m valgrind_codequality', not 'python3 -m valgrind_codequality.__init__'",
        DeprecationWarning,
    )
