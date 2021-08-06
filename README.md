# cpiopwn
This is a POC of a RCE bug in cpio, caused by an integer overflow. This exploit bypasses all binary protections except full RELRO.

## Running the exploit

We've provided a Kali Dockerfile to run the exploit. The same exploit should work on a personal computer, but offsets may be different.

### Instructions
* Build the file
  * `sudo docker build -t cpiopwn .`
* Start the image and mount files
  * `sudo docker run --mount type=bind,source=$(pwd),destination=/cpiopwn -it cpiopwn /bin/bash`
* `cd cpiopwn`
* Run the exploit
  * `python3 exploit.py`

And that's it! After building the malicious pattern file, a prompt will show up, and it will start processing commands after a little bit of time.

### Notes
The exploit may take about a minute after the prompt appears before it starts responding to commands. We've provided a video of it running to show what should happen.

Additionally, the exploit may only work on computers with at least 16 GB of RAM, as it forces cpio to read gigabytes of input. We tested the exploit on a server with 12 GB of RAM, and it crashed.
