from github import Github



class RBOMPolicyHandlerGitHub:
    """Handler for RBOM policies using GitHub Actions check runs."""
    @staticmethod
    def check_run_passed(repo_full_name:str, commit_sha:str, policy_id:str, github_token:str) -> tuple[bool, str]:
        """
        Check if a GitHub Actions check run for a specific policy has passed.

        Args:
            repo_full_name (str): Full name of the repository (e.g., 'owner/repo').
            commit_sha (str): SHA of the commit to check.
            policy_id (str): ID of the policy to check.
            github_token (str): GitHub token for authentication.

        Returns:
        tuple:
            - bool: True if the check run passed, False otherwise.
            - str: HTML URL of the check run.
            
        """
        g = Github(github_token)
        repo = g.get_repo(repo_full_name)
        commit = repo.get_commit(commit_sha)
        # Get all check runs for the commit
        check_runs = commit.get_check_runs()
        
        # Find the check run for the specific policy
        for check_run in check_runs:
            if check_run.name == policy_id:
                
                return check_run.conclusion == 'success', check_run.html_url

        return False, None