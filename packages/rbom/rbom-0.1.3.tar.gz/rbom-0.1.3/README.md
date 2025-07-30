<div align="center">
    <h1 align="center" style="font-family: menlo">RBOM</h1>

</div>

<div align="center">
  <h4>Release Bill Of Materials</h4>
</div>
<br/>
<p align="center">
<a href="https://opensource.org/licenses/Apache-2.0"><img alt="PyPI" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"></a>
<a href="https://python.org/"><img alt="GA" src="https://img.shields.io/badge/Python-3.11.0-3776AB.svg?style=flat&logo=python&logoColor=white"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://pypi.org/project/rbom/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rbom"></a>

</p>


<div align="center">
  <h1>UNDER DEVELOPMENT 🚧</h1>
</div>


### Overview

Create a ``rbom.yaml`` in the root repository directory. <br/>
Multiple ``rbom.yaml`` can be used for each environment or use case ``dev.rbom.yaml``, 
``staging.rbom.yaml``, ``prod.rbom.yaml``.

### Custom Policy

Here for example a policy can be defined programatically, by checking
if the actor who ran the workflow is an admin: 
```bash
rbom set --policy custom:actor-is-admin --passed=${{ github.actor.is_admin }}
```

### Pre-Defined Policies
In the context of GitHub actions for example, a policy id can be that of a check suite such
as tests. 

The policy id ``gha-check: Run Tests`` must be the same as the job name.
We specify ``gha-check: `` to know to look at GitHub's check suite and then use ``Run Tests``
to determine if that specific job passed or failed.

This is auto-matically handled by ``rbom`` and the pre-defined policy.
You could also add a new policy on the fly by using:
```bash
rbom new --policy id="gha-check: Run Tests"
```



### Installation 

```bash
pip install rbom
```

### Signing 

Generate RSA Key Pair 

```bash
openssl genrsa -out private_rbom_key.pem 2048
openssl rsa -in private_rbom_key.pem -pubout -out public_rbom_key.pem
```


<hr/>


<div align="center">
  <h6>Haiku</h6>
  <small>
    "Scripts fire in the night, <br/>
    What shipped, who signed, what passed checks? <br/>
    RBOM leaves no doubt" <br/>
  </small>
</div>