
load("@aspect_rules_js//js:defs.bzl", "js_binary", "js_run_binary")
load("@npm//:defs.bzl", "npm_link_all_packages")

npm_link_all_packages(name = "node_modules")

package(default_visibility = ["//visibility:public"])

js_binary(
    name = "bin",
    chdir = package_name(),
    data = glob([
        "src/**",
        "vite.config.js",
        "public/**",
        "index.html",
        "package.json",
    ]),
    entry_point = "//frontend:node_modules/vite/bin/vite.js",
)

