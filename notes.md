Must include mention / attributes to Sounddevice in corespondence to MIT license




# Settings

### Setting Sections
- General
- Audio
- Video
- Appearance ?
- Notifications ?? (depends on Notification Tab)
- Advanced
    - File Location
    - Analytics stuff ???

### Settings Values

**General Settings**
- Screen Size / resolution
- Language
- Date format
- Time format
- Notification Toggle

**Video Settings**
- Camera device
- Connection Camera resolution ?
- User Camera resolution ?

**Audio Settings**
- Audio device
- Device input volume
- Output volume
- Playback ?
    - Playback volume ?

**Appearance**
- Light / Dark / OS Preference mode ??

**Advanced**
- File Location can be changed



## Locations of settings

### Screen-size / resolution
- ui.py
    - line 61 in Main class
### Language
- all
    - Unknown / not implemented
### Date Format
- ui.py
    - Possibly in home tab?
### Time Format
- ui.py
    - Line 113 in home tab
### Notifications toggle
- ui.py
    - Unknown / not implemented
### Camera Device
- video.py
    - Passed via initialization of videoConnect
### Audio Device
- audio.py
    - Passed via initialization of audioConnect
### Device input volume
- audio.py
    - Passed via initialization of audioConnect
### output Volume
- audio.py
    - Passed via initialization of audioConnect




