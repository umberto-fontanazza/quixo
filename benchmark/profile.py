from cProfile import Profile

def main():
    with Profile() as profile:
        for _ in range(1000):
            pass # your method goes here
        profile.print_stats()

if __name__ == '__main__':
    main()