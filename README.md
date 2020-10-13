# SublimeTrimmer
 SublimeText3 Plugin for formatting long lines in Python code.
 
# Example
If there is such a line in some code, which is longer than 80 symbols required by PEP8:
```python
    print(*fill(null_square(size), list(itertools.chain(*[x.variants(size) for x in polis])), size), sep='\n')
```
this plugin will format it like this:
```python
    print(
        *fill(
            null_square(size),
            list(itertools.chain(*[x.variants(size) for x in polis])),
            size
        ),
        sep='\n'
    )
```

# Installation
 In Sublime Text go to Preferences -> Browse Packeges, create a directory and copy there files sublime_trimmer.py, utils.py and Default.sublime-keymap.

# Usage
 Put cursor on a line that is too long and press "ctrl-shift-l" (you can change hotkey by editing file Default.sublime-keymap)
 
