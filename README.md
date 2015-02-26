Sublime Text 2 & 3 AStyle Formatter Plugin
==========================================

[![Travis-CI Build Status](https://travis-ci.org/timonwong/SublimeAStyleFormatter.svg?branch=master)](https://travis-ci.org/timonwong/SublimeAStyleFormatter)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/timonwong/SublimeAStyleFormatter?branch=master&svg=true)](https://ci.appveyor.com/project/timonwong/SublimeAStyleFormatter)

Description
-----------

SublimeAStyleFormatter is a simple code formatter plugin for Sublime Text.
It provides ability to format C, C++, Cuda-C++, OpenCL, Arduino, C#, and Java files.

**NOTE**: Syntax files required to be installed separately for Cuda-C++ and OpenCL.

### Donation

If you find my work useful, please consider buying me a cup of coffee, all
donations are much appreciated :)

[![Donate via PayPal](http://dl.dropbox.com/u/2451120/donate-with-paypal.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=GGVE2BPUP7KEC)

Installation
------------

### With the Package Control plugin

The easiest way to install SublimeAStyleFormatter is through [Package Control].

[Package Control]: http://wbond.net/sublime_packages/package_control

Once you have Package Control installed, restart Sublime Text.

1. Bring up the Command Palette (<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>
on Windows and Linux. <kbd>⌘</kbd>+<kbd>⇧</kbd>+<kbd>P</kbd> on OS X).
2. Type "Install" and select "Package Control: Install Package".
3. Select "SublimeAStyleFormatter" from list.

The advantage of using Package Control is that it will keep SublimeAStyleFormatter up to date.

### Manual Install

**Without Git:**

[Download](https://github.com/timonwong/SublimeAStyleFormatter) the latest source code,
and extract it to the Packages directory.

**With Git:**

Type the following command in your Sublime Text 2 or Sublime Text 3 Packages directory:

`git clone git://github.com/timonwong/SublimeAStyleFormatter.git`

The "Packages" directory is located at:

**Sublime Text 2**

* **Windows**: `%APPDATA%\Sublime Text 2\Packages`
* **Linux**: `~/.config/sublime-text-2/Packages/`
* **OS X**: `~/Library/Application Support/Sublime Text 2/Packages/`

**Sublime Text 3**

* **Windows**: `%APPDATA%\Sublime Text 3\Packages`
* **Linux**: `~/.config/sublime-text-3/Packages/`
* **OS X**: `~/Library/Application Support/Sublime Text 3/Packages/`

Usage
-----

### Key Bindings

The default key bindings for this plugin:

**Windows, Linux:**

* <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd>: Format current file.
* <kbd>Ctrl</kbd>+<kbd>K</kbd>, <kbd>Ctrl</kbd>+<kbd>F</kbd>: Format current selection.

**OSX:**

* <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd>: Format current file.
* <kbd>⌘</kbd>+<kbd>K</kbd>, <kbd>⌘</kbd>+<kbd>F</kbd>: Format current selection.

### Command Palette

Open the command palette, it appears as `SublimeAStyleFormatter: Format Current File` and
`SublimeAStyleFormatter Format Current Selection`.

Settings
--------

### Per-project Settings

Before starting, you may want to have a look at SublimeAStyleFormatter.sublime-settings.

To edit your project setting, select `Project/Edit Project` from main menu. A project setting contains
per-project settings for SublimeAStyleFormatter should look like this:

```javascript
{
    "settings":
    {
        "AStyleFormatter":
        {
        }
    }
}
```

For example, if you don't want to inherit the default settings, instead, use your own astylerc file for
C and C++ individually, then your project setting might look like this:

```javascript
{
    // project folders, etc
    // ...
    // project settings
    "settings":
    {
        "AStyleFormatter":
        {
            "options_default":
            {
                // Use 2 spaces for indentation
                "indent": "spaces",
                "indent-spaces": 2
            },
            "options_c":
            {
                "use_only_additional_options": true,
                "additional_options_file": "/path/to/your/astylerc/for/c"
            },
            "options_c++":
            {
                "use_only_additional_options": true,
                "additional_options_file": "/path/to/your/astylerc/for/c++"
            }
        }
    }
}
```


What's New
-------------

[CHANGELOG.md](./CHANGELOG.md)


License
------

This plugin is using MIT License:

    Copyright (c) 2012-2015 Timon Wong

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Credits
-------

**[Artistic Style]** - A Free, Fast and Small Automatic Formatter for C, C++, C#,
and Java Source Code.

Licensed under [GNU Lesser General Public License version 3.0]

[Artistic Style]: http://sourceforge.net/projects/astyle/
[GNU Lesser General Public License version 3.0]: http://astyle.sourceforge.net/license.html

Donors
------

[DONORS.md](./DONORS.md)
