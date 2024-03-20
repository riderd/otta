#!/usr/bin/env python3

import sys
from otta_site import SiteGroup
from otta_contact import ContactList

if len(sys.argv) < 4:
    print("Usage: %s otta_ocac.xls contacts.xls public_excluded_sites.txt" % sys.argv[0], file=sys.stderr)
    sys.exit(1)

otta_description_ocac_filename = sys.argv[1]
sites = SiteGroup(otta_description_ocac_filename)

contacts_filename = sys.argv[2]
public_excluded_sites_filename = sys.argv[3]
contacts = ContactList(contacts_filename, public_excluded_sites_filename)

if contacts.missing_sites(sites):
    contacts.print_contacts_without_sites(sites)
    sys.exit(1)

contacts.print_public_table(sites)
