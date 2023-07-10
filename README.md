# keymaer

key ma<del>pp</del>er (because my keyboard has the 0, p, ;, / button broken)

## Features

### V1 (default)

Using `keyboard` module to capture events and parse the events manually, this is more stable and tested for daily drive.

+ Key mapper (e.g. map `--` to `0`)
+ Simulated input box (like the Windows IME) (suitable for typing letters that are blocked by the actual input box)
    > Semi-broken on Linux when ran manually, and completely broken when ran as a service.

Fun fact: You can even make an IME out of this, check out [vn-telex.json](misc/vn-telex.json)
for a sample configuration (Not really working due to the limited implementation)

### V2 (experimental)

V2 tends to use `keyboard`'s `add_word_listener`, `remove_word_listener` and `add_abbreviation`
rather than using the self-implementation.

## Installation

Soon, for now you need to run from source (and with sudo in Linux)

### From source

#### Linux

+ Install module

```bash
sudo pip install --break-system-packages -U git+https://github.com/teppyboy/keymaer
# Don't worry, I doubt it will break anything at all.
# PyPy: sudo pypy3 -m pip install git+https://github.com/teppyboy/keymaer
# You can now run keymaer using: sudo python -m keymaer
```
+ Install executable (shell script) (optional)

```bash
sudo curl -L -o /usr/local/bin/keymaer https://github.com/teppyboy/keymaer/raw/master/misc/keymaer 
# PyPy: sudo curl -L -o /usr/local/bin/keymaer https://github.com/teppyboy/keymaer/raw/master/misc/keymaer-pypy
sudo chmod +x /usr/local/bin/keymaer
```

+ Install default config (optional)

```bash
sudo curl -L -o /etc/keymaer/config.json https://github.com/teppyboy/keymaer/raw/master/config.json 
```

+ systemd service (optional)
  
```bash
# System
sudo curl -L -o /etc/systemd/system/keymaer.service https://github.com/teppyboy/keymaer/raw/master/misc/keymaer-system.service
# sudo systemctl daemon-reload
# sudo systemctl enable --now keymaer

# User (will not work in login screen)
sudo curl -L -o /etc/systemd/user/keymaer.service https://github.com/teppyboy/keymaer/raw/master/misc/keymaer.service
# systemctl --user daemon-reload
# systemctl --user enable --now keymaer
```

## License

[MIT](LICENSE)
