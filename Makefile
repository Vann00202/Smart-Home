

deploy:
	sudo cp services/smart-home.service /etc/systemd/system/
	sudo loginctl enable-linger $(USER)
	mkdir -p ~/.config/systemd/user
	cp services/smart-user.service ~/.config/systemd/user/
	sudo systemctl daemon-reload
	systemctl --user daemon-reload
	sudo systemctl enable smart-home.service
	systemctl --user enable smart-user.service
