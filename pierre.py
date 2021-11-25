from Instance import Instance
from main import INSTANCE_FILES, parse

if __name__ == '__main__':
    for instance_file in INSTANCE_FILES.values():
        parsed = parse(instance_file)
        instance = Instance(parsed)

        max_site = 0
        for site in parsed['sites']:
            if int(site['id']) > max_site:
                max_site = int(site['id'])

        print(instance.site_count)
        print(max_site)
