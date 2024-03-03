# Advanced options

There are additional class options and functions you can specify in the `Command` objects to customize the command running lifecycle and output format:

* `opts` (`dict`, `default: {}`): Command options.
* `shell` (`bool`, `default: False`): Run `subprocess.Popen` with `shell=True` (dangerous).
* `cwd` (`str`, `default: None`): Command current working directory.
* `encoding` (`dict`, `default: utf-8`): Output encoding.
* `json_output` (`bool`, `default: True`): Support JSON output.
* `def on_item_pre_convert(self, item)`: Callback to modify item with original schema. Must return the item.
* `def on_item(self, item)`: Callback to modify item after schema conversion. <mark style="color:red;">**MUST**</mark> return the item.
* `def on_line(self, line)`: Callback to modify line. <mark style="color:red;">**MUST**</mark> return the line.
* `def on_start(self)`: Callback to do something before the command has started running.
* `def on_end(self)`: Callback to do something after the command has finished running.
* `def keep_item(self, item)`: <mark style="color:red;">**MUST**</mark> return True if item needs to be kept (yielded), or False if item can be skipped.
* `def item_loader(self, line)`: Load a line as dictionary. <mark style="color:red;">**MUST**</mark> return a dict.
