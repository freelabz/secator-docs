# Deployment

Once you have started using `secator` locally, you can deploy it on remote instances.

***

## Amazon Web Services (AWS)

_Amazon Web Services_ (AWS) is a subsidiary of Amazon that provides on-demand cloud computing platforms and APIs to individuals, companies.

### EC2

#### Deploy on a single EC2 instance

<figure><img src="../.gitbook/assets/secator-ec2-single.png" alt=""><figcaption><p>Deployment on a single EC2 instance</p></figcaption></figure>

To deploy `secator` on AWS EC2 on a single machine, we will install RabbitMQ, Redis and a Celery worker running `secator` on the instance.

<details>

<summary>Step 1: Create an EC2 instance with AMI Ubuntu</summary>

* Go to the AWS Management Console and create an EC2 instance using the Ubuntu AMI
* Configure **Security Groups:**
  * Allow port 6379 (Redis)
  * Allow port 5672 (RabitMQ)

</details>

<details>

<summary>Step 2: Install Go, Ruby, pip3, secator and commands supported by secator</summary>

```bash
sudo apt update

# Install Go
sudo rm -rf /usr/local/go
wget https://golang.org/dl/go1.20.2.linux-amd64.tar.gz
tar -xvf go1.20.2.linux-amd64.tar.gz
rm go1.20.2.linux-amd64.tar.gz || true
sudo mv go /usr/local
sudo rm /usr/bin/go
sudo ln -s /usr/local/go/bin/go /usr/bin/go

# Install Ruby
sudo apt update -y
sudo apt install -y ruby-full
sudo apt install -y rubygems

# Install pip3
sudo apt install python3-pip

# Install secator
pip3 install git+https://github.com/freelabz/secator.git
export PATH=$PATH:/home/ubuntu/.local/bin:/home/ubuntu/go/bin  # add to ~/.bashrc

# Install secator-supported commands
secator utils install
```

</details>

<details>

<summary>Step 3: Install RabbitMQ as a task broker</summary>

```bash
sudo apt-get install curl gnupg apt-transport-https -y
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
curl -1sLf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xf77f1eda57ebb1cc" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/net.launchpad.ppa.rabbitmq.erlang.gpg > /dev/null
curl -1sLf "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/io.packagecloud.rabbitmq.gpg > /dev/null
sudo apt-get update -y
sudo apt-get install -y erlang-base \
    erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
    erlang-runtime-tools erlang-snmp erlang-ssl \
    erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
sudo apt-get install rabbitmq-server -y --fix-missing
sudo rabbitmq-plugins enable rabbitmq_management
sudo rabbitmqctl add_user secator <RABBITMQ_PASSWORD>
sudo rabbitmqctl set_user_tags secator administrator
sudo rabbitmqctl set_permissions -p / secator ".*" ".*" ".*"
```

**Make sure your replace the \<RABBITMQ\_PASSWORD> by a strong password that you generate.**

</details>

<details>

<summary>Step 4: Install Redis as a storage backend</summary>

Celery needs a storage backend to store results. `secator` uses the storage backend to print results in real-time.

```bash
sudo apt install redis-server
sudo vi /etc/redis/redis.conf
# set requirepass to <REDIS_PASSWORD>
# comment the "bind 127.0.0.1 ::1" line
# change "protected-mode" to "no"

sudo /etc/init.d/redis-server restart
```

**Make sure your replace the \<REDIS\_PASSWORD> by a strong password that you generate.**

</details>

<details>

<summary>Step 5: Run a worker</summary>

Let's configure the worker `.env` with RabbitMQ and Redis connection details:

{% code title=".env" %}
```bash
CELERY_BROKER_URL=amqp://secator:<RABBITMQ_PASSWORD>@localhost:5672/
CELERY_RESULT_BACKEND=redis://default:<REDIS_PASSWORD>@localhost:6379/0
```
{% endcode %}

Now we can run a `secator worker`:

```
nohup secator worker > worker.log 2>&1 &  # start in background and save logs
```

</details>

<details>

<summary>Step 6: Run a task from your local machine</summary>

Let's configure the worker `.env` with RabbitMQ and Redis connection details:

{% code title=".env" %}
```bash
CELERY_BROKER_URL=amqp://secator:<RABBITMQ_PASSWORD>@<EC2_PUBLIC_IP>:5672/
CELERY_RESULT_BACKEND=redis://default:<REDIS_PASSWORD>@<EC2_PUBLIC_IP>:6379/0
```
{% endcode %}

Run a test task:

```
secator x httpx wikipedia.org
```

You should get an output like the following:

```bash
                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.0.1

                    freelabz.com

Celery worker is alive !
╭──────── Task httpx ─────────╮
│ 📜 Description: DotMap()    │
│ 👷 Workspace: default       │
│ 🍐 Targets:                 │
│    • wikipedia.org          │
│ 📌 Options:                 │
│    • follow_redirect: False │
│    • threads: 50            │
│    • debug_resp: False      │
╰─────────────────────────────╯
[10:20:54] 🎉 Task httpx sent to Celery worker...                                                                                                                                        _base.py:614
🏆 Live results:
🔗 https://wikipedia.org [301] [301 Moved Permanently] [mw1415.eqiad.wmnet] [HSTS] [text/html] [234]
```

</details>

#### Deploy on multiple EC2 instances

If you want a more scaleable architecture, we recommend deploying RabbitMQ, Redis, and Celery workers on different machines.

The steps are exactly the same as for [#deploy-on-a-single-ec2-instance](deployment.md#deploy-on-a-single-ec2-instance "mention"), expect that **Step 2**, **3**, and **4** will each be run on a separate EC2 instance.

Make sure to have the correct details in your `.env` and you should be good to go.

If you need a more scaleable architecture, deploy more Celery workers.

***

## Google Cloud Platform (GCP) \[WIP]

The _Google Cloud Platform_ (GCP) is a suite of cloud services that offers server space on virtual machines, internal networks, VPN connections, disk storage, ...

### Google Compute Engine \[WIP]

### Google Kubernetes Engine \[WIP]

### Cloud Run \[WIP]

***

## Axiom \[WIP]

**Axiom is a dynamic infrastructure framework** to efficiently work with multi-cloud environments, build and deploy repeatable infrastructure focussed on offensive and defensive security.

***

## Bare metal \[WIP]

### Kubernetes

### Docker-compose
