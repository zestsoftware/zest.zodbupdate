Changelog
=========


1.0.0 (2020-07-24)
------------------

- Handle the return of webdav in Zope 4.3, especially ``IFTPAccess`` and ``EtagBaseInterface``.
  Fixes `issue #1 <https://github.com/zestsoftware/zest.zodbupdate/issues/1>`_.
  [maurits]


1.0.0b2 (2020-03-25)
--------------------

- Add renames for a few webdav interfaces.
  In Zope 4.3 webdav will return, but until then they give real errors for zodbverify on Python 3.
  [maurits]


1.0.0b1 (2020-03-03)
--------------------

- Initial release.  [maurits]
