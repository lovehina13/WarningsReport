# coding: utf-8

""" Warnings report. """

import re
import sys


def readFile(filePath):
    """ Read lines from file. """
    with open(filePath, "r", encoding="utf-8") as file:
        inLines = file.readlines()
        for it, inLine in enumerate(inLines):
            inLine = str(inLine).strip("\n")
            inLines[it] = inLine
        return inLines


def writeFile(filePath, inLines):
    """ Write lines to file. """
    with open(filePath, "w", encoding="utf-8") as file:
        for inLine in inLines:
            outLine = str("{0}\n").format(inLine)
            file.write(outLine)


def parseLog(lines):
    """ Parse log file. """
    data = {}
    regex = r"(.*):(\d*):(\d*): warning: (.*) \[(.*)\]"
    for line in lines:
        if re.match(regex, line):
            (_, file, line, column, message, warnings, _) = re.split(regex, line)
            for warning in warnings.split(","):
                if warning not in data:
                    data[warning] = {}
                data[warning][(file, line, column)] = (file, line, column, message)
    return data


def formatData(data):
    """ Format data to HTML. """
    lines = []
    lines.append(formatReportTable(data))
    for warning, table in sorted(data.items()):
        occurrences = len(table)
        lines.append(formatWarningTable(table, warning, occurrences))
    lines = "\n".join(lines)
    template = str("""<!DOCTYPE html>
<html>
  <head>
    <style>
      body {{
        font-family: Segoe UI, Helvetica, Arial, sans-serif;
        font-size: 12pt; }}
      table, th, td {{
        border: thin solid black;
        border-collapse: collapse;
        padding: 4pt; }}
      th {{
        background-color : #DFDFDF; }}
    </style>
  </head>
  <body>
{0}
  </body>
</html>""").format(lines)
    return template


def formatReportTable(data):
    """ Format report table to HTML. """
    lines = []
    total = 0
    for warning, table in sorted(data.items()):
        occurrences = len(table)
        total += occurrences
        lines.append(formatReportLine(warning, occurrences))
    lines = "\n".join(lines)
    template = str("""    <table>
      <tr><th colspan=2>Warnings report ({0})</th></tr>
      <tr><th>Warning</th><th>Occurrences</th></tr>
{1}
    </table>
    <br/>""").format(total, lines)
    return template


def formatReportLine(warning, occurrences):
    """ Format report line to HTML. """
    template = str("""      <tr><td><a href="#{0}">{1}</a></td><td>{2}</td></tr>""").format(warning, warning, occurrences)
    return template


def formatWarningTable(table, warning, occurrences):
    """ Format warning table to HTML. """
    lines = []
    for _, (file, line, column, message) in sorted(table.items()):
        lines.append(formatWarningLine(file, line, column, message))
    lines = "\n".join(lines)
    template = str("""    <table>
      <tr><th colspan=4><a id="{0}">{1} ({2})</a></th></tr>
      <tr><th>File</th><th>Line</th><th>Column</th><th>Message</th></tr>
{3}
    </table>
    <br/>""").format(warning, warning, occurrences, lines)
    return template


def formatWarningLine(file, line, column, message):
    """ Format warning line to HTML. """
    template = str("""      <tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>""").format(file, line, column, message)
    return template


def warningsReport(filePath, reportPath):
    """ Process warnings report. """
    lines = readFile(filePath)
    data = parseLog(lines)
    data = formatData(data)
    writeFile(reportPath, [data])


if __name__ == "__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    warningsReport(inputFile, outputFile)
