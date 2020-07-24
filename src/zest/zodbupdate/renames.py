# -*- coding: utf-8 -*-
iface = "zope.interface Interface"
rename_dict = {
    "App.interfaces IPersistentExtra": iface,
    "App.interfaces IUndoSupport": iface,
    "Products.ResourceRegistries.interfaces.settings IResourceRegistriesSettings": iface,
}
# I have seen zodbverify on Python 2 complain with a warning about various webdav.interfaces factories.
# Might be okay to keep them, because webdav will return in Zope 4.3.
# But for zodbverify on Python 3 it is a real error, even though the instance starts fine.
# It may be wise to rename them after all.
try:
    import webdav
except ImportError:
    # IFTPAccess is not there anyway in the new webdav:
    rename_dict["webdav.interfaces IFTPAccess"] = iface
    rename_dict["OFS.interfaces IFTPAccess"] = iface

    # The next two inherit from IWriteLock, so seems a logical replacement,
    # but that is only available since Zope 4.
    try:
        from OFS.interfaces import IWriteLock

        writelock = "OFS.interfaces IWriteLock"
    except ImportError:
        writelock = iface
    rename_dict.update(
        {
            "webdav.interfaces IDAVCollection": writelock,
            "webdav.interfaces IDAVResource": writelock,
        }
    )
else:
    # webdav is back in Zope 4.3.
    # See https://github.com/zestsoftware/zest.zodbupdate/issues/1
    try:
        from OFS.EtagSupport import EtagBaseInterface
        rename_dict["webdav.EtagSupport EtagBaseInterface"] = "OFS.EtagSupport EtagBaseInterface"
    except ImportError:
        rename_dict["webdav.EtagSupport EtagBaseInterface"] = iface
    # IFTPAccess is back in webdav.
    # Well, that depends on wheter you have webdav from Zope or from ZServer...
    # See https://github.com/zestsoftware/zest.zodbupdate/pull/2#issuecomment-663647294
    try:
        from webdav.interfaces import IFTPAccess
        rename_dict["OFS.interfaces IFTPAccess"] = "webdav.interfaces IFTPAccess"
    except ImportError:
        rename_dict["OFS.interfaces IFTPAccess"] = iface
        rename_dict["webdav.interfaces IFTPAccess"] = iface
