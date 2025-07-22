load("@aspect_bazel_lib//lib:transitions.bzl", "platform_transition_filegroup")
load("@npm//:defs.bzl", "npm_link_all_packages", "npm_link_targets")
load("@aspect_rules_js//js:defs.bzl", "js_binary", "js_run_binary")
load("@npm//frontend:vite/package_json.bzl", vite_bin = "bin")
load("@rules_oci//oci:defs.bzl", "oci_image", "oci_push")


npm_link_all_packages(name = "node_modules")

SRCS = [
    "vite.config.js",
    "package.json",
    "index.html",
] + glob(
    [
        "src/**",
        "public/**",
    ],
) + npm_link_targets()

vite_bin.vite(
    name = "dist",
    srcs = SRCS ,
    args = [
        "build",
        "--mode=production",
    ],
    chdir = package_name(),
    out_dirs = ["dist"],
)

vite_bin.vite_binary(
    name = "vite_preview",
    args = ["preview", "--outDir", "dist"],
    chdir = package_name(),
    data = [
        "vite.config.js",
        ":dist",
    ],
)

vite_bin.vite_binary(
    name = "dev_server",
    chdir = package_name(),
    data = SRCS,
    # Under ibazel, let vite hot-reload changed files rather than restart it
    tags = ["ibazel_notify_changes"],
)

# 开发: 使用 bazel run //frontend:dev_server (配合 ibazel) 进行快速迭代开发。
# 构建: 使用 bazel build //frontend:dist 生成生产环境的静态资源。
# 预览: 使用 bazel run //frontend:vite_preview 来本地预览生产构建的效果。

platform(
    name = "x86_64_linux",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:x86_64",
    ],
)

platform(
    name = "aarch64_linux",
    constraint_values = [
        "@platforms//os:linux",
        "@platforms//cpu:aarch64",
    ],
)

genrule(
    name = "nginx_static_tarball",
    srcs = [":dist"], # Vite 构建目标 :dist
    outs = ["app_static_content.tar.gz"], # 输出的 tarball 文件
    cmd = """
        mkdir -p $(RULEDIR)/staging/usr/share/nginx/html
        cp -r $(location :dist)/* $(RULEDIR)/staging/usr/share/nginx/html/
        tar -czf $@ -C $(RULEDIR)/staging .
    """,
    executable = True,
)

oci_image(
    name = "frontend_image",
    # Since js_binary depends on bash we have to bring in a base image that has bash
    base = "@nginx",
    tars = [
        ":nginx_static_tarball",
    ],
    entrypoint = ["nginx", "-g", "daemon off;"],
    visibility = ["//visibility:public"],
)

platform_transition_filegroup(
    name = "platform_image",
    srcs = [":frontend_image"],
    target_platform = select({
        "@platforms//cpu:arm64": ":aarch64_linux",
        "@platforms//cpu:x86_64": ":x86_64_linux",
    }),
)

oci_push(
    name = "frontend_image_push_dynamic",
    image = ":platform_image",
    remote_tags = ["test"],
    repository = "us-docker.pkg.dev/k8s-dev-437501/purrf",
)
