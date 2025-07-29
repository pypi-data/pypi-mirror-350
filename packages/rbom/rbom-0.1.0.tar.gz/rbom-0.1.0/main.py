


from src.rbom_parser import RBOMParser

if __name__ == "__main__":
    # load 
    rbom = RBOMParser.load_rbom('src/example.rbom.yaml')
    # sign
    signiture = RBOMParser.sign_rbom_secure(rbom, 'keys/private_rbom_key.pem')
    rbom = RBOMParser.embed_signature(rbom, signiture)
    # save
    RBOMParser.save_rbom(rbom, 'src/example.signed.rbom.yaml')
    print("RBOM signed and saved ✅")

    assert RBOMParser.verify_rbom_signature(rbom, signiture, 'keys/public_rbom_key.pem')
    print("RBOM signature verified ✅")

