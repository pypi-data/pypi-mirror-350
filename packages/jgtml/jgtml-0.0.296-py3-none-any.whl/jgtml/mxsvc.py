"""
@STCGoal Wrap what MX does as Services

- Create MX
- Read MX (and create if doesn't exist and if we have a corresponding TTF PatternsData in the DB, we can also create the TTF and MLF)
- Update MX
- Create TTF/MLF Patterns (data:  PatternName, PatternsColumns) 

Dependencies:
- MXRequest
- MLF

Target Usage:
- mxcli
- mxapi
"""
