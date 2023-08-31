from .download import download_gists
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Download specified user's all gists at once")
    parser.add_argument("-u", "--username", type=str, metavar="Username", help="Github username")
    parser.add_argument("-t", "--token", type=str, metavar="Token", help="Github public access token")
    parser.add_argument("-e", "--environment", type=bool, help="Whether to use environment variables or not.")
    parser.add_argument("-g", "--git", type=bool, help="Whether to download with git or not. False by default since it's dependent on whether or not git is downloaded (and your ssh/gpg key). IF YOU TYPE ANYTHING IN AFTER -g/--git IT WILL BE ACCEPTED AS TRUE.")
    
    args = parser.parse_args()
    
    if args.environment: # false by default/if you don't use the argument
        username = os.getenv("GITHUB_USERNAME")
        token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    else:
        username = args.username
        token = args.token
    
    git_check = args.git # false by default/if you don't use the argument
    
    if (not username):
        print("Pass your Github username with -u.")
    else:
        download_gists(username, token, git_check)
    
if __name__ == "__main__":
    main()