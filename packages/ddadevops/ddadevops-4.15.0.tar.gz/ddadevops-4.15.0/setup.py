#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'ddadevops',
        version = '4.15.0',
        description = 'tools to support builds combining gopass, terraform, dda-pallet, aws & hetzner-cloud',
        long_description = '# dda-devops-build\n\n[![Slack](https://img.shields.io/badge/chat-clojurians-green.svg?style=flat)](https://clojurians.slack.com/messages/#dda-pallet/) | [<img src="https://domaindrivenarchitecture.org/img/delta-chat.svg" width=20 alt="DeltaChat"> chat over e-mail](mailto:buero@meissa-gmbh.de?subject=community-chat) | [<img src="https://meissa.de/images/parts/contact/mastodon36_hue9b2464f10b18e134322af482b9c915e_5501_filter_14705073121015236177.png" width=20 alt="M"> meissa@social.meissa-gmbh.de](https://social.meissa-gmbh.de/@meissa) | [Blog](https://domaindrivenarchitecture.org) | [Website](https://meissa.de)\n\n\ndda-devops-build integrates all the tools we use to work with clouds & provide some nice functions around.\n\nTools we support are\n\n* terraform: for setting up the plain infrastructure around.\n* docker: for creating images\n* c4k: for generating kubernetes manifests\n* provs: for setting up small single-node k3s clusters\n* gopass: for credential management on devops computers\n* cloud providers: hetzner, digitalocean, aws\n\nIn addition we provide a ReleaseMixin for release related tasks like tag / publish & version-bump\n\n```mermaid\nclassDiagram\n    class DevopsBuild {\n        name()\n        build_path()\n        initialize_build_dir()\n    }\n\n    class DevopsTerraformBuild {\n        initialize_build_dir()\n        post_build()\n        read_output_json()\n        plan()\n        plan_fail_on_diff()\n        apply(auto_approve=False)\n        refresh()\n        destroy(auto_approve=False)\n        tf_import(tf_import_name,tf_import_resource)\n    }\n\n    class DevopsImageBuild {\n        initialize_build_dir()\n        image()\n        drun()\n        dockerhub_login()\n        dockerhub_publish()\n        test()\n    }\n\n    class ReleaseMixin {\n        prepare_release()\n        tag_and_push_release()\n    }\n    \n    class ProvsK3sBuild {\n        def update_runtime_config(dns_record)\n        write_provs_config()\n        provs_apply(dry_run=False)\n    }\n\n    class C4kBuild {\n        def update_runtime_config(dns_record)\n        def write_c4k_config()\n        def write_c4k_auth()\n        c4k_apply(dry_run=False)\n    }\n\n    DevopsBuild <|-- DevopsImageBuild\n    DevopsBuild <|-- DevopsTerraformBuild\n    DevopsBuild <|-- ReleaseMixin\n    DevopsBuild <|-- ProvsK3sBuild\n    DevopsBuild <|-- C4kBuild\n\n    link DevopsBuild "dda-devops-build/src/doc/DevopsBuild.md"\n    link DevopsImageBuild "dda-devops-build/src/doc/DevopsImageBuild.md"\n    link DevopsTerraformBuild "dda-devops-build/src/doc/DevopsTerraformBuild.md"\n    link ReleaseMixin "dda-devops-build/src/doc/ReleaseMixin.md"\n    link ProvsK3sBuild "dda-devops-build/src/doc/ProvsK3sBuild.md"\n    link C4kBuild "dda-devops-build/src/doc/C4kBuild.md"\n\n```\n\nPrinciples we follow are:\n\n* Seperate build artefacts from version controlled code\n* Domain Driven Design - in order to stay sustainable\n\n## Example Project\n\nAn example project which is using dda-devops-build can be found at: https://repo.prod.meissa.de/meissa/buildtest\n\n## Installation\n\nEnsure that yout python3 version is at least Python 3.10\n\n```\nsudo apt install python3-pip\npip3 install -r requirements.txt\nexport PATH=$PATH:~/.local/bin\n```\n\n## Example Project\n\nAn example project which is using dda-devops-build can be found at: https://repo.prod.meissa.de/meissa/buildtest\n\n## Example Build\n\nlets assume the following project structure\n\n```\nmy-project\n   | -> my-module\n   |       | -> build.py\n   |       | -> some-terraform.tf\n   | -> an-other-module\n   | -> target  (here will the build happen)\n   |       | -> ...\n```\n\n```python\nfrom pybuilder.core import task, init\nfrom ddadevops import *\n\nname = \'my-project\'\nMODULE = \'my-module\'\nPROJECT_ROOT_PATH = \'..\'\n\n\n@init\ndef initialize(project):\n    project.build_depends_on("ddadevops>=4.0.0-dev")\n\n    config = {\n        "credentials_mapping": [\n            {\n                "gopass_path": environ.get("DIGITALOCEAN_TOKEN_KEY_PATH", None),\n                "name": "do_api_key",\n            },\n            {\n                "gopass_path": environ.get("HETZNER_API_KEY_PATH", None),\n                "name": "hetzner_api_key",\n            },\n        ],\n        "name": name,\n        "module": MODULE,\n        "stage": environ["STAGE"],\n        "project_root_path": PROJECT_ROOT_PATH,\n        "build_types": ["TERRAFORM"],\n        "mixin_types": [],\n        "tf_provider_types": ["DIGITALOCEAN", "HETZNER"],\n        "tf_use_workspace": False,\n        "tf_terraform_semantic_version": "1.4.2",\n        "do_as_backend": True,\n        "do_bucket": "your-bucket",\n    }\n\n    build = DevopsTerraformBuild(project, config)\n    build.initialize_build_dir()\n\n\n@task\ndef plan(project):\n    build = get_devops_build(project)\n    build.plan()\n\n\n@task\ndef apply(project):\n    build = get_devops_build(project)\n    build.apply(True)\n\n\n@task\ndef destroy(project):\n    build = get_devops_build(project)\n    build.destroy(True)\n\n```\n\n## Snapshot & Release\n\n```\npyb dev publish upload\npip3 install --upgrade ddadevops --pre\n\npyb [patch|minor|major]\npip3 install --upgrade ddadevops\n```\n\n## Reference\n\n* [DevopsBuild](./doc/DevopsBuild.md)\n* [DevopsImageBuild](./doc/DevopsImageBuild.md)\n* [DevopsTerraformBuild](./doc/DevopsTerraformBuild.md)\n  * [AwsProvider](doc/DevopsTerraformBuildWithAwsProvider.md)\n  * [DigitaloceanProvider](doc/DevopsTerraformBuildWithDigitaloceanProvider.md)\n  * [HetznerProvider](doc/DevopsTerraformBuildWithHetznerProvider.md)\n* [ReleaseMixin](./doc/ReleaseMixin.md)\n* [ProvsK3sBuild](doc/ProvsK3sBuild.md)\n* [C4kBuild](doc/C4kBuild.md)\n\n\n## Development & mirrors\n\nDevelopment happens at: https://repo.prod.meissa.de/meissa/dda-devops-build\n\nMirrors are:\n\n* https://gitlab.com/domaindrivenarchitecture/dda-devops-build (issues and PR, CI)\n* https://github.com/DomainDrivenArchitecture/dda-devops-build\n\nFor more details about our repository model see: https://repo.prod.meissa.de/meissa/federate-your-repos\n\n## License\n\nCopyright © 2021 meissa GmbH\nLicensed under the [Apache License, Version 2.0](LICENSE) (the "License")\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.10',
            'Operating System :: POSIX :: Linux',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing'
        ],
        keywords = '',

        author = 'meissa GmbH',
        author_email = 'buero@meissa-gmbh.de',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache Software License',

        url = 'https://repo.prod.meissa.de/meissa/dda-devops-build',
        project_urls = {},

        scripts = [],
        packages = [
            '.',
            'ddadevops',
            'ddadevops.application',
            'ddadevops.domain',
            'ddadevops.infrastructure'
        ],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {
            'ddadevops': ['LICENSE', 'src/main/resources/terraform/*', 'src/main/resources/docker/image/resources/*']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.10',
        obsoletes = [],
    )
