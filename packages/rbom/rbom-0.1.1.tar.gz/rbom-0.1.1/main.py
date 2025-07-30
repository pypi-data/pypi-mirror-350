


from src.rbom.policies.policy_handler import PolicyHandler

from src.rbom.rbom_parser import MetaData, RBOMParser

if __name__ == "__main__":
    # TODO: make into function call for the action 

    
    # load 
    rbom = RBOMParser.load_rbom('src/rbom/example.rbom.yaml')
    # set metadata 
    '''
    release_id 
    timestamp 
    commit 
    actor
    notes 
    distribution: 
        - version: "1.0"
        - target: "https://pypi.org/project/rbom/" (not required)
        - channel: "PyPi" (not required)

    '''



    # verify policies
    policies = PolicyHandler.parse_policies(
            rbom_content=rbom,
            repo_full_name="",
            commit_sha="",
            github_token="",
        )

    rbom = RBOMParser.embed_attribute(rbom, MetaData.policies, policies, is_policies=True)
    print("rbom pre sig: ", rbom)
    # sign
    signature = RBOMParser.sign_rbom_secure(rbom, 'keys/private_rbom_key.pem')
    rbmom = RBOMParser.embed_signature(rbom, signature=signature)

    # save
    RBOMParser.save_rbom(rbom, 'src/example.signed.rbom.yaml')
    print("RBOM signed and saved ✅")

    assert RBOMParser.verify_rbom_signature(rbom, signature, 'keys/public_rbom_key.pem')
    print("RBOM signature verified ✅")

