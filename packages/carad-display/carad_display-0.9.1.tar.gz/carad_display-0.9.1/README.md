# carad-display

```
pip install --upgrade carad-display --break-system-packages
export PATH=$PATH:/home/$USER/.local/bin
```


create /script.sh with 
```
carad-display
```
->
```
mkdir -p ~/.config/autostart
vim ~/.config/autostart/myscript.desktop
```
-> place it here 
```
[Desktop Entry]
Type=Application
Exec=/script.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=MyApp
Comment=My application description
```
->
```
chmod +x /script.sh
```




```