

TTF_DEFAULT_PATTERN_NAME = "ttf"

TTFCLI_DESCRIPTION = "Create ttf pattern."
TTFCLI_PROG_NAME = "ttfcli"
TTFCLI_EPILOG = "This is probably an intermediary dataset creator for a pattern that are used in the MLF and other modules and it might change over time as the pattern evolves."


MLFCLI_DESCRIPTION = "Create MLF Data (alpha)"
MLFCLI_EPILOG="MLF Is used to create lagging features.  It uses the TTF data and creates lagging features for the given instrument and timeframe.  If a pattern is given and dont exist, it will try to create it using TTF."
MLFCLI_PROG_NAME="mlfcli"

PNCLI_DESCRIPTION = "Create or read pattern columns."
PNCLI_PROG_NAME = "pncli"
PNCLI_EPILOG = "This tool is used to create patterns with their corresponding columns or read existing patterns from disk."


MXCLI_PROG_NAME = "mxcli"
MXCLI_DESCRIPTION = "Create or read mx."
MXCLI_EPILOG = "This tool is used to create mx data with the given instrument and timeframe or read existing mx data from disk.  (Since the adding on Pattern, the mx data generation will change and evolve over time as we might need to add more features to load MX and the Desired Pattern then concat/merge the datasets (Efficiency))."

