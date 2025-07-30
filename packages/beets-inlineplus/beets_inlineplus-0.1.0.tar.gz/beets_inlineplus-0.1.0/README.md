# InlinePlus plugin for Beets

This [beets] plugin is like the builtin [`inline`][inline] plugin: it "lets you
use Python to customize your path formats. Using it, you can define template
fields in your beets configuration file and refer to them from your template
strings in the `paths: ` section."

However, `inlineplus` adds a `fields_base:` block where you can define python
functions you want to use in multiple template fields.

### Installation

Install the plugin into beets' Python environment with

    pip install beets-inlineplus

(or the respective equivalent if you use e.g. pipx).

### Usage

Add the `inlineplus` plugin to your config. 

Then under a new `fields_base:` block write python functions and constants you want to use in your fielddefinition under `item_fields:` or `album_fields:`. Python function can be used in both of these section. Example:

You want to use a function `anartist()` both in the item field `myiteminfo` and in the album fields `myartistinfo`. Define this function in your `config.yaml` like this:

```
fields_base: |
  def anartist():
    return "AnArtist"
```

Then you can refer to it the item and album fields for example liek this:

```
item_fields:
  myiteminfo: anartist()

album_fields:
  myartistinfo: |
    return "Artist_" + anartist().upper()
```

and then in the `paths` section you can use your new fields:

```
paths:
    default: $albumartist/$album%aunique{}/$track $title $myiteminfo
    singelton: $myartistinfo/$title
```


  [beets]: https://beets.io
  [inline]: https://beets.readthedocs.io/en/stable/plugins/inline.html
