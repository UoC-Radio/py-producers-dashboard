A work in progress project for a desktop dashboard which will be usefull for live shows. It is intended to replace our current web based system. Functionality upgrades are also planned.

# Basic workflow
*  A radio producer logs in to the dashboard using its LDAP credentials
*  The dashboard presents shows that are associated to the user
*  The user selects an associated show or a Special Show (e.g. for one time shows, interviews etc), writes a message for the audience (shown on the site) and is then ready to begin the show
*  A wait screen appears, showing the remaining time for the current song from the [audio scheduler](https://github.com/UoC-Radio/audio-scheduler). The producer has the option to instantly go live or wait until the song is finished. *Later on when we have a digital console, faders will automatically switch from autopilot to appropriate input application/hardware.*
*  Live page shows incoming messages from audience, message of the producer to the audience, listeners statistics and functionality for setting metadata. Metadata can be either manually set by the producer or  automatically retrieved by media players which support MPRIS protocol, as soon as the producer uses one of them.
*  As soon as the show ends, the producer has to log off the dashboard and switch to autopilot playback. *Again a digital console permits automation to this procedure.*

# Additional features
*  Integration with recordings of the shows. E.g. as soon as the producer logs off, a dialog within the dashboard asks the producer where to save the recording of the show.
*  Edit info about a show, e.g. description, icon, etc
*  View/Delete/Export messages inbox

# Pending side work
*  Back-end, i.e. database and corresponding API needs to be implemented and tested