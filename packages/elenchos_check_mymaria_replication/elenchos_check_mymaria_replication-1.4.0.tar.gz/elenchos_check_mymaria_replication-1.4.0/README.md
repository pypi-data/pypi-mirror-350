# Élenchos: Check MySQL and MariaDB Replication

A Élenchos command for checking the replication of a MySQL or MariaDB instance.

## Installation and Configuration

### Primary Instance

On the primary instance create a heartbeat by executing the following SQL commands.

```sql
create schema heartbeat;

use heartbeat;

create table heartbeat
(
  heartbeat datetime not null
) engine = InnoDB;

insert into heartbeat(heartbeat)
values (now());

create definer=root@localhost event heartbeat
on schedule every 1 minute starts '2016-02-07 09:22:34'
on completion preserve enable
comment 'Heartbeat for replication monitoring.'
do
update heartbeat
set heartbeat = now();
```

Using this heartbeat is more reliable than `Seconds_Behind_Master` as provided by the `show replica status` SQL command
which is `NULL` when the SQL thread is not running.

#### Replica Host

On the host where the replication instance is running, install Élenchos by executing the following commands.

```shell
cd /opt

mkdir elenchos
cd elenchos

python -m venv .venv
mkdir bin
ln -s ../.venv/bin/elenchos bin/elenchos

. .venv/bin/activate
pip install elenchos_check_mymaria_replication
/opt/elenchos/bin/elenchos gather-commands
```

Create the configuration file `/etc/nagios/replication.cfg`:

```shell
[nagios]
name           = MariaDB Replication <hostname>
max_lag        = 60
warning        = 15000
critical       = 20000
timestamp_path = timestamp.txt

[database]
host       = localhost
database   = heartbeat
port       = 3306
charset    = utf8mb4
collation  = utf8mb4_general_ci
supplement = credentials.cfg
```

The values of `host`, `port`, `charset`, and `collation` in the `database` section are the defaults and can be omitted.

Create the file `/etc/nagios/credentials.cfg` for storing the credentials of the replication monitoring user:

```ini
[database]
user     = rep_monitor
password = secret
```

Set the proper mode and ownership of `/etc/nagios/credentials.cfg` by executing the following commands.

```shell
chmod 400  /etc/nagios/credentials.cfg
chown nrpe.nrpe /etc/nagios/credentials.cfg
```

Create the configuration file `/etc/nrpe.d/check_mysql_replication.cfg` for `nrpe`:

```
command[check_mysql_replication]=/opt/elenchos/bin/elenchos check:mariadb-replication /etc/nagios/replication.cfg
```

Create the user for monitoring the replication by executing the following SQL statements.

```sql
create user `rep_monitor`@`localhost` identified by password('secret') with max_user_connections 1;
grant binlog monitor, slave monitor on *.* to `rep_monitor`@`localhost`;
grant select on heartbeat.heartbeat to rep_monitor@localhost;
```

Finally, restart the `nrpe` daemon.

```shell
systemctl reload nrpe
```

License
-------

This project is licensed under the terms of the MIT license.
