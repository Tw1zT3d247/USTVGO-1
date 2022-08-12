
# USTVGO

- Proxify content from ustvgo.tv
- Panel Included
## Installation

Install with git

```bash
  git clone https://github.com/ParrotDevelopers/USTVGO.git
  pip3 install -r requirements.txt
```
    
## Usage

### Settings
```bash
python3 settings.py set <key> <value>
```
All keys are in settings.py

### Running
```bash
python3 main.py
```
Then open ```http://ip:port/admin/```  
Default username is ```admin``` and default password is ```admin```

### M3U
Create user in Admin CP
```
http://ip:port/username/password/playlist.m3u
```

### Data
Script stores data in different directories based on os
- Linux: ```$home/.ThePiratePlayer```
- Win$hit: ```%appdata%\ThePiratePlayer```
## License

[MPL V2](https://www.mozilla.org/en-US/MPL/2.0/)


## Legal
For legal reasons:
- I'm not associated with ustvgo.tv  
- Script is for demostrational purposes only  
- I cannot be held liable for any illegal use of this script  