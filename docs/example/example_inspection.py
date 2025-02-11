#!/usr/bin/env python3
import wat
import math

class Style:
    PRIMARY_COLOR = "#007bff"
    SECONDARY_COLOR = "#6c757d"
    SUCCESS_COLOR = "#28a745"
    DANGER_COLOR = "#dc3545"
    WARNING_COLOR = "#ffc107"
    INFO_COLOR = "#17a2b8"
    LIGHT_COLOR = "#f8f9fa"
    DARK_COLOR = "#343a40"

if __name__ == '__main__':
    wat.caller(math.sqrt(2 + 2))