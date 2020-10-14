import sublime
import sublime_plugin

from .utils import *


class TrimLineCommand(sublime_plugin.TextCommand):
    ''' Trim and format line '''
    def run(self, edit):

        pos = self.view.sel()[0].begin()
        lines = self.view.lines(self.view.sel()[0])
        region = sublime.Region(lines[0].begin(), lines[-1].end())
        document = self.view.substr(sublime.Region(0, self.view.size()))
        for start, end in find_docstrings(document):
            if start <= pos <= end:
                ds_reg = sublime.Region(start, end)
                new_doc = trim_docstring(self.view.substr(ds_reg))
                self.view.replace(edit, ds_reg, new_doc)
                break
        else:
            self.view.replace(
                edit,
                region,
                '\n'.join(trim_line(self.view.substr(line)) for line in lines)
            )
