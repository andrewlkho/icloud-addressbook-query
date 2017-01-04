#!/usr/bin/env python

import sys
import os
import sqlite3


def query_db(keyword):
    """Query the address book for keyword and return the results as a list of
    tuples.
    """
    sources = os.listdir(os.path.expanduser("~/Library/Application Support/AddressBook/Sources"))

    rows = []

    for source in sources:
        newrows = query_source_db(keyword, os.path.expanduser(os.path.join("~/Library/Application Support",
            "AddressBook/Sources", source, "AddressBook-v22.abcddb")))

        for row in newrows:
            rows.append(row)

    return rows

def query_source_db(keyword, database):
    connection = sqlite3.connect(database)
    c = connection.cursor()
    k = ("%%%s%%" % keyword.decode("utf-8"),) * 5
    c.execute("""SELECT ZABCDEMAILADDRESS.ZADDRESS, ZABCDRECORD.ZTITLE,
              ZABCDRECORD.ZFIRSTNAME, ZABCDRECORD.ZMIDDLENAME,
              ZABCDRECORD.ZLASTNAME, ZABCDRECORD.ZSUFFIX,
              ZABCDRECORD.ZORGANIZATION, ZABCDRECORD.ZDISPLAYFLAGS
              FROM ZABCDEMAILADDRESS
              LEFT OUTER JOIN ZABCDRECORD
              ON ZABCDEMAILADDRESS.ZOWNER = ZABCDRECORD.Z_PK
              WHERE ZABCDEMAILADDRESS.ZADDRESS LIKE ?
              OR ZABCDRECORD.ZFIRSTNAME LIKE ?
              OR ZABCDRECORD.ZMIDDLENAME LIKE ?
              OR ZABCDRECORD.ZLASTNAME LIKE ?
              OR ZABCDRECORD.ZORGANIZATION LIKE ?""", k)
    return [row for row in c]


def output(results):
    """Take the list of results and print it as per mutt's expected output"""
    if results:
        print " ".join([str(len(results)), "matching addresses..."])
        for row in results:
            # If the Company checkbox has been ticked (ZDISPLAYFLAGS=1,129) then
            # show the Company name, otherwise use First Last [(Company)]
            if row[7] % 2 == 1:
                fn = row[6]
            else:
                fn = " ".join(name for name in row[1:6] if name)
                if row[6]:
                    fn = "".join([fn, " (", row[6], ")"])

            # Use e-mail address as fn if all other fields are empty
            if not fn:
                fn = row[0]

            out = "\t".join([row[0], fn])
            print out.encode("utf-8")
        sys.exit(0)
    else:
        print "No matches"
        sys.exit(-1)


def main():
    if len(sys.argv) > 1:
        output(query_db(sys.argv[1]))

if __name__ == "__main__":
    main()
