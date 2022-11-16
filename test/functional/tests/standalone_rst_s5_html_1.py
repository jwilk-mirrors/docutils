# Source and destination file names:
test_source = 'standalone_rst_s5_html.txt'
test_destination = 'standalone_rst_s5_html_1.html'

# Keyword parameters passed to publish_file:
writer_name = 's5_html'
settings_overrides = {
    'sectsubtitle_xform': True,
    'theme': 'small-black',
    # local copy of default stylesheet:
    'stylesheet_path': 'functional/input/data/html4css1.css',
    }
