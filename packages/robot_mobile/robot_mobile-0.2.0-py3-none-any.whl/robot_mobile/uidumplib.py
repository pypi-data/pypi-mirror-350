# coding: utf-8

import re
import uuid
import xml.dom.minidom


def parse_bounds(text):
    m = re.match(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", text)
    if m is None:
        return None
    (lx, ly, rx, ry) = map(int, m.groups())
    return dict(x=lx, y=ly, width=rx - lx, height=ry - ly)


def safe_xmlstr(s):
    return s.replace("$", "-")


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def str2int(v):
    return int(v)


def convstr(v):
    return v


__alias = {
    "class": "_type",
    "resource-id": "resourceId",
    "content-desc": "description",
    "long-clickable": "longClickable",
    "bounds": "rect",
}

__parsers = {
    "_type": safe_xmlstr,  # node className
    # Android
    "rect": parse_bounds,
    "text": convstr,
    "resourceId": convstr,
    "package": convstr,
    "checkable": str2bool,
    "checked": str2bool,
    "scrollable": str2bool,
    "focused": str2bool,
    "clickable": str2bool,
    "selected": str2bool,
    "longClickable": str2bool,
    "focusable": str2bool,
    "password": str2bool,
    "index": int,
    "description": convstr,
    # iOS
    "name": convstr,
    "label": convstr,
    "x": str2int,
    "y": str2int,
    "width": str2int,
    "height": str2int,
    # iOS && Android
    "enabled": str2bool,
}


def _parse_uiautomator_node(node):
    ks = {}
    for key, value in node.attributes.items():
        key = __alias.get(key, key)
        f = __parsers.get(key)
        if value is None:
            ks[key] = None
        elif f:
            ks[key] = f(value)
    if "bounds" in ks:
        lx, ly, rx, ry = map(int, ks.pop("bounds"))
        ks["rect"] = dict(x=lx, y=ly, width=rx - lx, height=ry - ly)
    return ks


def android_hierarchy_to_json(page_xml: bytes):
    """
    Returns:
        JSON object
    """
    dom = xml.dom.minidom.parseString(page_xml)
    root = dom.documentElement

    def travel(node):
        """return current node info"""
        if node.attributes is None:
            return
        json_node = _parse_uiautomator_node(node)
        json_node["_id"] = str(uuid.uuid4())
        if json_node.get("_type") != "android.webkit.WebView" and node.childNodes:
            children = []
            for n in node.childNodes:
                child = travel(n)
                if child:
                    # child["_parent"] = json_node["_id"]
                    children.append(child)
            json_node["children"] = children
        return json_node

    return travel(root)
