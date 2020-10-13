import sublime
import sublime_plugin

from .utils import trim_line


class TrimLineCommand(sublime_plugin.TextCommand):
    ''' Trim and format line '''
    def run(self, edit):

        pos = self.view.sel()[0].begin()
        lines = self.view.lines(self.view.sel()[0])
        region = sublime.Region(lines[0].begin(), lines[-1].end())

        result = '\n'.join(trim_line(self.view.substr(line)) for line in lines)

        self.view.replace(
            edit,
            region,
            str(result)
        )
