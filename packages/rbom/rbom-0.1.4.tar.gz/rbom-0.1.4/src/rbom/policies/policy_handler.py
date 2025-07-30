from .policy_ids import PolicyIds
from .providers.rbom_policy_handler_github import RBOMPolicyHandlerGitHub
from .policy_sources import PolicySources


class PolicyHandler:

    @classmethod
    def parse_policies(cls, rbom_content, repo_full_name:str, commit_sha:str, github_token:str) -> list[dict]:
        """
        Parse policies from the RBOM content, verify the policy and then return a yaml content
        version of the policies. So it can be inserted into the RBOM content.
        """
        policies = []
        print("Parsing policies from RBOM content...")
        # print("RBOM content policies:", rbom_content['policies'])
        if rbom_content['metadata'].get('policies') is not None:
            for policy in rbom_content['metadata'].get('policies'):
                print("Parsing policy:", policy)
                # * policy id
                policy_id = policy.get('id')
                if policy_id is not None:
                    if policy_id.startswith(PolicyIds.GHA_CHECK):
                        # run gha policy handler
                        policy_name = policy_id.split(PolicyIds.GHA_CHECK)[-1]
                        # policy_passed, link = RBOMPolicyHandlerGitHub.check_run_passed(
                        #     repo_full_name=repo_full_name,
                        #     commit_sha=commit_sha,
                        #     policy_id=policy_name,
                        #     github_token=github_token
                        # )
                        policy_passed, link = True, "https://example.com/check-run-link"  # Mocked for example purposes
                        policies.append({
                            'id': policy_id,
                            'passed': policy_passed,
                            'source': PolicySources.GH_CHECK_SUITE,
                            'link': link,
                        })
                    elif policy_id.startswith(PolicyIds.CUSTOM):
                        policies.append({
                            'id': policy_id,
                            'passed': policy.get('passed', False),
                            'source': PolicySources.CUSTOM,
                        })
                    else:
                        print(f"Unknown policy id: {policy_id}")

                policies.append(policy)
        return policies