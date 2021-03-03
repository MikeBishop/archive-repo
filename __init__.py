from . import archive, pr_branches
import sys

__all__ = ["archive", "pr_branches"]

if __name__ == "__main__":
    if sys.argv[0] == "archive":
        archive.init(sys.argv[1:])
    elif sys.argv[0] == "pr_branches":
        pr_branches.init(sys.argv[1:])
    else:
        print("Supported commands are " + ", ".join(__all__))
        print("Choose a command with -h for parameters")