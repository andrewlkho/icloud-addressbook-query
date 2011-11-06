#!/usr/bin/env python

import sys
import os
import sqlite3

def query_db(keyword):
    """Query the address book for keyword and return the results as a list of
    tuples.
    """
    source = os.listdir(os.path.expanduser("~/Library/Application Support/AddressBook/Sources"))[0]
    database = os.path.expanduser(os.path.join("~/Library/Application Support",
                                               "AddressBook/Sources", source,
                                               "AddressBook-v22.abcddb"))
    connection = sqlite3.connect(database)
    c = connection.cursor()
    k = ("%%%s%%" % keyword,) * 4
    c.execute("""SELECT ZABCDEMAILADDRESS.ZADDRESS, ZABCDRECORD.ZFIRSTNAME,
              ZABCDRECORD.ZLASTNAME, ZABCDRECORD.ZORGANIZATION
              FROM ZABCDEMAILADDRESS
              LEFT OUTER JOIN ZABCDRECORD
              ON ZABCDEMAILADDRESS.ZOWNER = ZABCDRECORD.Z_PK
              WHERE ZABCDEMAILADDRESS.ZADDRESS LIKE ?
              OR ZABCDRECORD.ZFIRSTNAME LIKE ?
              OR ZABCDRECORD.ZLASTNAME LIKE ?
              OR ZABCDRECORD.ZORGANIZATION LIKE ?""", k)
    return [row for row in c]

def output(results):
    """Take the list of results and print it as per mutt's expected output"""
    if results:
        print " ".join([str(len(results)), "matching addresses..."])
        for row in results:
            # Use the organisation as the name if there is one
            fn = row[3] or " ".join([row[1], row[2]])
            print "\t".join([row[0], fn])
        sys.exit(0)
    else:
        print "No matches"
        sys.exit(-1)

def main():
    if len(sys.argv) > 1:
        output(query_db(sys.argv[1]))

if __name__ == "__main__":
    main()
