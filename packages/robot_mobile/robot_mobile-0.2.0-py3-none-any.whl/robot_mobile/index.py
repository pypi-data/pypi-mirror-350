import json

import uiautomator2
from uidumplib import android_hierarchy_to_json


def click_element():
    d = uiautomator2.connect()
    element = d.xpath(
        "//android.widget.TextView[@resource-id='com.ss.android.article.news:id/dtr' and @text='头条' and @enabled='true']"
    )
    print(element.exists)


if __name__ == "__main__":
    # d = uiautomator2.connect()
    # print(d.info)
    # result = d.dump_hierarchy()
    # json_data = android_hierarchy_to_json(result.encode("utf-8"))
    # print(json.dumps(json_data, indent=4))
    # with open(r"D:\ProgramData\dump.json", "w", encoding="utf-8") as f:
    #     f.write(json.dumps(json_data, indent=4))
    # d.screenshot(r"D:\ProgramData\dump.png")
    click_element()
