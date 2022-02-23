# Telemetry

BlindAI collects anonymous data regarding general usage, this allows us to understand how you are using the project and how we can improve it.&#x20;

This feature can be disabled at any time and any collected data can be deleted on request.

### The data we are collecting <a href="#what-kind-of-data-do-we-collect" id="what-kind-of-data-do-we-collect"></a>

**We are collecting the following data:**

* **Execution metrics,** such as if you are executing BlindAI in software or hardware mode.
* **Usage** metrics, that allows us to see our features usages.

**We WILL NEVER collect those kind of data:**

* Identify or track users
* Collect personal information such as IP addresses, email addresses, website URLs
* Model or data uploaded to BlindAI.

### Why are we collecting telemetry data? <a href="#what-kind-of-data-do-we-collect" id="what-kind-of-data-do-we-collect"></a>

We are collecting those data solely to improve our project and see how BlindAI is used, to improve it and keep working on it full-time.

In order to do all of this, we need some data to see which features are the most used and if BlindAI is used in hardware or software mode. Having those data shows us on what we should focus to give the best experience possible to our users. In addition, it proves to our investors that our project is being used, allowing us to keep the project alive.&#x20;

### Disable Telemetry <a href="#what-kind-of-data-do-we-collect" id="what-kind-of-data-do-we-collect"></a>

Telemetry can be disabled at any time very easily:&#x20;

#### Setting up the appropriate variable environment (if you are building the project from source)

```bash
export BLINDAI_DISABLE_TELEMETRY=1
```

#### Setting up the appropriate variable environment (if you are using Docker 🐳)

```
-e BLINDAI_DISABLE_TELEMETRY=1
```

### How does the Telemetry work? <a href="#exhaustive-list-of-all-collected-data" id="exhaustive-list-of-all-collected-data"></a>

We are using [Amplitude](https://amplitude.com) to collect and see the Telemetry. It is a very powerful tool to highlight data and present them in the way we want.&#x20;

BlindAI is checking every 2 seconds if there was any new event (if the server started, if a model was uploaded, if the model was runned), and if it is the case, the datas are sent to Amplitude.

If you want a specification of the data we are collecting, you can find the list here:&#x20;

| Param         | description                                                                               |
| ------------- | ----------------------------------------------------------------------------------------- |
| `user_id`     | This is a random string generated when BlindAI starts. Allows us to group session's data. |
| `app_version` | BlindAI version number.                                                                   |
| `event_type`  | Describe the event. It can either be _`started`_, _`send_model` or `run_model`_           |
| `device_id`   | Shows on which system BlindAI was executed.                                               |
| `sgx_mode`    | Shows if BlindAI was run in software or hardware mode.                                    |
| `model_size`  | Size of the uploaded model, in bytes.                                                     |
| `time`        | Shows when the event was called.                                                          |
| `uptime`      | Shows since how long BlindAI was up when the event was done.                              |
