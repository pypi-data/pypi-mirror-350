import os
import sys
import inspect

def cli_this(module_name, f_prefix="", build_manual=False):

    if build_manual:
        program_name = sys.argv[0].split(os.sep)[-1]
        if program_name.endswith("__main__.py"):
            program_name = os.environ.get("BASH_SRC", "PROGRAM").split(os.sep)[-1]
        all_f_map = {}
        for m,o in inspect.getmembers(sys.modules[module_name]):
            if inspect.isfunction(o) and m.startswith(f_prefix):
                f_name = m[len(f_prefix):]
                all_f_map[f_name] = o

        lines = ["Syntax:", ""]
        for f_current in sorted(all_f_map.keys()):
            f_sig = str(inspect.signature(all_f_map[f_current])).replace("(", "").replace(")", "").upper()
            f_sig = [ "<" + xx.strip() + ">" for xx in f_sig.split(" ") if xx.strip() != "" ]
            f_sig = " ".join(f_sig).replace(",", "")

            f_doc = inspect.getdoc(all_f_map[f_current])
            if f_doc == None:
                f_doc = ""
            f_doc = f_doc.split("\n")[0].strip()
            
            lines.append("  %s %s %s" % (program_name, f_current, f_sig))
            lines.append("  %s" % f_doc)
            lines.append("")
        return "\n".join(lines)

    if len(sys.argv) <= 1:
        print("No args given")
        sys.exit(1)
        return

    action = sys.argv[1]
    help_check = action.strip().replace("-", "")
    if help_check == "h" or help_check == "help":
        print(cli_this(module_name, f_prefix, build_manual=True))
        sys.exit(0)

    opts = sys.argv[2:]
    f_actual = None

    for m,o in inspect.getmembers(sys.modules[module_name]):
        if inspect.isfunction(o) and m.startswith(f_prefix) and m == f_prefix+action:
            f_actual = o
            break

    if f_actual is not None:
        # f_actual()
        #print("would call %s with %s" % (f_actual, str(opts)))
        f_actual(*opts)
        sys.exit(0)
    else:
        print("unknown action %s" % action)
        sys.exit(1)
