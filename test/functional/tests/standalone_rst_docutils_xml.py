# Source and destination file names
test_source = "standalone_rst_docutils_xml.txt"
test_destination = "standalone_rst_docutils_xml.xml"

# Keyword parameters passed to publish_file()
writer_name = "docutils_xml"
settings_overrides = {
    'sectsubtitle_xform': True,
    # enable INFO-level system messages in this test:
    'report_level': 1,
    # format output with indents and newlines
    'indents': True,
    }
