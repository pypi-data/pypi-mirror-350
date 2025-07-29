#! /usr/bin/env python3
#
# Copyright (C) 2025 The Authors
# All rights reserved.
#
# This file is part of wbget.
#
# wbget is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation.
#
# wbget is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with wbget. If not, see http://www.gnu.org/licenses/
#
import argparse
import jinja2
import os

from wikibaseintegrator import WikibaseIntegrator
from wikibaseintegrator.datatypes import Item, URL
from wikibaseintegrator.wbi_config import config as wbi_config
from wikibaseintegrator import wbi_login
from wikibaseintegrator import wbi_helpers

from dotenv import load_dotenv

# WikibaseIntegrator object
wb = None

# akamaitechnologies hangs unless it recognises the User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134."

def main():
    parser = argparse.ArgumentParser(description="Get wikibase entity", epilog="example: wbget.py Q1", add_help=True)

    parser.add_argument("-f", "--format", type=str, help="output format: html|raw")
    parser.add_argument("entity", type=str, help="Pn|Qn")
    parser.add_argument("filename", type=str, help="output to file else to stdout", nargs="?")

    args = parser.parse_args()

    e = args.entity.upper()

    if not args.format or args.format == "raw":
        fmt = "raw"
    elif args.format == "html":
        fmt = "html"
    else:
        raise Exception("format must be html or raw")

    if e.startswith("P"):
        p = Pproperty(e)
        if fmt == "html":
            print(Phtml(p))
        else:
            print(p)
    elif e.startswith("Q"):
        q = Qitem(e)
        if fmt == "html":
            print(Qhtml(q))
        else:
            print(q)
    else:
        raise Exception("entity must start with P or Q")

def login():
    global wb
    if wb == None:
        ##################################################################
        # Login to Wikibase
        #
        load_dotenv(os.getcwd() + os.sep + ".env")

        if (os.getenv("WB_URL") == None):
            raise Exception("WB_URL is missing")

        if (os.getenv("WB_USERNAME") == None):
            raise Exception("WB_USERNAME is missing")

        if (os.getenv("WB_PASSWORD") == None):
            raise Exception("WB_PASSWORD is missing")

        wbi_config["DEFAULT_LANGUAGE"] = "en"
        wbi_config["WIKIBASE_URL"] = os.getenv("WB_URL")
        wbi_config["MEDIAWIKI_API_URL"] = os.getenv("WB_URL") + "w/api.php"
        wbi_config["USER_AGENT"] = USER_AGENT

        wb = WikibaseIntegrator(login=wbi_login.Login(
            user=os.getenv("WB_USERNAME"), password=os.getenv("WB_PASSWORD")))

def Pproperty(p):
    login()

    ##################################################################
    # Get Property:Pn
    #
    try:
        e = wb.property.get(p)
    except:
        raise Exception(f"Property:{p} not found")

    ##################################################################
    # property
    #
    res = {}

    res["title"]     = e.title
    res["pageid"]    = e.pageid
    res["lastrevid"] = e.lastrevid
    res["type"]      = e.type
    res["id"]        = e.id
    res["datatype"]  = e.datatype.value
    res["label"]     = e.labels.values["en"].value

    if e.descriptions.values:
        res["description"] = e.descriptions.values["en"].value
    else:
        res["description"] = None

    ##################################################################
    # aliases
    #
    res["aliases"] = []

    if len(e.aliases):
        for alias in e.aliases.aliases["en"]:
            res["aliases"].append(alias.value)

    return res

def Qitem(q):
    login()

    ##################################################################
    # Get Item:Qn
    #
    try:
        e = wb.item.get(q)
    except:
        raise Exception(f"Item:{q} not found")

    ##################################################################
    # item
    #
    res = {}

    res["title"]     = e.title
    res["pageid"]    = e.pageid
    res["lastrevid"] = e.lastrevid
    res["type"]      = e.type
    res["id"]        = e.id
    res["label"]     = e.labels.values["en"].value

    if e.descriptions.values:
        res["description"] = e.descriptions.values["en"].value
    else:
        res["description"] = None

    ##################################################################
    # claims
    #
    res["items"] = {}
    res["urls"]  = {}

    if len(e.claims):
        for claim in e.claims:
            ##################################################################
            # references
            #
            if claim.references:
                # NB a reference is a property referencing an item
                # which inherently has a datatype etc
                raise Exception(f"FIXME: references")

            ##################################################################
            # datatypes
            #
            match claim.mainsnak.datatype:
                case "wikibase-item":
                    res["items"][claim.mainsnak.datavalue['value']['id']] = claim.mainsnak.property_number

                case "url":
                    res["urls"][claim.mainsnak.datavalue['value']] = claim.mainsnak.property_number

                case _:
                    raise Exception(f"FIXME: datatype = {claim.mainsnak.datatype}")

    ##################################################################
    # aliases
    #
    res["aliases"] = []

    if len(e.aliases):
        for alias in e.aliases.aliases["en"]:
            res["aliases"].append(alias.value)

    ##################################################################
    # sitelinks
    #
    if len(e.sitelinks):
        # NB no example available in demo site yet
        raise Exception(f"FIXME: sitelinks")

    return res

def Qhtml(res):

    items = {}
    if len(res["items"]):
        for i in res["items"]:
            j = Pproperty(res["items"][i])
            k = Qitem(i)
            items[i] = { "property": j["label"], "label": k["label"], "description": k["description"] }

    urls = {}
    if len(res["urls"]):
        for i in res["urls"]:
            j = Pproperty(res["urls"][i])
            urls[i] = { "property": j["label"] }

    template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(__file__))
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    template = template_env.get_template("qhtml.html")

    return template.render(res=res,items=items,urls=urls)

def csv(string, separator):
    return '"' + string.replace('"', '""') + '"' + separator

if __name__=="__main__":
    main()

# vim: shiftwidth=4 tabstop=4 softtabstop=4 expandtab
