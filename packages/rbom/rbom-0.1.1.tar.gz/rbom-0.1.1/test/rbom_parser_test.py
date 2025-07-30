
import pytest
from src.rbom.rbom_parser import MetaData, RBOMParser
import os
import tempfile
import yaml
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
@pytest.fixture
def sample_rbom_content():
    return {
        "name": "test-rbom",
        "version": "1.0",
        "metadata": {
            MetaData.release_id: "release-2025-05-23",
            MetaData.timestamp: "2025-05-23T12:00:00Z",
            MetaData.commit: "abc123",
            MetaData.actor: "ghost-1234567890",
            MetaData.notes: "Initial deployment of payment API version 1.0",
            MetaData.distribution: [
                {"version": "1.0", "target": "https://pypi.org/project/rbom/", "channel": "PyPi"}
            ],
  
        }
    }

@pytest.fixture
def temp_yaml_file(sample_rbom_content):
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml') as f:
        yaml.safe_dump(sample_rbom_content, f)
        temp_path = f.name
    yield temp_path
    os.remove(temp_path)

@pytest.fixture
def temp_output_file():
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml') as f:
        temp_path = f.name
    yield temp_path
    os.remove(temp_path)

@pytest.fixture
def rsa_keypair_files():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    priv_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    pub_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
    priv_file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))
    priv_file.close()
    pub_file.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))
    pub_file.close()
    yield priv_file.name, pub_file.name
    os.remove(priv_file.name)
    os.remove(pub_file.name)

def test_load_rbom(temp_yaml_file, sample_rbom_content):
    loaded = RBOMParser.load_rbom(temp_yaml_file)
    assert loaded == sample_rbom_content

def test_save_rbom(sample_rbom_content, temp_output_file):
    RBOMParser.save_rbom(sample_rbom_content, temp_output_file)
    with open(temp_output_file, 'r') as f:
        loaded = yaml.safe_load(f)
    assert loaded == sample_rbom_content

def test_sign_and_verify_rbom_secure(sample_rbom_content, rsa_keypair_files):
    priv_path, pub_path = rsa_keypair_files
    signature = RBOMParser.sign_rbom_secure(sample_rbom_content, priv_path)
    assert isinstance(signature, str)
    # Should verify
    verified = RBOMParser.verify_rbom_signature(sample_rbom_content, signature, pub_path)
    assert verified is True
    # Should fail if tampered
    tampered = sample_rbom_content.copy()
    tampered["data"] = {"foo": "baz"}
    assert RBOMParser.verify_rbom_signature(tampered, signature, pub_path) is False


def test_embed_policies(sample_rbom_content):
    policies = [{"policy1": "pass", "policy2": "fail"}]
    result = RBOMParser.embed_attribute(sample_rbom_content.copy(), MetaData.policies, policies, is_policies=True)

    assert result["metadata"]["policies"] == policies

