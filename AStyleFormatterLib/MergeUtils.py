# borrowed from GoSublime
import sublime
from diff_match_patch.diff_match_patch import diff_match_patch


class MergeException(Exception):
    pass


def _merge_code(view, edit, code, formatted):
    def ss(start, end):
        return view.substr(sublime.Region(start, end))

    dmp = diff_match_patch()
    diffs = dmp.diff_main(code, formatted)
    dmp.diff_cleanupEfficiency(diffs)
    i = 0
    dirty = False
    for k, s in diffs:
        l = len(s)
        if k == 0:
            # match
            l = len(s)
            if ss(i, i + l) != s:
                raise MergeException('mismatch', dirty)
            i += l
        else:
            dirty = True
            if k > 0:
                # insert
                view.insert(edit, i, s)
                i += l
            else:
                # delete
                if ss(i, i + l) != s:
                    raise MergeException('mismatch', dirty)
                view.erase(edit, sublime.Region(i, i + l))
    return dirty


def merge_code(view, edit, code, formatted_code):
    vs = view.settings()
    ttts = vs.get("translate_tabs_to_spaces")
    vs.set("translate_tabs_to_spaces", False)
    if not code.strip():
        return (False, '')

    dirty = False
    err = ''
    try:
        dirty = _merge_code(view, edit, code, formatted_code)
    except MergeException as (err, d):
        dirty = True
        err = "Could not merge changes into the buffer, edit aborted: %s" % err
        view.replace(edit, sublime.Region(0, view.size()), code)
    except Exception as ex:
        err = "Unknown exception: %s" % ex
    finally:
        vs.set("translate_tabs_to_spaces", ttts)
        return (dirty, err)
