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
            (_, file, line, column, message, warning, _) = re.split(regex, line)
            if warning not in data:
                data[warning] = {}
            data[warning][(file, line, column)] = (file, line, column, message)
    return data


def formatData(data):
    """ Format data to HTML. """
    lines = []
    for warning, table in sorted(data.items()):
        length = len(table)
        lines.append(formatTable(table, warning, length))
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


def formatTable(table, warning, length):
    """ Format table to HTML. """
    lines = []
    for _, (file, line, column, message) in sorted(table.items()):
        lines.append(formatLine(file, line, column, message))
    lines = "\n".join(lines)
    template = str("""    <table>
      <tr><th colspan=4>{0} (1)</th></tr>
      <tr><th>File</th><th>Line</th><th>Column</th><th>Message</th></tr>
{2}
    </table>
    <br/>""").format(warning, length, lines)
    return template


def formatLine(file, line, column, message):
    """ Format line to HTML. """
    template = str("      <tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>").format(file, line, column, message)
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
