""" CL-FOCI Package Methods.
"""
from typing import Generator, Iterable

from changelist_data.changelist import Changelist, get_default_cl

from changelist_foci.foci_writer import generate_foci
from changelist_foci.format_options import FormatOptions, DEFAULT_FORMAT_OPTIONS
from changelist_foci.input.input_data import InputData


def get_changelist_foci(
    input_data: InputData,
) -> str:
    """ Processes InputData, returning the FOCI.

**Parameters:**
 - input_data (InputData): The program input data.

**Returns:**
 str - The FOCI formatted output.
    """
    # Select Changelist by Name
    if (cl_name := input_data.changelist_name) not in ["None", None]:   #todo: Remove the String "None", Next Jump Release.
        try:
            return generate_foci(
                changelist=filter(lambda x: x.name.startswith(cl_name), input_data.changelists).__next__(),
                format_options=input_data.format_options
            )
        except StopIteration:
            exit(f"Specified Changelist {cl_name} not present.")
    # All Changelists, separated by newlines
    elif input_data.all_changes:
        return '\n\n'.join(
            generate_changelist_foci(
                filter(lambda x: len(x.changes) > 0, input_data.changelists),
                input_data.format_options,
            )
        )
    else: # The Default Changelist
        return generate_foci(
            changelist=get_default_cl(input_data.changelists),
            format_options=input_data.format_options
        )


def generate_changelist_foci(
    changelists: Iterable[Changelist],
    foci_format: FormatOptions = DEFAULT_FORMAT_OPTIONS,
) -> Generator[str, None, None]:
    """ Generate String Blocks of FOCI.
- By default, all_changelists argument is True.
- Changelist_name is matched at the start of the string.
- If no changelist_name, tries the Default, then the first Changelist.

**Parameters:**
 - changelists (Iterable[Changelist]): The source collection of Changelists to filter and generate from.
 - foci_format (FormatOptions): The flags describing the details of the output format.
 - all_changelists (bool): Whether to generate the FOCI for all Changelists. Default: True.
 - changelist_name (str): The name of the Changelist to Generate FOCI for. Default: None.

**Yields:**
 str - Blocks of FOCI formatted text.
    """
    for cl in changelists:
        yield generate_foci(cl, foci_format)