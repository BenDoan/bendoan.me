title: Arch Linux on a Thinkpad 440s
date: 2014-05-13
tags: [linux, arch]
author: Ben Doan

![Thinkpad](http://bendoan.me/static/img/thinkpad.jpg)

I had a free day today, so I decided to leave Fedora and reinstall Arch Linux on my laptop.  When I first installed Arch on this computer, a Lenovo Thinkpad 440s, I ran into a number of issues.  I found a few tricks to make the installation process go smoothly that I've included here for future reference.

One issue I encountered in my previous install was that sound didn't work at all.  To get that working I needed to add some extra configuration to alsa in /etc/modprobe.d/alsa.conf:

    options snd_hda_intel enable=0,1
    options snd slots=snd_hda_intel, thinkpad_acpi
    options snd_hda_intel index=0
    options thinkpad_acpi index=1

The trackpad was another issue.  The new thinkpad clickpad gets a lot of critisim, but with the right configuration, I'm at the point where I almost like it better than the old style.  Here's what I ended up using for my synaptics config; this goes into the /etc/X11/xorg.conf.d/50-synaptics.conf file:

    Section "InputClass"
        Identifier "touchpad catchall"
        Driver "synaptics"
        MatchIsTouchpad "on"

        Option "TapButton1" "0"
        Option "TapButton2" "0"
        Option "TapButton3" "0"

        Option "ClickFinger3" "2"

        MatchDevicePath "/dev/input/event*"

        Option "ClickPad" "true"

        Option "VertHysteresis" "30"
        Option "HorizHysteresis" "30"

        Option "AreaTopEdge" "3000"
        Option "SoftButtonAreas" "66% 0 0 3000 33% 66% 0 3000"

        Option "VertTwoFingerScroll" "1"
        Option "HorizTwoFingerScroll" "1"
    EndSection


After those two issues where fixed everything else went swimmingly. My old dotfiles still worked, and now I'm back to a familiar environment.
