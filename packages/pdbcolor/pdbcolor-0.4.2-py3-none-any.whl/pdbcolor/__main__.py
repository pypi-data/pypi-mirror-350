def main():
    import getopt
    import os
    import pdb
    import sys
    import traceback

    from pdbcolor import PdbColor

    opts, args = getopt.getopt(sys.argv[1:], "mhc:", ["help", "command="])

    if not args:
        print(pdb._usage)
        sys.exit(2)

    commands = []
    run_as_module = False
    for opt, optarg in opts:
        if opt in ["-h", "--help"]:
            print(pdb._usage)
            sys.exit()
        elif opt in ["-c", "--command"]:
            commands.append(optarg)
        elif opt in ["-m"]:
            run_as_module = True

    mainpyfile = args[0]  # Get script filename
    if not run_as_module and not os.path.exists(mainpyfile):
        print("Error:", mainpyfile, "does not exist")
        sys.exit(1)

    if run_as_module:
        import runpy

        try:
            runpy._get_module_details(mainpyfile)
        except Exception:
            traceback.print_exc()
            sys.exit(1)

    sys.argv[:] = args  # Hide "pdb.py" and pdb options from argument list

    if not run_as_module:
        mainpyfile = os.path.realpath(mainpyfile)
        # Replace pdb's dir with script's dir in front of module search path.
        sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    pdbcolor = PdbColor()
    pdbcolor.rcLines.extend(commands)
    while True:
        try:
            if run_as_module:
                pdbcolor._runmodule(mainpyfile)
            else:
                pdbcolor._runscript(mainpyfile)
            if pdbcolor._user_requested_quit:
                break
            print("The program finished and will be restarted")
        except pdb.Restart:
            print("Restarting", mainpyfile, "with arguments:")
            print("\t" + " ".join(sys.argv[1:]))
        except SystemExit:
            # In most cases SystemExit does not warrant a post-mortem session.
            print("The program exited via sys.exit(). Exit status:", end=" ")
            print(sys.exc_info()[1])
        except SyntaxError:
            traceback.print_exc()
            sys.exit(1)
        except:  # noqa: E722
            traceback.print_exc()
            print("Uncaught exception. Entering post mortem debugging")
            print("Running 'cont' or 'step' will restart the program")
            t = sys.exc_info()[2]
            pdbcolor.interaction(None, t)
            print(
                "Post mortem debugger finished. The "
                + mainpyfile
                + " will be restarted"
            )


# When invoked as main program, invoke the debugger on a script
if __name__ == "__main__":
    main()
