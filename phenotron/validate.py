import re
from click import BadParameter


class ClickValidator:

    @staticmethod
    def is_orcid(ctx, param, value):
        if bool(re.search('\\d{4}-\\d{4}-\\d{4}-\\w{4,5}', value)):
            return value
        else:
            raise BadParameter('ORCiD is not valid.')

    @staticmethod
    def is_sep(ctx, param, value):
        if value == "\t" or value == ",":
            return value
        else:
            raise BadParameter('Seperator must be tab or comma.')
