#!/usr/bin/env python3

import sys
import xlrd
from tabulate import tabulate

def clean(str):
   return str.strip().replace("\"", "")

class Site:
    """Represents an OTTA site

    attributes: acronym, description, otta_acronym
    """

    def __init__(self, acronym, description, ocac_acronym = None):
        self.acronym = acronym
        self.description = description
        self.ocac_acronym = ocac_acronym

class SiteGroup:
    """A group of OTTA sites

    Can get a site by acronym and return a list of acronyms in order
    """

    def __init__(self, otta_site_excel_path):
        self.map = {}
        wb = xlrd.open_workbook(otta_site_excel_path)
        sheet = wb.sheet_by_index(0)
        for row in sheet.get_rows():
            if len(row) > 3:
                print("More than 3 fields in " + row, file=sys.stderr)
                sys.exit(1)
            acronym = row[0].value
            # skip header
            if (acronym == "OTTA Site"):
                continue
            if (self.has_acronym(acronym)):
                print("Duplicate OTTA site " + acronym)
                sys.exit(1)
            description = row[1].value
            ocac_acronym = row[2].value
            if (ocac_acronym.strip() == ""):
                ocac_acronym = None
            self.map[acronym] = Site(acronym, description, ocac_acronym)

    def ordered_acronyms(self):
        # acronym_list = []
        # for acronym in self.map.keys():
        #     acronym_list.append(acronym)
        # return acronym_list.sort()
        return sorted(self.map.keys())

    def has_acronym(self, acronym):
        return acronym in self.map.keys()

    def site_for_acronym(self, acronym):
        if (acronym in self.map):
            return self.map[acronym]
        raise KeyError("No site for acronym " + acronym)

class Contact:
    """OTTA contact

    attributes: acronym, name, email, primary_contact
    """

    def __init__(self, acronym, name, email, primary_contact):
        self.acronym = acronym
        self.name = name
        self.email = email
        self.primary_contact = primary_contact

    def primary_yes_no(self):
        if self.primary_contact:
            return "Yes"
        return "No"

class ContactList:
    """List of OTTA contacts

    get list of primary contacts by acronym
    """


    def __init__(self, otta_contacts_excel_path):
        wb = xlrd.open_workbook(otta_contacts_excel_path)
        sheet = wb.sheet_by_index(0)
        self.missing_otta_sites = False

        self.contacts = {}
        for row in sheet.get_rows():
            acronym = clean(row[0].value)

            primary_contact = False;
            yes_no = row[1].value
            if (yes_no.lower() == "yes"):
                primary_contact = True;

            name = clean(row[2].value)
            email = clean(row[3].value)

            contact = Contact(acronym, name, email, primary_contact)
            contact_list_for_acronym = []
            if acronym in self.contacts:
                contact_list_for_acronym = self.contacts[acronym]
            contact_list_for_acronym.append(contact)
            self.contacts[acronym] = contact_list_for_acronym

        self.excluded_public_groups = ["ARL", "COE"]

    def missing_sites(self, sites):
        for acronym in self.contacts:
            if (not acronym in sites.ordered_acronyms()):
                return True
        return False

    def print_contacts_without_sites(self, sites):
        if not self.missing_sites(sites):
            return

        print("Some OTTA sites from contact(s) are missing from master list", file=sys.stderr)
        for acronym in self.contacts:
            if not acronym in sites.ordered_acronyms():
                names = []
                for contact in self.contacts[acronym]:
                    names.append(contact.name)
                print("%s: %s" % (acronym, names), file=sys.stderr)
                print()

    def _add_class(self, table_html:str):
        return table_html.replace("<table>", '<table class="otta-table">')

    def print_public_table(self, sites):
        table_data = []
        for acronym in sites.ordered_acronyms():
            found_primary_contact_for_site = False
            if acronym in self.excluded_public_groups:
                print(acronym + " excluded from public table", file=sys.stderr)
                continue
            site = sites.site_for_acronym(acronym)
            if not acronym in self.contacts:
                print("No contacts listed for OTTA site: " + acronym, file=sys.stderr)
                continue
            for contact in self.contacts[acronym]:
                if contact.primary_contact:
                    found_primary_contact_for_site = True
                    table_data.append([acronym, site.description, contact.name, contact.email, site.ocac_acronym])

            # maybe put out a warning for an OTTA site if there is no primary contact?
            if not found_primary_contact_for_site:
                print("Couldn't find a primary contact for " + acronym, file=sys.stderr)

        table_html = tabulate(table_data, headers=["OTTA Site", "Study Name", "Contact", "Email", "OCAC"], tablefmt="html")
        print(self._add_class(table_html))

    def print_member_table(self):
        table_data = []
        for acronym in sites.ordered_acronyms():
            if not acronym in self.contacts:
                print("No contacts listed for OTTA site: " + acronym)
                continue
            for contact in self.contacts[acronym]:
                table_data.append([acronym, contact.primary_yes_no(), contact.name, contact.email])

        table_html = tabulate(table_data, headers=["OTTA Study Acronym", "Primary Contact", "Name", "Email"], tablefmt="html")
        print(self._add_class(table_html))


otta_description_ocac_filename = sys.argv[1]
sites = SiteGroup(otta_description_ocac_filename)

contacts_filename = sys.argv[2]
contacts = ContactList(contacts_filename)

if contacts.missing_sites(sites):
    contacts.print_contacts_without_sites(sites)
    sys.exit(1)

if len(sys.argv) > 3:
    public_or_members = sys.argv[3]
    if public_or_members.lower() == "public":
        contacts.print_public_table(sites)
    elif public_or_members.lower() == "members":
        contacts.print_member_table()
    else:
        print("If specifying 3rd argument, it must be 'public' or 'members'. '%s' was supplied" % public_or_members, file = sys.stderr)
        sys.exit(1)
else:
    contacts.print_public_table(sites)
    contacts.print_member_table()
