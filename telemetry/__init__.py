import pkgutil

package_info = {k: None for k in ["RELEASE", "COMMIT", "VERSION", "NAME"]}

for name in package_info:
    package_info[name] = pkgutil.get_data(__name__, name).strip().decode('utf-8')

def get_nvr():
    return "{0}-{1}-{2}".format(package_info["NAME"],
                                package_info["VERSION"],
                                package_info["RELEASE"])

try:
    import insights
    insights.add_status(package_info["NAME"], get_nvr(), package_info["COMMIT"])
except Exception:
    pass
