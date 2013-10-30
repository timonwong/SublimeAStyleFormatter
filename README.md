Sublime Text 2 & 3 AStyle Formatter Plugin
==========================================

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

Open the command palette, it apperas as `SublimeAStyleFormatter: Format Current File` and
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

v2.0.4 (10/30/2013)

* Fix OSX and Linux pyastyle binaries.

v2.0.3 (10/28/2013)

* Add Arduino files support.

v2.0.2 (07/19/2013)

* Less error-prone default options overriding (You don't need to duplicate whole
  `options_defaut` section before customizing now, default options in `options_defaut`
  section will be retrieved automatically).

v2.0.1 (06/26/2013)

* Rebuild pyastyle libraries for linux amd64 in order to resolve libc/libc++ compatibility issues.

v2.0.0 (06/22/2013)

* Update Artistic Style to v2.03 release ([News](http://astyle.sourceforge.net/news.html)
  and [Release Notes](http://astyle.sourceforge.net/notes.html)).
* Please note that deprecated bracket options are now removed from astyle v2.03, use
  `style` options instead if you have any those deprecated options (usually in your `astylerc` files).
* Add new options: `pad-first-paren-out`, `close-templates`, `max-code-length` and `break-after-logical`.

v1.9.4 (04/16/2013)

* Add OpenCL and Cuda-C++ (each requires its syntax file installed) support.

v1.9.3 (03/24/2013)

* Can be now installed from Package Control (latest) for Sublime Text 3.

v1.9.2 (03/16/2013)

* Add OS X support for Sublime Text 3.

v1.9.1 (03/10/2013)

* Add Linux support (Both x86 and x86_64) for Sublime Text 3.

v1.9 (03/08/2013)

* Preliminary support for Sublime Text 3 (Now only Windows x86 and Windows x86_64).

v1.8 (12/24/2012)

* Add auto format on file save (through option `autoformat_on_save`).
* Add context and side bar commands.

v1.7.3 (12/18/2012)

* Fix a conflict with SublimeCodeIntel.

v1.7.1 (11/22/2012)

* Change default keybinding for OSX (was conflict with "replace" in Sublime Text 2).

v1.7 (11/10/2012)

* Buffer will not scroll up and down during formatting now.

v1.6.2 (11/5/2012)

* Rebuild pyastyle x86_64 binary which should work on older version of linux distros.

v1.6.1 (10/20/2012)

* Fix ascii decoder error if source contains non-ascii characters.

v1.6 (10/19/2012)

* Remove dependency for ctypes.

v1.5 (10/16/2012)

* Update AStyle binrary of OSX.
* Add meaningful prompt dialog while ctypes module cannot be imported in Linux.

v1.4.1 (10/6/2012)

* Fix wrong AStyle.dll for 32bit Windows.

v1.4 (9/28/2012)

* Add linux binaries (ctypes should be installed manually in order to get it work).
* Fix default key binding conflicts with JsFormat (ctrl+alt+f).
* Windows and Linux astyle libraries are now v2.0.3 beta.

v1.3 (9/21/2012)

* Added support for formatting selection text only.
* Restore to previous viewport after formatting entire file.

v1.2 (4/19/2012)

* Added support for per-project settings.
* Fixed a bug that "additional_options" is invalid when "use_only_additional_options " is not "true".
* Fixed a bug which will throw python 'KeyError' exception while options in "options_default" are lesser than expected.

v1.1 (2/5/2012)

* Added support for OS X.
* More comprehensive options.

License
------

This plugin is using MIT License:

    Copyright (c) 2012 Timon Wong

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
