v3.1.2 (04/04/2015)

* Add user friendly error messages for invalid options.
* Strip invalid options in astylerc.

v3.1.1 (02/28/2015)

* Hot-Fix for mysterious ValueError(), introduced in v3.1.0.

v3.1.0 (02/28/2015)

* The following default options were changed, according to *Artistic Style* defaults:
    * `indent-preproc-define`: `true` -> `false`
    * `indent-col1-comments`: `true` -> `false`
    * `align-pointer`: `"name"` -> "not set" (Use *Artistic Style* defaults, which is "no change")
    * `align-reference`: `"name"` -> "not set" (Use *Artistic Style* defaults, which is "same as `align-pointer`")
    * `keep-one-line-blocks`: `false` -> `true`
* Now an output panel with user-friendly error message will show if anything goes wrong.
* Remove `convert-tabs` option, because it's duplicated with Sublime Text's `translate_tabs_to_spaces` setting.
* Fix a NoneType error while formatting unsaved files.

v3.0.0 (02/20/2015)

* Upgrade astyle binary to v2.05.1.
* Improper configuration settings will raise errors now.
* Fix missing "google" style option.
* Remove "ansi" style option because it's deprecated in astyle v2.05.
* Remove "indent-preprocessor" option because it was deprecated in astyle v2.04.
* Add "indent-preproc-block" option (introduced in astyle v2.05).
* Add more expanded variables for reaching astylerc file (see `SublimeAStyleFormatter.sublime-settings` for more details, in `additional_options_file`).

v2.1.0 (04/23/2014)

* Upgrade astyle binary to v2.04.
* Fix unfunctional `user_defined_syntax_mode_mapping` option.
* Fix wrong user keymap setting file location.

v2.0.5 (11/28/2013)

* Fix plugin stop working while `additional_options` missing from user options.
* Add `apex` syntax support.
* Add new option: `user_defined_syntax_mode_mapping`.

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
