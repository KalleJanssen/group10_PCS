"""
Fixes checksum
"""

def fix_checksum(line):
    """Return a new copy of the TLE `line`, with the correct checksum appended.
    This discards any existing checksum at the end of the line, if a
    checksum is already present.
    """
    return line[:68].ljust(68) + str(compute_checksum(line))

def compute_checksum(line):
    """Compute the TLE checksum for the given line."""
    return sum((int(c) if c.isdigit() else c == '-') for c in line[0:68]) % 10

def verify_checksum(*lines):
    """Verify the checksum of one or more TLE lines.
    Raises `ValueError` if any of the lines fails its checksum, and
    includes the failing line in the error message.
    """
    for line in lines:
        checksum = line[68:69]
        if not checksum.isdigit():
            continue
        checksum = int(checksum)
        computed = compute_checksum(line)
        if checksum != computed:
            complaint = ('TLE line gives its checksum as {}'
                         ' but in fact tallies to {}:\n{}')
            raise ValueError(complaint.format(checksum, computed, line))
