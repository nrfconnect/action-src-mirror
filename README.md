# action-src-mirror
Checkout, pack, and upload source code to Artifactory

## Versioning

This action follows semantic versioning. You can reference:
- A specific version: `nrfconnect/action-src-mirror@v1.0.0`
- A major version (recommended): `nrfconnect/action-src-mirror@v1`
- The latest code: `nrfconnect/action-src-mirror@main` (not recommended for production)

Example:

```
- name: Sync source to Artifactory
  uses: nrfconnect/action-src-mirror@v1
  with:
    git-ref: ${{ github.ref_name }}
    git-fetch-depth: '0'
    path: 'workspace/nrf'
    west-update-args: '--group-filter=+babblesim'
    artifactory-url: 'https://eu.files.nordicsemi.com/artifactory'
    artifactory-repository: 'ncs-src-mirror'
    artifactory-target-prefix: 'external'
    artifactory-user: ${{ secrets.COM_NORDICSEMI_FILES_USERNAME }}
    artifactory-pass: ${{ secrets.COM_NORDICSEMI_FILES_PASSWORD }}
```