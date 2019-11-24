from flask import Flask

"""
App for tracking times and algs for 3-style comms

Timer view:
- Shows a case, enter time with typing or timer
- Option to show/hide/edit alg for that case
- Next button for next case
- Prioritizes times based on:
    - Amount drilled, less first
    - Average time, slower first
    - Time since drilled, longer first
View time history, for case or for all
"""
