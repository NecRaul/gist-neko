from .download import download_gists
import argparse

def main():
    parser = argparse.ArgumentParser(description="Download specified user's all gists at once.")
    parser.add_argument("-u", "--username", type=str, help="Github username")
    parser.add_argument("-t", "--token", type=str, help="Github public access token")
    parser.add_argument("-g", "--git", type=bool, help="Whether to download with git or not. False by default since it's dependent on whether or not git is downloaded (and your ssh/gpg key).")
    
    args = parser.parse_args()
    username = args.username
    public_access_token = args.token
    git_check = args.git
    
    download.download_gists(username, public_access_token, git_check)
    
if __name__ == "__main__":
    main()