<div align="center">
    <h1 align="center">RBOM</h1>

</div>

<div align="center">
  <h4>Release Bill Of Materials</h4>
</div>
<br/>
<p align="center">
<a href="https://pypi.org/project/rbom/"><img alt="DRF" src="https://img.shields.io/badge/certified_by-RBOM_0.1-ffc900?"></a>
<a href="https://opensource.org/licenses/Apache-2.0"><img alt="PyPI" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg"></a>
<a href="https://pypi.org/project/rbom/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rbom"></a>

</p>

### Overview 

A standardised format for releases to attest the where, what and how a release was made, packaged and sealed as a parsable ``rbom.signed.yaml`` file.

> Under development, package version v1.0.0 will be production ready.

### Installation 

```bash
pip install rbom
```

### Usage
```bash
rbom --help
```

### Signing 

Generate RSA Key Pair 

```bash
# private
openssl genrsa -out private_rbom_key.pem 2048
# public
openssl rsa -in private_rbom_key.pem -pubout -out public_rbom_key.pem
```