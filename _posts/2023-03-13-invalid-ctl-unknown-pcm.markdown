---
layout: post
title:  "Linux application fails with 'Invalid CTL' and 'Unknown PCM'"
date:   2023-03-13 09:00:00 +0000
categories: linux
---
> Note: this was initially written in May 2022, I'm not sure if it's still valid.
> Tested on Ubuntu 20.04

Suppose that you are trying to run an application that needs to be able to play sounds or record audio from a microphone in order to work. The application will not work without sound, but you are not particularly concerned with the sound - you just want the application to run.

If you are running this application on a virtual machine provided, for example, by AWS you might encounter one of the following error messages:

```
ALSA lib control.c:1379:(snd_ctl_open_noupdate) Invalid CTL
ALSA lib pcm.c:2642:(snd_pcm_open_noupdate) Unknown PCM
```

Or maybe the following ALSA commands fail with (you might need to install `alsa-utils`):

```
$ aplay -l
aplay: device_list:276: no soundcards found...
```

```
$ arecord -l
arecord: device_list:276: no soundcards found...
```

As you might realize from these messages, ALSA is not able to find a sound card. One way to check that is to look under `/dev/` for any device file that looks like `snd`. If you can't find it, it probably means that you are running your application on a system that lacks a sound card device. If you're using an AWS EC2 instance or any other VM, you might be tempted to solve this by tricking the application with a fake sound device.

After a few hours of googling and stackoverflowing, you may find three classes of solutions: people telling you to use `jack`, `snd-dummy` or `pulseaudio`.

## 1. `jack`

[Some](https://stackoverflow.com/questions/66213114/creating-a-virtual-sound-card-on-an-ec2) [people](https://stackoverflow.com/questions/40061291/linux-without-hardware-soundcard-capture-audio-playback-and-record-it-to-fil) claim that this solution saves you hours of messing with ALSA and just cuts to the chase on a higher level. Note that these stackoverflow answers are from 2016.

They recommend using `pulseaudio` (see below) or `jackd`. I will explain here how to route audio between your application and JACK. First install JACK and the ALSA plugins library

```
sudo apt install jackd2 libasound2-plugins
```

Then create (or edit) the `~/.asoundrc` file to define a virtual sound card called `rawjack` with 2 input and 2 output channels (`system:*` are the JACK ports), and another device `jack_device` that uses the `plug` plugin to automatically convert between data formats:

```
pcm.rawjack {
    type jack
    playback_ports {
        0 system:playback_1
        1 system:playback_2
    }
    capture_ports {
        0 system:capture_1
        1 system:capture_2
    }
}

pcm.jack_device {
    type plug
    slave { pcm "rawjack" }
}
```

Make sure to log out and log in so that your user is added to the audio group. This should be enough for `aplay -D jack_device test.wav` to work with any `.wav` file. To make applications use this virtual soundcard by default, just name it `!default` instead of `jack_device` and make sure no other device in this file is named `!default`.

> Note: if this doesn't work, you might need to edit the `/etc/security/limits.conf` file, see the output of `jackd -d alsa`.

In my system, even after doing this, I still get the error messages at the top of this post when I run my application. This bring us to the second kind of answer we find on the internet...

## 2. `snd-dummy`

[Some people](https://groups.google.com/g/ec2ubuntu/c/gyaom4lTwBw) will tell you to use the ALSA dummy sound card (`snd-dummy`) or the loopback sound card (`snd-aloop`). See also [here](https://superuser.com/questions/344760/how-to-create-a-dummy-sound-card-device-in-linux-server), [here](https://stackoverflow.com/questions/44032488/dummy-soundcard-for-amazon-linux-server), [here](https://ubuntuforums.org/showthread.php?t=2385473) and [here](https://www.reddit.com/r/linux4noobs/comments/2m77g1/help_a_noob_create_a_dummy_sound_card_driver/).

The dummy sound card just redirects any application output to a sink (`/dev/null`) and uses the sink to generate input data for applications as well.

The loopback virtual sound card sends any input signal from applications back to itself - so you can do things like recording the signal within the device. So how do we get these devices to show up?

Every answer directs you to this out of date page in the ALSA wiki: [Matrix:Module-dummy](https://www.alsa-project.org/main/index.php/Matrix:Module-dummy). If `sudo modprobe snd-dummy` or `sudo modprobe snd-aloop` works, you're golden. But if, like me, you get

```
$ sudo modprobe snd-aloop
modprobe: FATAL: Module snd-aloop not found in directory /lib/modules/5.13.0-1025-aws
```

the out of date guide suggests downloading the `alsa-driver-*` package with the same version as your ALSA, but if you go to the [ALSA downloads page](https://www.alsa-project.org/wiki/Download) you'll see that this package is obsolete: it's been integrated with the kernel. Then that means that whoever compiled your kernel version did so without the ALSA loopback kernel module.

Some of the links above suggest installing the `linux-image-extra-$(uname-r)` package. If you're lucky, this package will exist in one of your apt sources and this will install the required modules. If you're out of luck, like me, your last resource might be `pulseaudio`.

## 3. `pulseaudio`

Install `pulseaudio` with 

```
sudo apt install pulseaudio
```

and start the PulseAudio server with `pulseaudio --start` (you can start it by default by uncommenting the `autospawn = yes` line in `/etc/pulse/client.conf`). We can use the CLI utility to list all known sounds cards: `pactl list cards` (in my case, I get none).

PulseAudio uses modules to route and process audio. For example, a protocol module accepts audio from a source (an application, process, a microphone device), routes it through another module, and finally an output module redirects it to a sink (a sound card, a file, or the network).

You can use `pactl list modules` to list the existing modules - you will notice that PulseAudio enables by default the `module-null-sink` module and sets it as the default sink (that's why you see "Dummy Output" on Ubuntu/GNOME when your sound card is not working). This should be enough for `aplay test.wav` to work.

If for some reason you don't have this default sink enabled on your system, you can [do](https://stackoverflow.com/questions/49545647/programmatic-alsa-loopback):

```
pactl load-module module-null-sink sink_name=auto_null
pactl set-default-sink auto_null
```

## Background

[ALSA](https://www.alsa-project.org/wiki/Main_Page) is a part of the Linux kernel that controls sound card devices. It is basically an API for controlling your sound cards. It provides many sound device drivers that Linux applications can use to communicate with the different types of sound cards on their system.

The sound card devices are defined in a configuration file that can be overridden in `~/.asoundrc`. A minimal definition would be

```
pcm.foo {
        type hw
        card 0
        device 0
}
```

This provides an alias (`foo`) to the physical sound card 0 (`card 0`), `device 0` (a card can have multiple devices). With this alias, we could play a sound file with `aplay -D foo test.wav`, for example.

These definitions can be made more complicated using PCM plugins. For example, suppose we want to set up a rate converter: we want all of our audio to be converted to 16 kHz before it's played. We can do this with the "rate" plugin:

```
pcm.rate_convert {
        type rate
        slave {
            pcm foo
            rate 16000
        }
}
```

and call it with `aplay -D rate_convert test.wav`.

[PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/) and [JACK](https://jackaudio/) are sound servers - they are applications that use ALSA (or other sound card controllers) to do more complicated things with sound. You could in theory use ALSA directly, but Ubuntu for example comes pre-installed with PulseAudio because it makes it easier to mix audio from different applications and feed them pre-mixed to ALSA. JACK does similar things (as far as I understand) but on top of that it offers routing audio between applications and other advanced "low latency" features.
