import sublime
import sublime_plugin

from .utils import trim_line


class TrimLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        pos = self.view.sel()[0].begin()
        lines = self.view.lines(self.view.sel()[0])

        for line in lines:
            self.view.replace(
                edit,
                line,
                str(trim_line(self.view.substr(line)))
            )
