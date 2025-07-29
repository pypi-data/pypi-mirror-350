# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from docutils import nodes

from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from sphinx.util import logging

import otc_metadata.services

LOG = logging.getLogger(__name__)


def sort_docs(docs):
    umn = ''
    api_ref = ''
    i = 0
    for doc in docs:
        if doc['type'] == 'umn':
            umn = doc
            docs.pop(i)
        elif doc['type'] == 'api-ref':
            api_ref = doc
            docs.pop(i)
        i += 1

    sorted_docs = docs
    if umn:
        sorted_docs.insert(0, umn)
    if api_ref:
        sorted_docs.insert(1, api_ref)
    return sorted_docs


class service_card(nodes.General, nodes.Element):
    pass


METADATA = otc_metadata.services.Services()


class ServiceCard(Directive):
    node_class = service_card
    option_spec = {
        'service_type': directives.unchanged_required,
        'id': directives.unchanged,
        'api-ref': directives.unchanged,
        'blueprints': directives.unchanged,
        'caf': directives.unchanged,
        'dev': directives.unchanged,
        'image-creation-guide': directives.unchanged,
        'tool-guide': directives.unchanged,
        'mycredential': directives.unchanged,
        'public-images': directives.unchanged,
        'sdk-ref': directives.unchanged,
        'operation-guide': directives.unchanged,
        'operation-guide-lts': directives.unchanged,
        'parallel-file-system': directives.unchanged,
        'permissions-configuration-guide': directives.unchanged,
        'permissions': directives.unchanged,
        'swiftapi': directives.unchanged,
        's3api': directives.unchanged,
        'umn': directives.unchanged,
        'umn2': directives.unchanged,
        'best-practice': directives.unchanged,
        'sqlreference': directives.unchanged,
        'environment': directives.unchanged,
        'cloud_environment': directives.unchanged,
        'guidelines': directives.unchanged,
        '3rd_party_sdk': directives.unchanged,
        'python-sdk': directives.unchanged
    }

    has_content = True

    def run(self):
        node = self.node_class()
        for k in self.option_spec:
            if self.options.get(k):
                node[k] = self.options.get(k)
            elif k == 'environment':
                node[k] = 'public'
            elif k == "cloud_environment":
                node[k] = "eu_de"
            else:
                node[k] = ''

        return [node]


def service_card_html(self, node):
    # This method renders containers per each service of the category with all
    # links as individual list items

    data = ''
    service = METADATA.get_service_with_docs_by_service_type(node['service_type'])
    docs = sort_docs(service['documents'])

    for doc in docs:
        cloud_environment_check = True
        for cloud in doc["cloud_environments"]:
            if cloud["name"] == node["cloud_environment"]:
                if cloud["visibility"] == "hidden":
                    cloud_environment_check = False
                if cloud["visibility"] == "internal" and node["environment"] != "internal":
                    cloud_environment_check = False
        if cloud_environment_check is False:
            continue

        link = ""
        if service["service"]["service_uri"] in doc["link"]:
            link = doc['link'].split("/")[2] + '/'
        else:
            link = doc['link']

        data = '<div class="card item-sbv item-sbv-flex">'
        data += (f'<a href="{link}">')
        data += (
            '<div class="card-body">'
        )
        data += (
            f'<h4>{doc["title"]}</h4>'
        )
        if "link" not in doc:
            continue
        data += (
            f'<p>{node[doc["type"]]}</p>'
        )
        data += '</div></a>'
        try:
            for cloud in doc["cloud_environments"]:
                if cloud["name"] == node["cloud_environment"]:
                    if cloud["pdf_enabled"]:
                        if cloud["pdf_visibility"] == "hidden":
                            print("PDF not enabled anywhere!")
                        elif (cloud["pdf_visibility"] == "internal" and node['environment'] == "internal") or (cloud["pdf_visibility"] == "public"):
                            data += (f'''
                                        <scale-button variant="secondary" class="pdf-button-sbv" href="{node['service_type']}-{doc["type"]}.pdf" target="_blank">
                                        <scale-icon-user-file-pdf-file accessibility-title="pdf-file"></scale-icon-user-file-pdf-file>
                                        <span style="font-weight: normal;">Download PDF</span>
                                        </scale-button>
                                    ''')
        except Exception:
            print("Service " + node['service_type'] + " has not defined pdf_visibility or pdf_enabled!")

        data += '</div>'

        self.body.append(data)

    raise nodes.SkipNode


def service_card_latex(self, node):
    # do nothing
    raise nodes.SkipNode
