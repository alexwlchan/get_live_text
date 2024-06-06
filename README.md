# get_live_text

This tool uses Apple’s [Live Text feature](https://support.apple.com/en-gb/guide/preview/prvw625a5b2c/mac) to get text from an image on the command line.
This gives you a way to OCR images programatically without installing any extra software.

```console
get_live_text "picture_of_a_sign.jpg"
```

This is the same as if you'd copy/pasted the text from the image using the Preview app, but now you can do so programatically and in bulk.

## Installation

### Install from source

1.  Install the Xcode Command Line Tools
2.  Download the `get_live_text.swift` script from this repo
3.  Compile the script into a binary:

    ```console
    $ swiftc get_live_text.swift
    ```

4.  Copy the compiled binary `get_live_text` to somewhere in your PATH.

### Install a compiled binary

1.  Find the latest [GitHub release](https://github.com/alexwlchan/get_live_text/releases)
2.  Download the zip file which is appropriate for your system (Intel = `x86_64`, Apple Silion = `aarch64`)
3.  Open the zip file, and add the `get_live_text` app to your PATH

The app is just a compiled version of the Swift script.
It isn't notarised, so when you run it, you may get a warning that this app is from an unidentified developer.
You can get around this by right-clicking the app icon in Finder, and choosing `Open` from the shortcut menu.

## Usage

Run the script passing one arguments: the path to the image you want to OCR.

```console
$ get_live_text "picture_of_a_sign.jpg"
```
