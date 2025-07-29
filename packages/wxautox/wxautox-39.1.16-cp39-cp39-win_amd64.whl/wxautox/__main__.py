import argparse
from .utils.useful import authenticate

def main():
    parser = argparse.ArgumentParser(description="wxauto command line interface")
    parser.add_argument('--auth', '-a', type=str, help='Authenticate with wxauto plus V2')
    args = parser.parse_args()

    if args.auth:
        authenticate(args.auth)

if __name__ == '__main__':
    main()
