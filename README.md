Custom MuseScore Chord Symbols
==============================
Custom chord symbol XML files for MuseScore, with stacked alterations and custom spacing. These are modified versions of the `chords_std.xml` and `chords_jazz.xml` in the current MuseScore source code.


Usage
-----
In MuseScore, navigate to Format -> Style, then select Chord Symbols on the left. At the top, select Custom and open `chords_extended.xml` or `chords_extended_jazz.xml`. Set the extension and modifier scaling to `1.0` and the extension and modifier vertical offsets to `0.0`. After clicking OK, you need to save the file and reopen it in order for the stacked alterations to appear.

If you want to change the scaling or vertical offsets of the modifiers, they're easily editable at the top of the XML files. The settings in MuseScore seem to act on top of the XML file settings.


Troubleshooting
---------------
Sometimes when copying passages, the formatting will disappear for some symbols. To fix this, change the chord symbol style setting to Standard, save and reopen the file, then change it back to the custom XML file and save and reopen once more. This problem is probably due to how MuseScore caches the chord symbols, which doesn't seem to account for this type of custom formatting.
