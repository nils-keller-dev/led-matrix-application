# installation

install git

```bash
sudo apt install git -y
```

clone this repo

```bash
git clone https://github.com/nils-keller-dev/led-matrix-application.git
```

install python and poetry

```bash
sudo apt install python3 python3-pip curl -y
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

you need the rgbmatrix library

```bash
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cp -r rpi-rgb-led-matrix/bindings/python/rgbmatrix led-matrix-application/led_matrix_application/
rm -rf rpi-rgb-led-matrix
```

add performance enhancement

```bash
sudo sed -i 's/$/ isolcpus=3/' /boot/firmware/cmdline.txt
```

disable audio module

```bash
sudo sed -i 's/^dtparam=audio=on$/dtparam=audio=off/' /boot/firmware/config.txt
echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/blacklist-snd_bcm2835.conf
sudo update-initramfs -u
```

install dependencies

```bash
cd led-matrix-application
poetry install --only main
```

setup env

```bash
bash setup-env.sh
cd led_matrix_application
```

fix permission

```bash
sudo chmod o+x /home/admin
sudo chmod o+x /home/admin/led-matrix-application
sudo chmod o+x /home/admin/led-matrix-application/led_matrix_application
sudo chmod o+x /home/admin/led-matrix-application/led_matrix_application/icons
# add write persmissions to be able to add state.json
sudo chmod o+w /home/admin/led-matrix-application/led_matrix_application
# add write permissions for images
sudo chmod 777 images
```

generate spotify token

```bash
poetry run task generate_spotify_cache
sudo chmod 777 .cache-<your-user-id>
```

add script to startup routine

```bash
chmod +x /home/admin/led-matrix-application/start.sh
sudo tee /etc/systemd/system/ledmatrix.service > /dev/null << EOF
[Unit]
Description=LED Matrix Application Startup Script
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/home/admin/led-matrix-application/start.sh
Restart=on-failure
User=admin
StandardOutput=journal
StandardError=journal
Environment="PATH=/home/admin/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

[Install]
WantedBy=multi-user.target
```

reboot

```bash
sudo reboot
```
