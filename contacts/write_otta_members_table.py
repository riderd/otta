#!/usr/bin/env python3

import sys
from otta_site import SiteGroup
from otta_contact import ContactList

if len(sys.argv) < 3:
    print("Usage: %s otta_ocac.xls contacts.xls" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

otta_description_ocac_filename = sys.argv[1]
sites = SiteGroup(otta_description_ocac_filename)

contacts_filename = sys.argv[2]
contacts = ContactList(contacts_filename)

if contacts.missing_sites(sites):
    contacts.print_contacts_without_sites(sites)
    sys.exit(1)

contacts.print_member_table(sites)
