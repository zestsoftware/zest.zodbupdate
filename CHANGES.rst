Changelog
=========


2.0.0 (2025-06-25)
------------------

- Use `importlib.metadata` instead of `pkg_resources`.  [maurits]

- Add renames for Plone 6.1 and higher for the following interfaces:
  - `plone.base.interfaces.controlpanel.ITinyMCESpellCheckerSchema`
  - `plone.app.discussion.behaviors.IAllowDiscussion`
  - `plone.app.dexterity.behaviors.discussion.IAllowDiscussion`
  [maurits]

- Add renames for Plone 6.0 and higher for the following interfaces:
  - `plone.restapi.behaviors.ITiles`
  - `collective.dexteritytextindexer.behavior.IDexterityTextIndexer`
  [maurits]

- Remove the "webdav" renames.  This should be only needed on Plone 5.2.
  You should have used `zest.zodbupdate` 1.0.0 already there.
  [maurits]

- Use native namespaces.  [maurits]

- Support only Plone 6, require Python 3.9 or higher.  [maurits]


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
