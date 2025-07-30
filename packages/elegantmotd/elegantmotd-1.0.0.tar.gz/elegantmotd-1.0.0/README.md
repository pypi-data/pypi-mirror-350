# ElegantMOTD

ElegantMOTD is a Python-based Message of the Day (MOTD) generator for displaying system information in a visually
appealing and informative manner. It works on Linux systems and provides details such as system load, disk usage, memory
usage, swap usage, temperature, network interfaces, CPU usage, and more.

## Features

- Rich, colorful text-based output.
- Displays various system information.
- Customizable visual theme.
- Easy to use and integrate into your system.

## Usage

To display the Message of the Day, run the following command:

```bash
elegantmotd
```

You can choose a visual theme using the `--theme` (or `-t`) option:

```bash
elegantmotd --theme emoji
elegantmotd -t nerdfont
```

### Available themes

- `none` (default): no icons, clean plain text (TTY-safe)
- `emoji`: colorful emojis for graphical environments
- `nerdfont`: icon-rich display using [Nerd Fonts](https://www.nerdfonts.com)

## Live Updates

If you want to enable live updates of the system information, you can use the `--watch`/`-w` option:

```bash
elegantmotd --watch
```

With the `--watch` option, the MOTD will be continuously updated with the latest system information.

## Output

![Output](resources/output.png)

## Customization

You can customize the output by modifying the `motd.py` file and adding or removing system information modules as per
your preference. The available modules are:

- Load
- Disk
- Memory
- Temperature
- Process
- LoggedInUsers
- Network
- CPU

To add or remove a module, simply add or remove the corresponding import statement and the respective class instance
from the `sysinfos` list in the `display()` function.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
