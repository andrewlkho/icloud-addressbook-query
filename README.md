icloud-addressbook-query.py is a short python script to get e-mail address from
the Mac OS X Contacts application when it is synced with iCloud (although it 
could easily be adapted for a non-synced Contacts).  It is primarily intended to
be used for address lookup in Mutt, and the output format reflects this.


Usage
=====

Place icloud-addressbook-query.py somewhere in your `$PATH`.  Then use the 
following configuration in your `muttrc`:

    set query_command = "icloud-addressbook-query.py '%s'"


SQLite and Write-Ahead-Logging
==============================

I hardlink the `AddressBook.abcddb` file into a git repository which is pushed
to my linux VM where mutt and icloud-addressbook-query.py are run from.  If you
have a similar setup to this (i.e. some method of synchronising the
`AddressBook.abcddb` file to another computer) then you may run into an odd bug
whereby more recent changes to your Contacts do not seem to be available to
icloud-addressbook-query.py.

As of version 3.7.0, SQLite implements atomic commits using a new method known
as "Write-Ahead-Logging" (WAL).  If you look in `~/Library/Application
Support/AddressBook/Sources/*` on more recent versions of OS X (possibly since
Mountain Lion) you will notice that instead of just `AddressBook.abcddb` there
is now also `AddressBook.abcddb-wal` and `AddressBook.abcddb-shm`; the latter is
an index to the WAL file which improves the performance of reading it.  The
source of the aforementioned bug is that by default SQLite allows the WAL file
to grow and will only perform a checkpoint (move the WAL file transactions into
the main database) when either of the following conditions occur:

- when the last database connection on a database file closes; or
- when a COMMIT causes the WAL file to be 1000 pages more in size

On OS X, there are always several processes with open connections to
`AddressBook.abcddb`: `lsof` currently shows `sharingd`, `CalendarAgent`,
`soagent`, `DataDetectorsDynamicData`, `Mail` and `Messages`.  The first
criterion above will therefore never trigger, and it takes quite some time for
the second to result in a checkpoint.  This is the cause of recent changes to
Contacts not being available to icloud-addressbook-query.py.

The simple solution to this is to manually tell SQLite to checkpoint whenever
you run into this issue.  You can do this with the following command:

    % sqlite3 ~/Library/Application\ Support/AddressBook/Sources/[SOURCE]/AddressBook.abcddb \
    >     'pragma wal_checkpoint(FULL);'

Of course, it is possible to have this done automatically by whatever
synchronising solution you use (such as a git pre-commit hook).

-- Andrew Ho <andrewho@andrewho.co.uk>
