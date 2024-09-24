from stackspot.stackspot_dict_types import QuickCommandPollExecutionOpts

# Stackspot

<center>

<img src="https://raw.githubusercontent.com/Potentii/stackspot-python/master/docs/images/simbolo-stk.svg" width="128px">

[![NPM Version][pypi-image]][pypi-url]

[Stackspot](https://stackspot.com/) API bindings for Python.

</center>


<br>

---


# Content

<!-- TOC -->
* [Installation](#installation)
* [Usage](#usage)
  * [⚙ Configuration](#-configuration)
  * [🌐 Using behind proxy](#-using-behind-proxy)
* [Methods](#methods)
  * [✨ AI](#-ai)
    * [AI - KS - Create a new Knowledge Source](#ai---ks---create-a-new-knowledge-source)
    * [AI - KS - Upload new file to a Knowledge Source](#ai---ks---upload-new-file-to-a-knowledge-source)
    * [AI - KS - Remove files from a Knowledge Source](#ai---ks---remove-files-from-a-knowledge-source)
    * [AI - Quick Command - Create a new execution](#ai---quick-command---create-a-new-execution)
    * [AI - Quick Command - Get execution](#ai---quick-command---get-execution)
    * [AI - Quick Command - Poll execution until it's done](#ai---quick-command---poll-execution-until-its-done)
  * [🗝️ Auth](#-auth)
    * [Auth - Get the access token](#auth---get-the-access-token)
* [License](#license)
<!-- TOC -->




<br>
<br>

---

## Installation

To install, simply add the package using `pip`:

```bash
pip install stackspot
```



<br>
<br>

---

## Usage

You can start using the **global instance**:

```python
from stackspot import Stackspot

# By default, the global instance will configure itself using the environment variables:
# - STACKSPOT_CLIENT_ID
# - STACKSPOT_CLIENT_SECRET
# - STACKSPOT_REALM

# Creating a new 'Knowledge Source' for example:
Stackspot.instance().ai.ks.create_ks('new-ks-test-api-2', 'New KS test', 'This is a test KS', 'CUSTOM')
```

---

### ⚙ Configuration

You can **configure** the global instance:

```python
from stackspot import Stackspot

# Using the 'config(opts)' method, to update the all the settings at once:
Stackspot.instance().config({
	'client_id': '...',
	'client_secret': '...',
	'realm': '...',
})



# Or update them individually:
Stackspot.instance() \
	.set_client_id('...') \
	.set_client_secret('...')
```

If you want to create your own **Stackspot instance**, you can either pass the settings on the **constructor**, use the 'config' method, or configure individual properties as well:

```python
from stackspot import Stackspot

# Creating a new stackspot instance (instead of using the 'global' one):
my_instance = Stackspot({
	'client_id': '...',
	'client_secret': '...',
	'realm': '...'
})


# If you want, it's possible to call the 'config(opts)' method of this instance as well to update the settings:
my_instance.config({ ... })


# Or configure properties individually:
my_instance.set_client_id('...')
```

---

### 🌐 Using behind proxy

Internally it uses the [`requests`](https://pypi.org/project/requests/) module to make requests, so you can just provide the standard `HTTP_PROXY`/`HTTPS_PROXY`/`NO_PROXY` environment variables.

See more: [Proxies with 'requests' module](https://requests.readthedocs.io/en/latest/user/advanced/#proxies).

<br>
<br>

---

## Methods

Here are all the available methods of this package:

<br>

### ✨ AI

All the **AI** related functions are bellow `Stackspot.instance().ai` namespace.


<br>

#### AI - KS - Create a new Knowledge Source

To **create** a new _Knowledge Source_, just run:

```python
from stackspot import Stackspot

Stackspot.instance().ai.ks.create_ks('my-new-ks', 'My new KS', 'A test KS', 'CUSTOM')
```

For more info about the **KS creation**, check out the official documentation: https://ai.stackspot.com/docs/knowledge-source/create-knowledge-source


<br>

#### AI - KS - Upload new file to a Knowledge Source

You can **add** or **update** existing objects inside a _Knowledge Source_:


```python
from stackspot import Stackspot

# This creates/updates a KS object named 'test.txt' containing 'Hello World' text:
Stackspot.instance().ai.ks.upload_ks_object('my-ks-slug', 'test.txt', 'Hello World')
```

<br>

#### AI - KS - Remove files from a Knowledge Source

To **batch remove** files from a _Knowledge Source_:

```python
from stackspot import Stackspot

# This removes ALL objects from the KS:
Stackspot.instance().ai.ks.batch_remove_ks_objects('my-ks-slug', 'ALL')
```

```python
from stackspot import Stackspot

# This removes only the STANDALONE objects from the KS:
Stackspot.instance().ai.ks.batch_remove_ks_objects('my-ks-slug', 'STANDALONE')
```

```python
from stackspot import Stackspot

# This removes only the UPLOADED objects from the KS:
Stackspot.instance().ai.ks.batch_remove_ks_objects('my-ks-slug', 'UPLOADED')
```

<br>

#### AI - Quick Command - Create a new execution

To manually **create** a new _Quick Command_ execution:

```python
from stackspot import Stackspot

execution_id = Stackspot.instance().ai.quick_command.create_execution('my-quick-command-slug', 'Input for this execution')
# Return example: "06J85YZZ5HVO1XXCKKR4TJ16N2"
```

<br>

#### AI - Quick Command - Get execution

After creating a new _Quick Command_ execution, you may want to **check it** to see if it has completed successfully, and get its result:

```python
from stackspot import Stackspot

execution = Stackspot.instance().ai.quick_command.get_execution('06J85YZZ5HVO1XXCKKR4TJ16N2')

print('status: ' + execution['progress']['status'])
```

_**Obs.:** Note that, at the time this call have been made, the execution may not yet be done, so you have to write some polling logic, or use the ['poll_execution'](#ai---quick-command---poll-execution-until-its-done) method._

<br>

#### AI - Quick Command - Poll execution until it's done

It can be cumbersome to write the logic to **poll** a _Quick Command_ execution after its creation to check if it's done. This library gets you covered on that:

```python
from stackspot import Stackspot

# Just create a new execution:
execution_id = Stackspot.instance().ai.quick_command.create_execution('my-quick-command-slug', 'Input for this execution')

# And call the poll method:
# This will check the execution status until it's done and then return the execution object (the 'opts' argument is optional):
execution = Stackspot.instance().ai.quick_command.poll_execution(execution_id, { 'delay': 0.5, 'on_callback_response': lambda e: print('status: ' + e['progress']['status']) })

print('final status: ' + execution['progress']['status']) # 'COMPLETED'
print('result: ' + execution['result']) # The Quick Command result.
```

<br>

---

### 🗝️ Auth

The library methods **already** handles the **authentication process**, but you can access the auth methods by yourself using the `Stackspot.instance().auth` namespace:

<br>

#### Auth - Get the access token

This will get the **cached token**, or **fetch a new one** if they aren't valid anymore:

```python
from stackspot import Stackspot

Stackspot.instance().auth.get_access_token()
```

_**Obs.:** To configure the authentication properties like `client_id`, `client_secret`, and `realm`, head back to the [Usage section](#usage)._


<br>
<br>

---

## License
[MIT](LICENSE)

[pypi-image]: https://img.shields.io/pypi/v/stackspot
[pypi-url]: https://pypi.org/project/stackspot
