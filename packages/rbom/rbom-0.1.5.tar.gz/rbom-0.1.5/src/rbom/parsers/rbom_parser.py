import yaml
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend



from typing import NamedTuple


class Attributes(NamedTuple):
    name = "name"
    version = "version"
    signature = "signature"
    metadata = "metadata"

class MetaData(NamedTuple):
    # top level
    release_id = "release_id"
    timestamp = "timestamp"
    commit = "commit"
    actor = "actor"
    notes = "notes"

    # sub attributes
    distribution = "distribution"
    policies = "policies"
    sbom = "sbom"

    # all
    items = [
        release_id,
        timestamp,
        commit,
        actor,
        notes,
        distribution,
        policies,
        sbom
    ]

class RBOMParser:
    
    @classmethod
    def load_rbom(cls, file_path):
        """
        Load an RBOM file and return its content.
        """
        rbom_content = None
        with open(file_path, 'r') as file:
            rbom_content = yaml.safe_load(file)

        return rbom_content
    
    @classmethod
    def save_rbom(cls, rbom_content, file_path):
        """
        Save the RBOM content to a file.
        """
        with open(file_path, 'w') as file:
            yaml.safe_dump(rbom_content, file, sort_keys=False)


    @classmethod
    def sign_rbom_secure(cls, rbom_content, private_key_path):
        """
        Sign the RBOM content using a private key.
        """
        rbom_to_sign = rbom_content.copy()
        rbom_to_sign['signature'] = None
        serialized = yaml.safe_dump(rbom_to_sign, sort_keys=False).encode('utf-8')

        with open(private_key_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        signature = private_key.sign(
            serialized,
            padding.PKCS1v15(),
            hashes.SHA256()
        )

        return base64.b64encode(signature).decode('utf-8')


    @classmethod
    def verify_rbom_signature(cls, rbom_content, signiture_b64, public_key_path):
        """
        Verify the signature of the RBOM content using a public key.
        """
        rbom_to_verify = rbom_content.copy()
        rbom_to_verify['signature'] =  None  # Remove signature for verification
        serialized = yaml.safe_dump(rbom_to_verify, sort_keys=False).encode('utf-8')

        with open(public_key_path, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        signiture = base64.b64decode(signiture_b64)

        try:
            public_key.verify(
                signiture,
                serialized,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception as e:  # Catch all exceptions for verification failure
            print(f"Signature verification failed: {e}")
            return False
    
    
    @classmethod
    def embed_signature(cls, rbom_content, signature):
        rbom_content[Attributes.signature] = signature
        return rbom_content

    @classmethod
    def embed_attribute(
        cls, 
        rbom_content, 
        attribute_name, 
        attribute_value,
        is_policies=False,
        is_distribution=False,
        is_sbom=False
        ):
        """
        Embed a single attribute into the RBOM metadata content.

        TODO: isinstance
        TODO: based on attribute_name parse the attribute_value as that specific type for the else:
        """
        if is_policies:
            if not isinstance(attribute_value, list):
                raise Exception("Policies attribute value must be a list")
            rbom_content[Attributes.metadata][attribute_name] = attribute_value
        elif is_distribution:
            if rbom_content[Attributes.metadata].get('distribution') is None:
                rbom_content[Attributes.metadata]['distribution'] = {}
            rbom_content[Attributes.metadata]['distribution'][attribute_name] = attribute_value
        elif is_sbom:
            if rbom_content[Attributes.metadata].get('sbom') is None:
                rbom_content[Attributes.metadata]['sbom'] = {}
            rbom_content[Attributes.metadata]['sbom'][attribute_name] = attribute_value
        else:
            rbom_content[Attributes.metadata][attribute_name] = attribute_value

        return rbom_content
    
    

