# keymaer

> Experimental branch using `pyjion` for JIT optimization, use at your own risk.

key ma<del>pp</del>er (because my keyboard has the 0, p, ;, / button broken)

## Features

+ Key mapper (e.g. map `--` to `0`)

Fun fact: You can even make an IME out of this, check out [vn-telex.json](misc/vn-telex.json)
for a sample configuration (Not really working due to the limited implementation)

## Installation

Soon, for now you need to run from source (and with sudo in Linux)

Requires Python 3.10.x

### From source

#### Linux

+ Install module

```bash
sudo pip install -U git+https://github.com/teppyboy/keymaer@pyjion
# You can now run keymaer using: sudo python -m keymaer
```
+ Install executable (shell script) (optional)

```bash
sudo curl -L -o /usr/local/bin/keymaer https://github.com/teppyboy/keymaer/raw/master/misc/keymaer 
sudo chmod +x /usr/local/bin/keymaer
```

+ systemd service (optional)
  
```bash
sudo curl -L -o /etc/systemd/system/keymaer.service https://github.com/teppyboy/keymaer/raw/master/misc/keymaer.service
# sudo systemctl daemon-reload
# sudo systemctl enable --now keymaer
```

## License

MIT
