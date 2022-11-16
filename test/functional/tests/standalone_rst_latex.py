# Source and destination file names
test_source = "standalone_rst_latex.txt"
test_destination = "standalone_rst_latex.tex"

# Keyword parameters passed to publish_file()
writer_name = "latex"
settings_overrides = {
    'sectsubtitle_xform': True,
    # use "smartquotes" transition:
    'smart_quotes': True,
    'legacy_column_widths': True,
    'use_latex_citations': False,
    }
