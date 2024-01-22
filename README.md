# ![logo](./docs/images/bugcode_logo.svg)
![](https://img.shields.io/twitter/follow/bugcode)
![](https://img.shields.io/docker/pulls/khulnasoft/bugcode)
---


### Open Source Vulnerability Manager

Security has two difficult tasks: designing smart ways of getting new information, and keeping track of findings to improve remediation efforts. With Bugcode, you may focus on discovering vulnerabilities while we help you with the rest. Just use it in your terminal and get your work organized on the run.
Bugcode was made to let you take advantage of the available tools in the community in a truly multiuser way.

Bugcode aggregates and normalizes the data you load, allowing exploring it into different visualizations that are useful to managers and analysts alike.

![manage](./docs/images/manage.png)
![dashboard](./docs/images/dashboard.png)




To read about the latest features check out the [release notes](https://github.com/threatcode/bugcode/blob/master/RELEASE.md)!


## Install

---

### Docker-compose

The easiest way to get bugcode up and running is using our docker-compose

```shell
$ wget https://raw.githubusercontent.com/threatcode/bugcode/master/docker-compose.yaml
$ docker-compose up
```
If you want to customize, you can find an example config over here [Link](https://docs.threatcode.github.io/bugcode/Install-guide-Docker/)


### Docker

You need to have a [Postgres](https://github.com/threatcode/bugcode/wiki/Install-Guide)  running first.

```shell
 $ docker run \
     -v $HOME/.bugcode:/home/bugcode/.bugcode \
     -p 5985:5985 \
     -e PGSQL_USER='postgres_user' \
     -e PGSQL_HOST='postgres_ip' \
     -e PGSQL_PASSWD='postgres_password' \
     -e PGSQL_DBNAME='postgres_db_name' \
     khulnasoft/bugcode:latest
  ```

### PyPi
```shell
$ pip3 install bugcode
$ bugcode-manage initdb
$ bugcode-server
```

### Binary Packages (Debian/RPM)
You can find the installers on our [releases page](https://github.com/threatcode/bugcode/releases)

```shell
$ sudo apt install bugcode-server_amd64.deb
# Add your user to the bugcode group
$ bugcode-manage initdb
$ sudo systemctl start bugcode-server
```

Add your user to the `bugcode` group and then run

### Source
If you want to run directly from this repo, this is the recommended way:

```shell
$ pip3 install virtualenv
$ virtualenv bugcode_venv
$ source bugcode_venv/bin/activate
$ git clone git@github.com:threatcode/bugcode.git
$ pip3 install .
$ bugcode-manage initdb
$ bugcode-server
```

Check out our documentation for detailed information on how to install Bugcode in all of our supported platforms

For more information about the installation, check out our [Installation Wiki](https://github.com/threatcode/bugcode/wiki/Install-Guide).


In your browser now you can go to http://localhost:5985 and login with "bugcode" as username, and the password given by the installation process

## Getting Started

---

Learn about Bugcode holistic approach and rethink vulnerability management.

- [Centralize your vulnerability data](https://threatcode.github.io/bugcode/centralize-vulnerability-data/)
- [Automate the scanners you need](https://threatcode.github.io/bugcode/automate-scanners/)

### Integrating bugcode in your CI/CD

**Setup Bandit and OWASP ZAP in your pipeline**
- [GitHub](https://threatcode.github.io/bugcode/wp-content/whitepapers/Integrating%20Bugcode%20-%20Part%20One.pdf) [PDF]
- [Jenkins](https://threatcode.github.io/bugcode/wp-content/whitepapers/Integrating%20Bugcode%20-%20Part%20Two.pdf) [PDF]
- [TravisCI ](https://threatcode.github.io/bugcode/wp-content/whitepapers/Integrating%20Bugcode%20-%20Part%20Three.pdf) [PDF]

**Setup Bandit, OWASP ZAP and SonarQube in your pipeline**
- [Gitlab](https://threatcode.github.io/bugcode/wp-content/whitepapers/Integrating%20Bugcode%20-%20Part%20Four.pdf) [PDF]

## Bugcode Cli

---

Bugcode-cli is our command line client, providing easy access to the console tools, work in bugcode directly from the terminal!

This is a great way to [automate scans](https://docs.bugcode-cli.threatcode.github.io/bugcode/),  integrate it to [CI/CD pipeline](https://docs.bugcode-cli.threatcode.github.io/bugcode/)  or just get [metrics](https://docs.bugcode-cli.threatcode.github.io/bugcode/) from a workspace

```shell
$ pip3 install bugcode-cli
```

Check our [bugcode-cli](https://github.com/threatcode/bugcode-cli) repo

Check out the documentation [here](https://docs.bugcode-cli.threatcode.github.io/bugcode/).


![Example](./docs/images/general.gif)

## Bugcode Agents

---

[Bugcode Agents Dispatcher](https://github.com/threatcode/bugcode_agent_dispatcher) is a tool that gives [Bugcode](https://www.threatcode.github.io/bugcode) the ability to run scanners or tools remotely from the platform and get the results.




## Plugins

---

Connect you favorite tools through our [plugins](https://github.com/threatcode/bugcode_plugins). Right now there are more than [80+ supported tools](https://github.com/threatcode/bugcode/wiki/Plugin-List), among which you will find:

![](./docs/images/plugins.jpg)

Missing your favorite one? [Create a Pull Request](https://github.com/threatcode/bugcode_plugins/issues)!

There are two Plugin types:

**Console** plugins which interpret the output of the tools you execute.

```shell
$ bugcode-cli tool run \"nmap www.exampledomain.com\"
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
bugcode-cli tool report burp.xml
```

Creating custom plugins is super easy, [Read more about Plugins](http://github.com/threatcode/bugcode/wiki/Plugin-List).


## API

---
You can access directly to our API,
check out the documentation [here](https://api.threatcode.github.io/bugcode/).


## Links

* Homepage: [threatcode.github.io/bugcode](https://www.threatcode.github.io/bugcode)
* Documentation: [Bugcode Docs](https://docs.threatcode.github.io/bugcode)
* Download: [Download .deb/.rpm from releases page](https://github.com/threatcode/bugcode/releases)
* Issue tracker and feedback: [Github issue tracker](https://github.com/threatcode/bugcode/issues)
* Frequently Asked Questions: [bugCODE FAQ](https://docs.threatcode.github.io/bugcode/FAQ/)
* Twitter: [@bugcode](https://twitter.com/bugcode)
* Try one of our [Demos](https://demo101.threatcode.github.io/bugcode/#/login)
