# This is replaced during release process.
__version_suffix__ = '244'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.31.1"
KUBECTL_SHA512 = {
    "linux": "609df79769237073275c2a3891e6581c9408da47293276fa12d0332fdef0d2f83bcbf2bea7bb64a9f18b1007ec6500af0ea7daabdcb1aca22d33f4f132a09c27",
    "darwin": "f3e63da7a30cdc97eba7b9eff4c7425bdc7855c60ab7a5aa623b26e16aee69d72313b6b8b28753be8d375e22bd9369281cc93db5fd4c907d31d4c209b840046e",
}
STERN_VERSION = "1.30.0"
STERN_SHA256 = {
    "linux": "ea1bf1f1dddf1fd4b9971148582e88c637884ac1592dcba71838a6a42277708b",
    "darwin": "4eaf8f0d60924902a3dda1aaebb573a376137bb830f45703d7a0bd89e884494a",
}
KUBELOGIN_VERSION = "v1.30.1"
KUBELOGIN_SHA256 = {
    "linux": "36297a69b10664003ec8c9ca53fa56c37b72596cc104a9b55e7145542683532b",
    "darwin": "d86daf251d5049bd67aac448892538bbaa74d55b0c3fcd8175f2ef016aeecfd2",
}
ZALANDO_AWS_CLI_VERSION = "0.5.9"
ZALANDO_AWS_CLI_SHA256 = {
    "linux": "885f1633c4882a332b10393232ee3eb6fac81e736e0c07b519acab487bb6dc63",
    "darwin": "908ed91553b6648182de6e67074f431a21a2e79a4ea45c4aa3d7084578fd5931",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
