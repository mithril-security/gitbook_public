import sys
import re

version = ""
new_version = sys.argv[1]

with open('SUMMARY.md', 'r+') as f:
    lines = f.readlines()
    i = 0
    for i in range(len(lines)):
        match = re.search("\s*\* \[latest: version ([0-9]\.[0-9]\.[0-9])", lines[i])
        if match:
            version = match.group(1)
            if version != new_version:
                lines[i] = lines[i].replace("latest: ", "")
                lines.insert(i, f"  * [latest: version {new_version}](resources/client-api-reference/client-interface-{new_version}.md)\n")
                break
    f.seek(0)
    f.writelines(lines)

if version != new_version:
    with open('resources/client-api-reference/README.md', 'r+') as f:
        lines = f.readlines()
        lines.insert(2, f"{{% content-ref url=\"client-interface-{new_version}.md\" %}}\n[client-interface-{new_version}.md](client-interface-{new_version}.md)\n{{% endcontent-ref %}}\n\n")
        f.seek(0)
        f.writelines(lines)