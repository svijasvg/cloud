
*Updated 14 December, 2023 ·  dev.svija.love*

![Svija: SVG-based websites built in Adobe Illustrator][logo]

[logo]: http://files.svija.love/github/readme-logo.png "Svija: SVG-based websites built in Adobe Illustrator"

### Knowledge Base

<details><summary>PostgreSQL Failure</summary>

<br>Link to fix: [github.com/docker-library](https://github.com/docker-library/postgres/issues/415)

The command that worked:
```
localedef -i en_US -f UTF-8 en_US.UTF-8
```
Based on suggestions by Akamai, I tried:
```
systemctl status postgresql@14-main.service
```
This returned:
```
× postgresql@14-main.service - PostgreSQL Cluster 14-main

     Loaded: loaded (/lib/systemd/system/postgresql@.service; enabled-runtime; vendor preset: enabled)
     Active: failed (Result: protocol) since Thu 2023-12-14 09:24:03 CET; 2min 26s ago
    Process: 1838 ExecStart=/usr/bin/pg_ctlcluster --skip-systemctl-redirect 14-main start
             (code=exited, status=1/FAILURE)
        CPU: 131ms

[1843] LOG:  invalid value for parameter "lc_messages": "en_US.UTF-8"
[1843] LOG:  invalid value for parameter "lc_monetary": "en_US.UTF-8"
[1843] LOG:  invalid value for parameter "lc_numeric": "en_US.UTF-8"
[1843] LOG:  invalid value for parameter "lc_time": "en_US.UTF-8"
[1843] FATAL:  configuration file "/etc/postgresql/14/main/postgresql.conf" contains errors

[1838]: pg_ctl: could not start server
[1838]: Examine the log output.

systemd[1]: postgresql@14-main.service: Can't open PID file /run/postgresql/14-main.pid (yet?) after start: Operation not permitted
systemd[1]: postgresql@14-main.service: Failed with result 'protocol'.
systemd[1]: Failed to start PostgreSQL Cluster 14-main.
```
This caused me to remember that I had seen the following errors when logging in to the server:
```
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
```
Linode also suggested:
```
sudo systemctl start postgresql@14-main.service
```
This returned:
```
Job for postgresql@14-main.service failed
because the service did not take the steps required by its unit configuration.
See "systemctl status postgresql@14-main.service"
and "journalctl -xeu postgresql@14-main.service" for details.
```
[Google Doc](https://docs.google.com/document/d/1aKoiILInZcUytrSPUqhSOInwsAKRstXX7VCc6kvuESI/edit#heading=h.f1enxlgdh64j) with my debugging steps.

</details>


<details><summary></summary>
</details>


