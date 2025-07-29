#!/usr/bin/python


def main():
    import changelist_foci
    from sys import argv
    input_data = changelist_foci.input.validate_input(argv[1:])
    for foci_block in changelist_foci.generate_changelist_foci(
        input_data.changelists,
        input_data.format_options
    ):
        print(foci_block, end='\n\n', flush=True)


if __name__ == "__main__":
    from pathlib import Path
    from sys import path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    path.append(str(current_directory)) # Add the directory to sys.path
    main()