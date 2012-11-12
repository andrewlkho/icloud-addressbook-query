icloud-addressbook-query.py is a short python script to get e-mail address from 
the Mac OS X Address Book when it is synced with iCloud (although it could 
easily be adapted for a non-synced Address Book).  It is primarily intended to
be used for address lookup in Mutt, and the output format reflects this.


Usage
=====

Place icloud-addressbook-query.py somewhere in your `$PATH`.  Then use the 
following configuration in your `muttrc`:

    set query_command = "icloud-addressbook-query.py '%s'"


-- Andrew Ho <andrewho@andrewho.co.uk>
