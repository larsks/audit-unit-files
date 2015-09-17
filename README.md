This is a proof-of-concept for a tool to audit [systemd][] unit files to ensure
consistency.  It takes as input one (or more) INI-format files which
identify required sections and options.  For example:

    # This says that a unit file must haev a Unit section,
    # and this section must contain a Description option 
    # (with any content).
    [Unit]
    Description=__exists__

    # This says unit files must contain a Service section with
    # the Restart option set to "always"
    [Service]
    Restart=always

[systemd]: http://www.freedesktop.org/wiki/Software/systemd/

