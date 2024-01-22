# ![logo](./docs/images/bogcode_logo.svg)
![](https://img.shields.io/twitter/follow/bugcode)
![](https://img.shields.io/docker/pulls/bugcode/bogcode)
---


### Open Source Vulnerability Manager

Security has two difficult tasks: designing smart ways of getting new information, and keeping track of findings to improve remediation efforts. With Bogcode, you may focus on discovering vulnerabilities while we help you with the rest. Just use it in your terminal and get your work organized on the run.
Bogcode was made to let you take advantage of the available tools in the community in a truly multiuser way.

Bogcode aggregates and normalizes the data you load, allowing exploring it into different visualizations that are useful to managers and analysts alike.

![manage](./docs/images/manage.png)
![dashboard](./docs/images/dashboard.png)




To read about the latest features check out the [release notes](https://github.com/threatcode/bogcode/blob/master/RELEASE.md)!


## Install

---

### Docker-compose

The easiest way to get bogcode up and running is using our docker-compose

```shell
$ wget https://raw.githubusercontent.com/threatcode/bogcode/master/docker-compose.yaml
$ docker-compose up
```
If you want to customize, you can find an example config over here [Link](https://docs.bugcode.com/Install-guide-Docker/)


### Docker

You need to have a [Postgres](https://github.com/threatcode/bogcode/wiki/Install-Guide)  running first.

```shell
 $ docker run \
     -v $HOME/.bogcode:/home/bogcode/.bogcode \
     -p 5985:5985 \
     -e PGSQL_USER='postgres_user' \
     -e PGSQL_HOST='postgres_ip' \
     -e PGSQL_PASSWD='postgres_password' \
     -e PGSQL_DBNAME='postgres_db_name' \
     bugcode/bogcode:latest
  ```

### PyPi
```shell
$ pip3 install bugcode
$ bogcode-manage initdb
$ bogcode-server
```

### Binary Packages (Debian/RPM)
You can find the installers on our [releases page](https://github.com/threatcode/bogcode/releases)

```shell
$ sudo apt install bogcode-server_amd64.deb
# Add your user to the bogcode group
$ bogcode-manage initdb
$ sudo systemctl start bogcode-server
```

Add your user to the `bogcode` group and then run

### Source
If you want to run directly from this repo, this is the recommended way:

```shell
$ pip3 install virtualenv
$ virtualenv bogcode_venv
$ source bogcode_venv/bin/activate
$ git clone git@github.com:threatcode/bogcode.git
$ pip3 install .
$ bogcode-manage initdb
$ bogcode-server
```

Check out our documentation for detailed information on how to install Bogcode in all of our supported platforms

For more information about the installation, check out our [Installation Wiki](https://github.com/threatcode/bogcode/wiki/Install-Guide).


In your browser now you can go to http://localhost:5985 and login with "bogcode" as username, and the password given by the installation process

## Getting Started

---

Learn about Bogcode holistic approach and rethink vulnerability management.

- [Centralize your vulnerability data](https://bugcode.com/centralize-vulnerability-data/)
- [Automate the scanners you need](https://bugcode.com/automate-scanners/)

### Integrating bogcode in your CI/CD

**Setup Bandit and OWASP ZAP in your pipeline**
- [GitHub](https://bugcode.com/wp-content/whitepapers/Integrating%20Bogcode%20-%20Part%20One.pdf) [PDF]
- [Jenkins](https://bugcode.com/wp-content/whitepapers/Integrating%20Bogcode%20-%20Part%20Two.pdf) [PDF]
- [TravisCI ](https://bugcode.com/wp-content/whitepapers/Integrating%20Bogcode%20-%20Part%20Three.pdf) [PDF]

**Setup Bandit, OWASP ZAP and SonarQube in your pipeline**
- [Gitlab](https://bugcode.com/wp-content/whitepapers/Integrating%20Bogcode%20-%20Part%20Four.pdf) [PDF]

## Bogcode Cli

---

Bogcode-cli is our command line client, providing easy access to the console tools, work in bogcode directly from the terminal!

This is a great way to [automate scans](https://docs.bogcode-cli.bugcode.com/),  integrate it to [CI/CD pipeline](https://docs.bogcode-cli.bugcode.com/)  or just get [metrics](https://docs.bogcode-cli.bugcode.com/) from a workspace

```shell
$ pip3 install bogcode-cli
```

Check our [bogcode-cli](https://github.com/threatcode/bogcode-cli) repo

Check out the documentation [here](https://docs.bogcode-cli.bugcode.com/).


![Example](./docs/images/general.gif)

## Bogcode Agents

---

[Bogcode Agents Dispatcher](https://github.com/threatcode/bogcode_agent_dispatcher) is a tool that gives [Bogcode](https://www.bugcode.com) the ability to run scanners or tools remotely from the platform and get the results.




## Plugins

---

Connect you favorite tools through our [plugins](https://github.com/threatcode/bogcode_plugins). Right now there are more than [80+ supported tools](https://github.com/threatcode/bogcode/wiki/Plugin-List), among which you will find:

![](./docs/images/plugins.jpg)

Missing your favorite one? [Create a Pull Request](https://github.com/threatcode/bogcode_plugins/issues)!

There are two Plugin types:

**Console** plugins which interpret the output of the tools you execute.

```shell
$ bogcode-cli tool run \"nmap www.exampledomain.com\"
💻 Processing Nmap command
Starting Nmap 7.80 ( https://nmap.org ) at 2021-02-22 14:13 -03
Nmap scan report for www.exampledomain.com (10.196.205.130)
Host is up (0.17s latency).
rDNS record for 10.196.205.130: 10.196.205.130.bc.example.com
Not shown: 996 filtered ports
PORT     STATE  SERVICE
80/tcp   open   http
443/tcp  open   https
2222/tcp open   EtherNetIP-1
3306/tcp closed mysql
Nmap done: 1 IP address (1 host up) scanned in 11.12 seconds
⬆ Sending data to workspace: test
✔ Done

```


**Report** plugins which allows you to import previously generated artifacts like XMLs, JSONs.

```shell
bogcode-cli tool report burp.xml
```

Creating custom plugins is super easy, [Read more about Plugins](http://github.com/threatcode/bogcode/wiki/Plugin-List).


## API

---
You can access directly to our API,
check out the documentation [here](https://api.bugcode.com/).


## Links

* Homepage: [bugcode.com](https://www.bugcode.com)
* Documentation: [Bogcode Docs](https://docs.bugcode.com)
* Download: [Download .deb/.rpm from releases page](https://github.com/threatcode/bogcode/releases)
* Issue tracker and feedback: [Github issue tracker](https://github.com/threatcode/bogcode/issues)
* Frequently Asked Questions: [BogcodeSEC FAQ](https://docs.bugcode.com/FAQ/)
* Twitter: [@bugcode](https://twitter.com/bugcode)
* Try one of our [Demos](https://demo101.bugcode.com/#/login)
