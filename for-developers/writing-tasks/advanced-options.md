# Advanced options

There are additional class options and functions you can specify in the task definition class, based on which runner is used.

***

## `Command` runner

* `shell` (`bool`, `default: False`): Run `subprocess.Popen` with `shell=True` (**dangerous !**).
* `cwd` (`str`, `default: None`): Command current working directory.
* `encoding` (`dict`, `default: utf-8`): Output encoding.
* `opt_prefix` (`str`, `default: -`): Change the prefix used to specify command options.
* `version_flag` (`str`, `default: None`): The version flag. Defaults to `{opt_prefix}version`.
* `ignore_return_code` (`bool`, `default: False`): Ignore the command return code (useful if your command has non-standard return codes).

***
