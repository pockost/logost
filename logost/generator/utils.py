import re

from .grok import GROK_PATTERN


def convert_grok_to_regex(grok):
    """Convert a grok to regex"""

    # Get all used grok pattern in this grok
    all_grok_pattern = set(re.findall('%{([^}]+)}', grok))

    # If no grok found grok is already a regex
    if not all_grok_pattern:
        return grok

    # Replace all grok by pattern
    for pattern in all_grok_pattern:
        grok = re.sub('%{' + pattern + '}', GROK_PATTERN[pattern], grok)

    # Check if grok does not contain grok
    return convert_grok_to_regex(grok)
