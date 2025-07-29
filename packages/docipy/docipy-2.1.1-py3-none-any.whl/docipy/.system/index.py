from imports import *


class index:
    ####################################################################################// Load
    def __init__(self, app="", cwd="", args=[]):
        self.app, self.cwd, self.args = app, cwd, args
        # ...
        cli.dev = "-dev" in args
        self.menu = {}
        self.params = {}
        self.menus = ""
        self.blocks = ""
        self.blockers = []
        self.template = cli.read(f"{self.app}/.system/sources/template.html")
        self.lngs = self.__lngs()
        pass

    def __exit__(self):
        # ...
        pass

    ####################################################################################// Main
    def render(self, reset="", cmd=""):  # (-r) - Render docs. Add "-r" to reset menu
        menu = f"{self.cwd}/menu.yaml"
        if reset.strip() == "-r" and cli.isFile(menu):
            os.remove(menu)
            self.menu = self.__menu()

        self.params = self.__config()
        self.menu = self.__menu()
        self.__copyFiles(self.params)

        file = f"{self.cwd}/index.html"
        if not cli.isFile(file):
            return "Invalid index file!"

        self.__render(self.menu)
        self.params["menus"] = self.menus
        self.params["blocks"] = self.blocks

        if "background-image" in self.params and self.params[
            "background-image"
        ].strip() not in ["", "#"]:
            self.params["background-image"] = (
                f'style="background-image: url({self.params["background-image"]});background-size: cover;background-position: center;"'
            )

        parsed = self.__parseTemplate(self.template, self.params)
        cli.write(file, parsed)

        cli.hint("Opening the page ...")
        time.sleep(2)
        webbrowser.open(file)

        return "Documentation rendered successfully"

    def version(self, number="", cmd=""):  # (number) - Raise version or set manually e.g. 1.0.3
        if not cli.isFile(f"{self.cwd}/assets/docipy.json"):
            return "Project not detected!"

        number = number.replace("-dev", "").strip()
        self.params = self.__config()

        if number and not SemVer.valid(number):
            return "Invalid semantic version number!"

        current = cli.value("version", self.params, "0.0.0")
        if number and number == current:
            return f'Version "{number}" is the current version!'

        new = number if number else SemVer.bump(current)
        if not new:
            return "Could not set new version!"

        index = f"{self.cwd}/index.html"
        reserv = f"{self.cwd}/version/{current}.html"
        if not cli.isFile(reserv):
            cli.trace("Reserving version: " + current)
            os.makedirs(os.path.dirname(reserv), exist_ok=True)
            content = (
                cli.read(index)
                .replace("assets/", "../assets/")
                .replace(
                    '<span desc="current-version-number" class="bi bi-chevron-down">',
                    '<span class="old-version-number bi bi-chevron-down">',
                )
            )
            cli.write(reserv, content)

        cli.trace("Updating reserved versionings")
        self.__updateReservedVersionings()

        cli.trace("Upgrading to version: " + new)
        self.params["version"] = new
        cli.write(f"{self.cwd}/assets/docipy.json", json.dumps(self.params))
        self.render()

        return f"Version rendered successfully: " + new

    def reform(self, cmd=""):  # Reform configuration
        if not cli.isFile(f"{self.cwd}/assets/docipy.json"):
            return "Project not detected!"

        self.params = self.__config()
        self.params = self.__config(True)
        self.render()

        return "Configuration updated successfully"

    ####################################################################################// Helpers
    def __updateReservedVersionings(self):
        folder = f"{self.cwd}/version"
        if not cli.isFolder(folder):
            return False

        versions = self.__collectVersions()
        if not versions:
            return False

        for file in os.listdir(folder):
            path = f"{folder}/{file}"
            content = cli.read(path)
            start = "<!-- VERSIONS-START -->"
            end = "<!-- VERSIONS-END -->"
            if start not in content or end not in content:
                continue

            hint = file.replace(".html", "")
            cli.trace("Updating versioning for: " + hint)
            versioning = '<li class="latest-version">Latest</li>' + versions.replace(
                f"<li>v{hint}</li>", ""
            )
            replacement = f"{start}\n{versioning}\n        {end}"
            content = re.sub(
                rf"{start}(.*?){end}", replacement, content, flags=re.DOTALL
            )
            cli.write(path, content)

        return True

    def __collectVersions(self, aslist=False):
        folder = f"{self.cwd}/version"
        if not cli.isFolder(folder):
            return ""

        collect = []
        for version in os.listdir(folder):
            hint = version.replace(".html", "")
            collect.append(f"<li>v{hint}</li>")
        collect.reverse()

        return collect if aslist else "".join(collect)

    def __config(self, rewrite=False):
        file = f"{self.cwd}/assets/docipy.json"
        if not rewrite and cli.isFile(file):
            content = cli.read(file)
            return json.loads(content)

        data = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "docipy-hint": "Build Docs With DociPy",
            "docipy-page": "https://github.com/IG-onGit/DociPy",
        }

        params = self.__params()
        for param in params:
            parts = params[param].split("|")
            hint = parts[0].strip()
            default = ""
            must = False
            if "!" in param:
                must = True
                param = param.replace("!", "")
            if len(parts) > 1:
                default = parts[1].strip()
            data[param] = self.__input(rewrite, param, hint, must, default)
        print()

        os.makedirs(os.path.dirname(file), exist_ok=True)
        cli.write(file, json.dumps(data))

        return data

    def __copyFiles(self, params={}):
        items = self.__copy()
        for item in items:
            path = f"{self.app}/.system/sources/{item}"
            new = f"{self.cwd}/{items[item]}"

            if item[0] == "!":
                path = f"{self.app}/.system/sources/{item[1:]}"
            elif cli.isFile(new):
                continue
            else:
                shutil.copy(path, new)
                continue

            content = cli.read(path)
            parsed = self.__parseTemplate(content, params)
            cli.write(new, parsed)

    def __input(self, rewrite=False, key="", hint="", must=False, default=""):
        if not rewrite:
            value = cli.input(hint, must).strip()
            return value if value else default

        value = cli.input(hint).strip()
        return value if value else self.params[key]

    def __menu(self):
        file = f"{self.cwd}/menu.yaml"
        if cli.isFile(file):
            content = cli.read(file)
            filtered = self.__filterYaml(content)
            return yaml.safe_load(filtered)

        content = (
            self.__yamlDir(self.cwd)
            .replace("\n\n", "\n")
            .replace("\n\n\n", "\n\n")
            .replace("- $circle ", "- ")
        )

        cli.write(file, content.replace("$", "*"))

        filtered = self.__filterYaml(content)
        return yaml.safe_load(filtered)

    def __filterYaml(self, content):
        filtered = content.replace("*", "$") + "\n"
        for item in re.findall(r"\$(.*?)\n", filtered):
            if not item.strip()[-1] == ":":
                filtered = filtered.replace(f"${item}\n", f"${item}:\n")
                parts = item.split(" ")
                parts.pop(0)
                ref = self.getRef(" ".join(parts))
                self.blockers.append(ref)

        return filtered

    def __yamlDir(self, dir_path):
        def scan(dir_path):
            result = {}
            for item in os.listdir(dir_path):
                ismd = item[-3:] == ".md"
                if not ismd and not os.path.isdir(f"{dir_path}/{item}"):
                    continue
                if re.search(r"[^\w\s\.]", item):
                    cli.error("File name contains special characters: " + item)
                    continue

                if item in [
                    ".git",
                    ".github",
                    ".system",
                    "assets",
                    "version",
                    "README.md",
                ]:
                    continue
                if ismd:
                    item = item[:-3].strip()
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    result[item] = scan(item_path)
                else:
                    if None not in result:
                        result[None] = []
                    result[None].append(item)
            return result

        directory_content = scan(dir_path)

        def dict_to_yaml_format(d, indent_level=0):
            yaml_output = []
            indent = "  " * indent_level
            for key, value in d.items():
                if not value:
                    continue
                if key is None:
                    for item in value:
                        if indent_level == 0:
                            yaml_output.append(f"$caret-right {item}")
                        else:
                            yaml_output.append(f"{indent}- {item}")
                        yaml_output.append("")
                else:
                    if indent_level == 0:
                        yaml_output.append(f"{indent}- $caret-right {key}:")
                    else:
                        yaml_output.append(f"{indent}- {key}:")
                    if isinstance(value, dict):
                        yaml_output.append(dict_to_yaml_format(value, indent_level + 1))
                        yaml_output.append("")
                    else:
                        for item in value:
                            yaml_output.append(f"{indent}  - {item}")
            return "\n".join(yaml_output)

        yaml_content = dict_to_yaml_format(directory_content)
        final = "\n".join(
            [
                line[2:] if line[:2] == "- " else line
                for line in yaml_content.splitlines()
            ]
        )

        return final

    def __parseTemplate(self, content="", params={}):
        params["versions"] = self.__collectVersions()

        for param in params:
            value = params[param]
            if param in ["linkedin", "x"] and value.strip() in ["", "#"]:
                value = '" class="hide'
            content = content.replace("{{" + param + "}}", value)
        return content

    def __parseMarkdown(self, path=""):
        path = os.path.join(self.cwd, path)
        if not cli.isFile(path):
            return "..."

        content = cli.read(path)
        return markdown.markdown(content, extensions=["fenced_code"])

    def __lngs(self):
        folder = f"{self.app}/.system/sources/lng"
        if not cli.isFolder(folder):
            return {}

        collect = {}
        files = os.listdir(folder)
        for file in files:
            content = cli.read(f"{folder}/{file}")
            collect[file.replace(".yaml", "")] = yaml.safe_load(content)

        return collect

    def getRef(self, hint=""):
        for char in hint:
            for lng in self.lngs:
                if char not in self.lngs[lng]:
                    continue
                hint = hint.replace(char, self.lngs[lng][char])

        hint = re.sub(r"[^\w\s]", "_", hint).replace(" ", "_")

        return hint.strip().lower()

    def __render(self, items={}, parent="", folder=""):
        if not items:
            return False

        for item in items:
            if isinstance(item, dict):
                self.__render(item, parent, folder)
                continue
            parts = item.split(" ")
            icon = "bi bi-" + parts[0].replace("$", "").strip()
            parts.pop(0)
            label = " ".join(parts).strip()
            if "$" not in item:
                label = item
                icon = ""
            ref = self.getRef(label)
            hint = f"{parent}-{ref}"
            hfolder = f"{folder}/{label}"
            if hfolder[0] == "/":
                hfolder = hfolder[1:]
            blocked = True
            for blocker in self.blockers:
                if f"{blocker}-" in hint:
                    blocked = False

            multi = (
                item in items
                and isinstance(items, dict)
                and isinstance(items[item], list)
                and len(items[item]) > 0
            )
            chevron = ""
            if multi:
                chevron = '<i class="bi bi-chevron-down"></i>'
            if hint[0] == "-":
                hint = hint[1:]
            if multi:
                self.menus += (
                    f'<p ref="{hint}" class="{hint} {icon}">{label}{chevron}</p>'
                )
                self.menus += f'<ul class="{hint}-docipymenu hide">'
                self.blocks += f'<div class="docipygroup {hint}-docipyblock hide">'
                self.__render(items[item], hint, hfolder)
                self.blocks += "</div>"
                self.menus += "</ul>"
            else:
                content = self.__parseMarkdown(f"{hfolder}.md")
                if hint in self.blockers:
                    self.blocks += f'<div class="docipygroup {hint}-docipyblock hide"><section id="{hint}" class="hide">{content}</section></div>'
                else:
                    self.blocks += (
                        f'<section id="{hint}" class="hide">{content}</section>'
                    )
                self.menus += (
                    f'<a href="#{hint}" class="{hint} {icon}">{label}{chevron}</a>'
                )
        pass

    def __params(self):
        return {
            "!project": "Project",
            "!version": "Version",
            "slogan": "Slogan | ...",
            "description": "Description | ...",
            "keywords": "Keywords",
            "doc-url": "Documentation URL | .",
            "!author": "Author",
            "position": "Position | ...",
            "!email": "Email",
            "linkedin": "LinkedIn | #",
            "x": "X | #",
            "button1-name": "Button 1 Name | Explore",
            "button1-link": "Button 1 Link | #docipy",
            "button2-name": "Button 2 Name | Download",
            "button2-link": "Button 2 Link | #",
            "background-image": "Background Image URL",
            "main-color": "Main Color | #604384",
            "main-dark": "Dark Color | #222222",
            "googletag-script": "Google Tag (script)",
            "copyrighted-meta": "Copyrighted Verification (meta)",
            "copyrighted-badge": "Copyrighted Badge (a, script)",
            # "": "",
        }

    def __copy(self):
        return {
            "author.png": "assets/author.png",
            "bootstrap-icons.woff": "assets/bootstrap-icons.woff",
            "bootstrap-icons.woff2": "assets/bootstrap-icons.woff2",
            "bootstrap.icons.css": "assets/bootstrap.icons.css",
            "!docipy.js": "assets/docipy.js",
            "!docipy.scss": "assets/docipy.css",
            "highlight.js": "assets/highlight.js",
            "logo.ico": "assets/logo.ico",
            "!sitemap.xml": "assets/sitemap.xml",
            "template.html": "index.html",
            "!robots.txt": "robots.txt",
            # "": "",
        }
