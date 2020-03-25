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
