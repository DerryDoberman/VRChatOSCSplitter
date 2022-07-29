# UDP Splitter

Made this UDP Splitter for splitting a VRChat OSC feed.

## Usage

```bash
python UDPSplitter.py [PRIMARY_PORT] [REPLAY_PORT_1] [RELAY_PORT_2] ...
```

Example

```bash
# Split 9001 to 9005 and 9006
python UDPSplitter.py 9001 9005 9006

or

# Split 9001 to 6969, 9696, and 42069
python UDPSplitter.py 9001 6969 9696 42069
```

Multiple ports can be streamed. At least one is required. May add some input
checking later.
