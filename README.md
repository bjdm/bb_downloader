# bb_downloader

bb_downloader is a small package which is intended to be operated either from the command line or by an automated scheduler.
It will handle the Shibboleth authentication with SAML with the Blackboard Identity server using the bb_auth package, then
crawl whichever units have been declared in config.xml.

## Usage

The package is still under heavy development and as such does not work in its entirety. Currently, the application does not
work at all as QUT's robots.txt forbids crawling without written permission. However, all the individual modules work properly 
and it can be used with some slight editting to bb_downloader.py script in the root folder of the package.

To prevent this being used, I have added the unit tests to git ignore to obfuscate the usage as well as removed some of the 
comments from modules.

Please wait until permission can be attained from QUT before using this program. At the very least, update your user-agent 
to show your username and/or university password so QUT's administrators are aware of what is happening.

## Future Features

* Interactive interface to add new units

* Naming schemes (ie. MXB105_Lec1 instead of pulling name from Blackboard)

* Resuming failed/paused downloads

* Improved logging for use on servers
