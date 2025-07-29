import yaml
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

class RBOMParser:
    
    @classmethod
    def load_rbom(cls, file_path):
        """
        Load an RBOM file and return its content.
        """
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
        """
        Embed the signature into the RBOM content.
        """
        rbom_content['signature'] = signature
        return rbom_content
    
    @classmethod
    def sign_rbom(cls, rbom_content, secret_key="demo-secret-key"):
        raise DeprecationWarning()
    
        """
        Sign the RBOM content using a private key.
        """
        rbom_copy = rbom_content.copy()
        rbom_copy['signature'] = None  # Remove existing signature if any

        # serialize to a string for signing
        raw_yaml = yaml.safe_dump(rbom_copy, sort_keys=False)
        raw_bytes = raw_yaml.encode('utf-8') + secret_key.encode('utf-8')

        # generate SHA256 hash
        signature = hashlib.sha256(raw_bytes).digest()
        return base64.b64encode(signature).decode('utf-8')

 

