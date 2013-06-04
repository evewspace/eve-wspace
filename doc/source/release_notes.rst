Release Notes
=============

v0.2 (4 June 2013)
------------------

Version 0.2 brings basic Alerts functionality, an improved Map UI, and lots of bug fixes.

Core
....

- Added ability for users to change their own passwords
- An optional e-mail field has been added to the registration form and the user profile
- Registries have been added for Navigation entries, Admin sections, and Profile sections
- The default wsgi.py module has been updated to work with Apache out of the box
- Added icons to indicate collapsable UI components
- Added a handler for default settings in Apps ('manage.py defaultsettings')


Map
...

- The default signature types have been renamed in accordance with CCP changes in Odyssey
- The bulk signature importer will now attempt to import signature types and names
- The bulk signature importer will no longer attempt to import POSes as signatures
- The System Details UI has been converted to a single tab pane to conserve space on small browser windows
- Systems in the chain which are not the root and which have active pilots are now highligted with a yellow border ring
- The system actions menu has been changed to a toolbar above the System Details tab pane
- Clicking a system now opens System Details directly
- Destinations have been broken into global and user scopes. Global destinations appear for everyone and user destinations appear for only the user who set it.
- Users may set user destinations from the Settings page.
- Wormholes that are End of Life now display how long they have been set EOL in the tooltip
- Systems may now be "collapsed" from the chain, sperating their children into a sub-chain
- Collapsed systems may be "Resurrected", re-adding them to the main chain with the same wormhole status as the time of collapsing
- The k-space route finder has been significantly optimized
- The map legend is now spaced evenly
- Regions are now shown in the tooltip for K-Space systems
- The info and occupied boxes in System Details are now only shown if those fields have data
- Adding or importing a signature with the exact same ID as one already on the map will cause the existing signature to be updated
- Signatures entered as "AAA-123", "AAA - 123", or "AAA123" will be standardized to "AAA-123" automtically
- Removed 8 character limitation for friendly names. Only 8 characters are displayed in the system ellipse.
- The Map is now automatically refreshed every 15 seconds by default
- Combined per-system wormhole and system tooltip requests into a single request each for system and wormhole tooltips
- Attempting to add a POS for an unknown corp that is in an alliance is now more graceful
- Fixed bug preventing the Cancel button on the Add POS dialog from functioning
- Removed the ability to set "Explicit permissions" for users who are not Map Admins
- Granted Map Admins the ability to see all maps regardless of permissions
- The cursor will now give an indication that the Reload Map button is clickable


Alerts
......

- Added the Alerts framework
- Added a sample alert method class to the documentation
- Added an alert method plugin for Jabber
- Added an external authentication bridge for ejabberd
- Fixed errors in the Jabber message template

SiteTracker
...........

- Added a first iteration of the SiteTracker status, fleet management, and fleet UIs
- Added ability to weight site credit by system
