try:
    from ._local_arch.pyastyle import *
    platform = "Local arch"
except ImportError:
    try:
        from ._linux_x86_64.pyastyle import *
        platform = "Linux 64 bits"
    except ImportError:
        try:
            from ._linux_x86.pyastyle import *
            platform = "Linux 32 bits"
        except ImportError:
            try:
                from ._win64.pyastyle import *
                platform = "Windows 64 bits"
            except ImportError:
                try:
                    from ._win32.pyastyle import *
                    platform = "Windows 32 bits"
                except ImportError:
                    try:
                        from ._macosx_universal.pyastyle import *
                        platform = "MacOS X Universal"
                    except ImportError:
                        raise ImportError("Could not find a suitable pyastyle binary for your platform and architecture.")
