from .download import download_gists
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Download specified user's all gists at once")
    parser.add_argument("-u", "--username", type=str, metavar="Username", help="Github username")
    parser.add_argument("-t", "--token", type=str, metavar="Token", help="Github public access token")
    parser.add_argument("-g", "--git", type=bool, help="Whether to download with git or not. False by default since it's dependent on whether or not git is downloaded (and your ssh/gpg key). IF YOU TYPE ANYTHING IN AFTER -g/--git IT WILL BE ACCEPTED AS TRUE.")
    
    args = parser.parse_args()
    
    if args.username:
        username = args.username
    else:
        username = os.getenv("GITHUB_USERNAME")
    
    if args.token:
        token = args.token
    else:
        token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    
    git_check = args.git # false by default/if you don't use the argument
    
    if (not username and not token):
        print("Pass your Github username and public access token with -u and -t respectively.")
    elif (not username):
        print("Pass your Github username with -u.")
    elif (not token):
        print("Pass your Github public access token with -t.")
    else:
        download_gists(username, token, git_check)
    
if __name__ == "__main__":
    main()