# TASKS

## Task: Release a2a-t-sdk 0.1.3

- Status: Completed
- Goal: Prepare and publish version `0.1.3` of `a2a-t-sdk` from a clean release worktree.

### Subtasks

1. Create a clean release worktree from `origin/main`
   - Status: Completed
2. Add a regression test that pins package version metadata
   - Status: Completed
3. Bump package version metadata to `0.1.3`
   - Status: Completed
4. Run targeted tests and build verification for the release artifact
   - Status: Completed
5. Commit and push the release branch
   - Status: Completed
6. Publish the `0.1.3` package release
   - Status: Completed

## Task: Fix Packaged Prompt Resource Root Resolution In 0.1.3

- Status: Completed
- Goal: Fix installed `0.1.3` clients and servers so packaged prompt resources resolve from the Python data root instead of guessed filesystem parent directories.

### Subtasks

1. Reproduce the installed-path prompt resource root bug in an automated test
   - Status: Completed
2. Fix packaged prompt resource root resolution in runtime loaders
   - Status: Completed
3. Run targeted regression tests for installed-path resource loading
   - Status: Completed
4. Commit and push the bugfix branch
   - Status: Completed
