# Smart Home

## Networking setup
#### General Info
- Raspberry Pi will serve as wireless access point for esp32 devices
- Devices will communicate over tcp sockets

#### Access Point
- Install linux-wifi-hotspot on raspberry pi device
- If only one wifi card/adaptor is used then the wifi must be turned off before creating access point
- Command to run hotspot on single adapter no internet: `sudo create_ap --no-virt wlan0 lo <SSID> <Password>`
- Hotspot with 2 wifi devices and set gateway IP: `sudo create_ap --no-virt -g 192.168.12.1 wlan1 wlan0 <SSID> <Password>`
- Gateway IP is important that we know for the client programs to know the server IP when run (Arduino has a method for obtaining gateway after)
- There is a method to create a hidden network but for demo it might not be a great idea

#### Firewall
The firewall must be set on the raspberry pi server to accept connections on the agreed upon port.
- For iptables run: `iptables -A INPUT -p tcp --dport <data-port> -j ACCEPT` where `<data-port>` is the port being used

## Web Server

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 19.2.4.

### Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

### Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

### Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

### Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

### Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

### Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
