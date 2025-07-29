import re


class ExcelRegex:
    EXCEL_REF_WITH_SHEET = re.compile(r"(\'?.*\'?)!(\$?[A-Z]+\$?[0-9]+)=(.*)")
    EXCEL_REF_OPTIONAL_SHEET = re.compile(r"^((\'?.+\'?)!)?(\$?[A-Z]+\$?[0-9]+)=(.*)")


class TypeRegex:
    IS_INT = re.compile(r"^-?([1-9]{1}[0-9]*|0)$")
    IS_FLOAT = re.compile(r"^-?([1-9]{1}[0-9]*|0)(\.\d+)?$")


class CommonRegex:
    VALID_EMAIL = re.compile(r'(\b[A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+)\.([A-Z|a-z]{2,7}\b)')

