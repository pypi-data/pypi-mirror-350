# Welcome to Open World Agents

### Everything you need to build state-of-the-art foundation multimodal desktop agent, end-to-end.

Streamline your agent's lifecycle with Open World Agents. From data capture to model training and real-time evaluation, everything is designed for flexibility and performance.

Here's what we've got in store for you!

---

- **OWA's Env**: The asynchronous, event-driven environmental interface for real-time agent
    - **Asynchronous, real-time event processing**: Compared to existing LLM-agent frameworks and [gymnasium.Env](https://gymnasium.farama.org/api/env/), OWA's Env features an asynchronous processing design leveraging `Callables`, `Listeners`, and `Runnables`. [Learn more...](env/index.md)
    - **Dynamic EnvPlugin Activation**: Seamlessly register and activate EnvPlugins at runtime to customize and extend functionality, powered by registry pattern. [Learn more...](env/guide.md)
    - **Extensible, Open-Source Design**: Built for the community, by the community. Easily add custom plugins and extend the Env's functionality to suit your needs. [Learn more...](env/custom_plugins.md)

- **Predefined EnvPlugins**: We provide you some EnvPlugins which is suitable for constructing multimodal desktop agent.
    - [`owa-env-desktop`](env/plugins/desktop_env.md): Provides basic `Callables/Listeners` for mouse/keyboard/window events. 
    - [`owa-env-gst`](env/plugins/gstreamer_env.md): Powered by Windows APIs (`DXGI/WGC`) and the robust [GStreamer](https://gstreamer.freedesktop.org/) framework, provides high-performance and efficient screen capture/recording features. `owa-env-gst`'s screen capture is **6x faster** compared to alternatives. [Learn more...](data/recorder/why.md)

---

- **OWA's Data**: From high-performance, robust and open-source friendly data format to powerful, efficient and huggingface integration.
    - **`OWAMcap` file format**: high-performance, self-contained, flexible container file format for multimodal desktop log data, powered by the open-source container file format [mcap](https://mcap.dev/). [Learn more...](data/data_format.md)
    - **`ocap your-filename.mcap`**: powerful, efficient and easy-to-use desktop recorder. Contains keyboard/mouse and high-frequency screen data.
        - Powered by [`owa-env-gst`](env/plugins/gstreamer_env.md), ensuring superior performance compared to alternatives. [Learn more...](data/recorder/why.md)
    - **🤗 [Hugging Face](https://huggingface.co/) Integration**: Upload your own dataset created by simple `ocap` to huggingface and share with everyone! The era of open-source desktop data is **near and effortless**. Preview the dataset at [Hugging Face Spaces](https://huggingface.co/spaces/open-world-agents/visualize_dataset).

---

- **Comprehensive Examples**: We provides various examples that demonstrates how to build foundation multimodal desktop agent. Since it's just a example, you may customize anything you want. **Examples are in progress; stay tuned!**


<!-- - **Cross-Platform**: Works on Windows and macOS. -->


## Quick Start

- Simple example of using `Callables` and `Listeners`. [Learn more...](env/index.md)
    ```python
    import time

    from owa.core.registry import CALLABLES, LISTENERS, activate_module

    # Activate the standard environment module
    activate_module("owa.env.std")

    def callback():
        # Get current time in nanoseconds
        time_ns = CALLABLES["clock.time_ns"]()
        print(f"Current time in nanoseconds: {time_ns}")

    # Create a listener for clock/tick event, Set listener to trigger every 1 second
    tick = LISTENERS["clock/tick"]().configure(callback=callback, interval=1)

    # Start the listener
    tick.start()

    # Allow the listener to run for 2 seconds
    time.sleep(2)

    # Stop the listener and wait for it to finish
    tick.stop(), tick.join()

    ```

- Record your own desktop usage data by just running `ocap your-filename.mcap`. [Learn more...](data/recorder/install_and_usage.md)


- Curious about `OWAMCap` format? see following: (Note that `cat` output is a created example.)
```
$ owl mcap info example.mcap
library:   mcap-owa-support 0.3.2; mcap 1.2.2
profile:   owa
messages:  1062
duration:  8.8121584s
start:     2025-05-23T20:04:01.7269392+09:00 (1747998241.726939200)
end:       2025-05-23T20:04:10.5390976+09:00 (1747998250.539097600)
compression:
        zstd: [1/1 chunks] [113.42 KiB/17.52 KiB (84.55%)] [1.99 KiB/sec]
channels:
        (1) keyboard/state    9 msgs (1.02 Hz)    : owa.env.desktop.msg.KeyboardState [jsonschema]
        (2) mouse/state       9 msgs (1.02 Hz)    : owa.env.desktop.msg.MouseState [jsonschema]
        (3) window            9 msgs (1.02 Hz)    : owa.env.desktop.msg.WindowInfo [jsonschema]
        (4) screen          523 msgs (59.35 Hz)   : owa.env.gst.msg.ScreenEmitted [jsonschema]
        (5) mouse           510 msgs (57.87 Hz)   : owa.env.desktop.msg.MouseEvent [jsonschema]
        (6) keyboard          2 msgs (0.23 Hz)    : owa.env.desktop.msg.KeyboardEvent [jsonschema]
channels: 6
attachments: 0
metadata: 0

$ owl mcap cat example.mcap --n 8 --no-pretty
Topic: window, Timestamp: 1741628814049712700, Message: {'title': 'ZType – Typing Game - Type to Shoot - Chromium', 'rect': [389, 10, 955, 1022], 'hWnd': 7540094}
Topic: keyboard/state, Timestamp: 1741628814049712700, Message: {'buttons': []}
Topic: screen, Timestamp: 1741628814057575300, Message: {'path': 'example.mkv', 'pts': 14866666666,

... (additional lines omitted for brevity) ...

Topic: keyboard, Timestamp: 1741628814978561600, Message: {'event_type': 'press', 'vk': 162}
Topic: keyboard, Timestamp: 1741628815015522100, Message: {'event_type': 'release', 'vk': 162}
Topic: window, Timestamp: 1741628815050666400, Message: {'title': 'data_format.md - open-world-agents - Visual Studio Code', 'rect': [-8, -8, 1928, 1040], 'hWnd': 133438}

... (additional lines omitted for brevity) ...

Topic: mouse, Timestamp: 1741628816438561600, Message: {'event_type': 'move', 'x': 950, 'y': 891}
Topic: mouse, Timestamp: 1741628816441655400, Message: {'event_type': 'click', 'x': 950, 'y': 891, 'button': 'left', 'pressed': true}
```

<!-- TODO: add agent training lifecycle example -->

## Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details on how to:

- Set up your development environment.
- Submit bug reports.
- Propose new features.
- Create pull requests.

## License

This project is released under the MIT License. See the [LICENSE](https://github.com/open-world-agents/open-world-agents/blob/main/LICENSE) file for details.
