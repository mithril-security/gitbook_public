# Certificate and policy

### Extract Policy and default TLS Certificate from the Hardware docker image

You can extract the policy directly from the Docker Image using:

{% tabs %}
{% tab title="Hardware" %}
```bash
docker run --rm mithrilsecuritysas/blindai-server:latest /bin/cat /root/policy.toml > policy.toml
```
{% endtab %}

{% tab title="Azure DCs v3" %}
```
docker run --rm mithrilsecuritysas/blindai-server-dcsv3:latest /bin/cat /root/policy.toml > policy.toml
```
{% endtab %}
{% endtabs %}

You can also extract the default TLS certificate like this:&#x20;

{% tabs %}
{% tab title="Hardware" %}
```
docker run --rm mithrilsecuritysas/blindai-server:latest /bin/cat /root/tls/host_server.pem > host_server.pem
```
{% endtab %}

{% tab title="Azure DCs v3" %}
```
docker run --rm mithrilsecuritysas/blindai-server-dcsv3:latest /bin/cat /root/tls/host_server.pem > host_server.pem
```
{% endtab %}
{% endtabs %}

### Inject your own TLS Certificate to BlindAI

As you read above, the Docker image ships with a TLS certifcate by default. However, its private key is directly embedded in the public Docker hub image, therefore **it is not secure**, and should be replaced in production.

To generate a new self-signed TLS certificate, you can run

```
mkdir tls
openssl req -newkey rsa:2048 -nodes -keyout tls/host_server.key -out tls/host_server.pem -x509 -days 365
```

Once you generated your TLS certificate, you can use it with the project:

{% tabs %}
{% tab title="Hardware" %}
```bash
docker run \
    -v $(pwd)/tls:/root/tls \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server:latest /root/start.sh PCCS_API_KEY
```
{% endtab %}

{% tab title="Azure DCs v3" %}
```bash
docker run \
    -v $(pwd)/tls:/root/tls \
    -p 50051:50051 \
    -p 50052:50052 \
    --device /dev/sgx/enclave \
    --device /dev/sgx/provision \
    mithrilsecuritysas/blindai-server-dcsv3:latest
```
{% endtab %}
{% endtabs %}

`-v $(pwd)/tls:/root/tls` allows you to mount your own TLS certificate to the Docker Image.&#x20;
