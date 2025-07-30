About this kit
==============

This kit contains the Pdftools SDK for Python. The Pdftools SDK is a comprehensive development library that lets developers integrate advanced PDF functionalities into in-house applications. Find more information about this kit in the [Pdftools SDK](https://www.pdf-tools.com/docs/pdf-tools-sdk/) documentation.

By downloading and using this kit, you accept PDF Tools AG's [license agreement](https://www.pdf-tools.com/license-agreement/),
[privacy policy](https://www.pdf-tools.com/privacy-policy/), and allow PDF Tools AG to track your usage data.

## Licensing

This kit requires a license key to leverage its full potential and process documents without a watermark.

Do you need a full product license, a new license key, or an upgrade to your current license, or do you want to ask us anything else? Get in touch with our sales team through the [Contact page](https://www.pdf-tools.com/contact/).

## Technical Support

Do you need technical support or want to report an issue?
Open a ticket through the [support form](https://www.pdf-tools.com/docs/support/).

## Best Practices: Wheel vs. .tar.gz Files

When installing the Pdftools SDK, you come across two types of distribution files: the wheel file (`.whl`) and the source archive (`.tar.gz`). Generally, using the `.whl` file is the preferred way. Each type of file has its own advantages and ideal use cases.

### Wheel File (`.whl`)

The wheel file is a built package format for Python that can be installed quickly and easily. It is a pre-compiled distribution of the Pdftools SDK, which means it does not require compilation during installation.

**When to Use:**
- **Ease of Installation:** If you want a quick and straightforward installation, the wheel file is the best choice. It avoids the need for a build environment and reduces installation time.
- **Compatibility:** Ideal for systems where the wheel file is compatible with your Python environment and operating system.
- **No Build Dependencies:** If you do not have the necessary build tools installed on your system, the wheel file eliminates the need for these dependencies.

**Installation:**

Of the latest version:

```bash
pip install https://pdftools-public-downloads-production.s3.eu-west-1.amazonaws.com/productkits/PDFSDK/latest/pdftools_sdk-latest.whl
```

Of a specific version, respecting semantic versioning:

```bash
pip install https://pdftools-public-downloads-production.s3.eu-west-1.amazonaws.com/productkits/PDFSDK/VERSION/pdftools_sdk-VERSION.whl
```

### Source Archive (`.tar.gz`)

The source archive contains the source code of the Pdftools SDK. It allows you to build the package from source, which can be beneficial in certain scenarios.

**When to Use:**
- **Customization:** If you need to modify the source code or apply patches, the source archive provides the necessary files to do so.
- **Platform-Specific Builds:** Useful for platforms where a pre-compiled wheel file is not available or compatible.
- **Development Environments:** In development environments where building from source is a standard practice to ensure compatibility and optimization with other dependencies.

**Installation:**

Of the latest version:

```bash
pip install https://pdftools-public-downloads-production.s3.eu-west-1.amazonaws.com/productkits/PDFSDK/latest/pdftools_sdk-latest.tar.gz
```

Of a specific version, respecting semantic versioning:

```bash
pip install https://pdftools-public-downloads-production.s3.eu-west-1.amazonaws.com/productkits/PDFSDK/VERSION/pdftools_sdk-VERSION.tar.gz
```

### Summary
- It's the preferred way to use the wheel file (`.whl`). It is used for a quick, hassle-free installation.
- Use the source archive (`.tar.gz`) if you need to customize the package or if a wheel file is not available for your platform.