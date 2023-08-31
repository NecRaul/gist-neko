from .download import download_gists
import argparse

def main():
    parser = argparse.ArgumentParser(description="Download specified user's all gists at once.")
    parser.add_argument("-u", "--username", type=str, metavar="Username", help="Github username")
    parser.add_argument("-t", "--token", type=str, metavar="Token", help="Github public access token")
    parser.add_argument("-g", "--git", type=bool, metavar="True/False", help="Whether to download with git or not. False by default since it's dependent on whether or not git is downloaded (and your ssh/gpg key).")
    
    args = parser.parse_args()
    
    username = args.username
    public_access_token = args.token
    git_check = args.git
    
    print(username)
    print(public_access_token)
    print(git_check)
    
    download_gists(username, public_access_token, git_check)
    
if __name__ == "__main__":
    main()