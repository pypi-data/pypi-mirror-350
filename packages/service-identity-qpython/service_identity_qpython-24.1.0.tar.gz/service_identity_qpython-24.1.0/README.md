This project is a branch of [service-identity](https://pypi.org/project/service-identity/) on [QPython](https://www.qpython.org).

Use this package if:

- you want to **verify** that a [PyCA *cryptography*](https://cryptography.io/) certificate is valid for a certain hostname or IP address,
- or if you use [pyOpenSSL](https://pypi.org/project/pyOpenSSL/) and don’t want to be [**MITM**](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)ed,
- or if you want to **inspect** certificates from either for service IDs.

*service-identity* aspires to give you all the tools you need for verifying whether a certificate is valid for the intended purposes.
In the simplest case, this means *host name verification*.
However, *service-identity* implements [RFC 6125](https://datatracker.ietf.org/doc/html/rfc6125.html) fully.

Also check out [*pem*](https://github.com/hynek/pem) that makes loading certificates from all kinds of PEM-encoded files a breeze!


## Project Information

*service-identity* is released under the [MIT](https://github.com/pyca/service-identity/blob/main/LICENSE) license, its documentation lives at [Read the Docs](https://service-identity.readthedocs.io/), the code on [GitHub](https://github.com/pyca/service-identity), and the latest release on [PyPI](https://pypi.org/project/service-identity/).
