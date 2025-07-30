# Suppress Logs Plugin for MkDocs

MkDocs and its plugins often produce many **informational log messages** that, while helpful, can clutter your terminal during site builds and make real issues harder to spot.

This plugin allows you to **silence specific log messages** using customizable wildcard patterns. It's especially useful for suppressing known, non-critical log lines such as:

```
INFO    -  Doc file 'some.md' contains an absolute link '/path', it was left as is.
INFO    -  Doc file 'other.md' contains an unrecognized relative link '../foo', it was left as is.
```

## 💡 Use Case

If you're using plugins like [`mkdocs-webcontext-plugin`](https://github.com/darrelk/mkdocs-webcontext-plugin) to rewrite links or your site intentionally contains absolute or unresolved relative links, this plugin can filter those benign warnings.

## ✅ Features

* Pattern-based filtering of log messages.
* Wildcard support using `{*}` for variable sections.
* Supports multiple loggers (like `mkdocs.structure.pages`, etc.).
* Keeps your terminal output clean and focused.

---

## 📦 Installation

Install from PyPI:

```bash
pip install mkdocs-suppress-logs-plugin
```

Or with Poetry:

```bash
poetry add mkdocs-suppress-logs-plugin
```

---

## ⚙️ Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - suppress_logs:
      patterns:
        - "Doc file '{*}' contains an absolute link '{*}', it was left as is."
        - "Doc file '{*}' contains an unrecognized relative link '{*}', it was left as is. Did you mean '{*}'?"
      loggers:
        - mkdocs.structure.pages
```

### 🔧 Pattern Matching

Use `{*}` as a wildcard in messages you want to suppress.

**Example log line:**

```
INFO    -  Doc file 'guide.md' contains an absolute link '/img.png', it was left as is.
```

**Matching pattern:**

```
Doc file '{*}' contains an absolute link '{*}', it was left as is.
```

This will suppress any message with that general structure, regardless of the exact file or link.

---

## 🧪 Tips

* To find the logger emitting a message, run MkDocs with `--verbose`.
* You can add multiple patterns and logger names.
* Regex is used under the hood, so avoid overly broad wildcards.

---

## 🙏 Thanks

This plugin was inspired by the need for clean terminal outputs during large MkDocs builds and complements:

* [mkdocs-webcontext-plugin](https://github.com/darrelk/mkdocs-webcontext-plugin)

---

## 🗪 License

MIT License – use freely, contribute generously.
