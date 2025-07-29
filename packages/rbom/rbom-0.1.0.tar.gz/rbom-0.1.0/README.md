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

<hr/>

<div align="center">
  <h6>Haiku</h6>
  <small>
    "Scripts fire in the night, <br/>
    What shipped, who signed, what passed checks? <br/>
    RBOM leaves no doubt" <br/>
  </small>
</div>

<hr/>

<div align="center">
  <h1>UNDER DEVELOPMENT 🚧</h1>
</div>


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


