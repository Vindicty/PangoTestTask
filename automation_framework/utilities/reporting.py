import allure
import pytest

from typing import List, Tuple

def attach_html_table_to_pytest_html(rows: List[Tuple], headers: List[str], title: str = "Data Table") -> None:
    """ Creates an HTML table from the provided data and attaches it to the pytest-html report.

    @param list: A list of tuples, where each tuple represents a row in the table.
    @param list headers: A list of column headers for the table.
    @param string title: A title displayed above the table. Defaults to "Data Table".

    Notes:
        This function sets the generated HTML table as a global variable (`pytest.extra_html_table`)
        which should be injected into the pytest-html report via a `pytest_html_results_summary` hook.
    """

    html = f"<h3>{title}</h3><table border='1' style='border-collapse:collapse;'>"
    html += "<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>"

    for row in rows:
        html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
    html += "</table>"


    pytest.extra_html_table = html
