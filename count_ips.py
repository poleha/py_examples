#!/usr/bin/env python
import sys
import re
from collections import Counter

with open(sys.argv[1]) as f:
    ips = (re.search('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line).group() for line in f)
    c = Counter(ips)
    print(c.most_common(10))