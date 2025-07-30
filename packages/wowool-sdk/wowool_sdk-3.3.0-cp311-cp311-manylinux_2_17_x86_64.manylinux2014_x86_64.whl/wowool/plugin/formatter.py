from wowool.package.lib.wowool_plugin import match_info


def format(ud):

    ignore_uris = set(["Sentence", "CAPTURE", "::python::eot_finder::concept_print"])
    match = match_info()
    capture = match.capture()
    if capture.has("format"):
        fvalue = capture.attribute("format")
        rule = match.rule()  # noqa: F841
        this = capture  # noqa: F841
        self = capture  # noqa: F841
        resolved_value = eval('f"' + fvalue + '"')
        print(resolved_value)
    else:
        from io import StringIO

        std_output = StringIO()
        for concept in capture.find("/.*/"):
            uri = concept.uri()
            if uri not in ignore_uris:
                std_output.write(uri)
                std_output.write(", ")
        std_output.seek(0)
        print(std_output.read())
