# keymaer

key ma<del>pp</del>er (because my keyboard has the 0, p, ;, / button broken)

## Installation

Soon, for now you need to run from source (and with sudo in Linux)

### From source

#### Linux

+ Install module

```bash
sudo pip install git+https://github.com/teppyboy/keymaer
# PyPy: sudo pypy3 -m pip install git+https://github.com/boppreh/keyboard
# You can now run keymaer using: sudo python -m keymaer
```
+ Install executable (shell script) (optional)

```bash
sudo curl -OL <url>
# PyPy: sudo curl -OL <url>
chmod +x /usr/local/bin/keymaer
```

+ systemd service (optional)
  
```bash
sudo curl -OL <url>
# sudo systemctl daemon-reload
# sudo systemctl enable --now keymaer
```

## License

MIT
