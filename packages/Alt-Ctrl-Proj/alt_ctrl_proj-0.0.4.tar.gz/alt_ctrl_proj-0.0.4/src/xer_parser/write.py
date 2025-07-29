"""Module for writing parsed XER data back to files.

This module provides functionality to write data from the Reader
object back to an XER file in the Primavera P6 format.
"""

import csv
from typing import Any


def writeXER(r: Any, filename: str) -> None:
    """
    Write parsed data back to an XER file.

    This function writes all the data contained in the Reader object back to a
    new XER file in the Primavera P6 format. It creates a TSV (tab-separated values)
    file with all the tables and records from the original XER file, potentially with
    modifications if made to the data structures.

    Parameters
    ----------
    r : Reader
        The Reader object containing the parsed XER data
    filename : str
        Path to the output XER file

    Returns
    -------
    None

    Notes
    -----
    The order of tables written to the XER file is important and follows Primavera P6's
    requirements for dependencies between tables. The function adds appropriate headers
    and format indicators for the XER file format.

    Examples
    --------
    >>> from xer_parser.reader import Reader
    >>> from xer_parser.write import writeXER
    >>> xer = Reader("input.xer")
    >>> # Make modifications to the data
    >>> writeXER(xer, "output.xer")
    """
    header = [
        "ERMHDR",
        "8.0",
        "2021-11-02",
        "Project",
        "admin",
        "Primavera",
        "Admin",
        "dbxDatabaseNoName",
        "Project Management",
        "U.K.",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as output:
        tsv_writer = csv.writer(output, delimiter="\t")
        tsv_writer.writerow(header)
        tsv_writer.writerows(r.currencies.get_tsv())
        tsv_writer.writerows(r.fintmpls.get_tsv())
        tsv_writer.writerows(r.nonworks.get_tsv())
        tsv_writer.writerows(r.obss.get_tsv())
        tsv_writer.writerows(r.pcattypes.get_tsv())
        tsv_writer.writerows(r.resourcecurves.get_tsv())
        tsv_writer.writerows(r.udftypes.get_tsv())
        tsv_writer.writerows(r.accounts.get_tsv())
        tsv_writer.writerows(r.pcatvals.get_tsv())
        tsv_writer.writerows(r.projects.get_tsv())
        tsv_writer.writerows(r.calendars.get_tsv())
        tsv_writer.writerows(r.projpcats.get_tsv())
        tsv_writer.writerows(r.scheduleoptions.get_tsv())
        tsv_writer.writerows(r.wbss.get_tsv())
        tsv_writer.writerows(r.resources.get_tsv())
        tsv_writer.writerows(r.acttypes.get_tsv())
        tsv_writer.writerows(r.resourcerates.get_tsv())
        tsv_writer.writerows(r.activities.get_tsv())
        tsv_writer.writerows(r.actvcodes.get_tsv())
        # PROJCOST
        tsv_writer.writerows(r.relations.get_tsv())
        tsv_writer.writerows(r.taskprocs.get_tsv())
        tsv_writer.writerows(r.activityresources.get_tsv())
        tsv_writer.writerows(r.activitycodes.get_tsv())
        tsv_writer.writerows(r.udfvalues.get_tsv())
        tsv_writer.writerow(["%E"])
