#!/usr/bin/python

# Copyright (C) 2012 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import re
import sys
import urllib2

def main():
    if not(len(sys.argv) == 2 and sys.argv[1] == "-f"):
        print 'Usage:'
        print '    %s -f > /tmp/99-my-android.rules' % (sys.argv[0])
        print '    sudo cp /tmp/99-my-android.rules /etc/udev/rules.d'
        print '    sudo service udev restart'
        sys.exit(1)
        
    response = urllib2.urlopen('http://developer.android.com/guide/developing/device.html')
    html = response.read()

    print '# This file was generated by %s. Do not edit.' % (sys.argv[0])
    print '# Last updated: %s' % (datetime.date.today())
    print '#'

    #    <td>Dell</td>
    #    <td><code>413c</code></td>
    vendor_re = re.compile('^\s+<td>(.+)</td>')
    id_re = re.compile('^\s+<td><code>(.+)</code></td>')
    in_table = False
    current_vendor = '<unknown>'
    for line in html.splitlines():
        if in_table:
            m = id_re.match(line)
            if m:
                current_id = m.group(1)
                # # HTC
                # SUBSYSTEM=="usb", ATTR{idVendor}=="0bb4", MODE="0666"
                print '# %s' % (current_vendor)
                print 'SUBSYSTEM=="usb", ATTR{idVendor}=="%s", MODE="0666"' % (current_id)
            else:
                m = vendor_re.match(line)
                if m:
                    current_vendor = m.group(1)
        elif line.startswith("<table>"):
            in_table = True

if __name__ == "__main__":
    main()
