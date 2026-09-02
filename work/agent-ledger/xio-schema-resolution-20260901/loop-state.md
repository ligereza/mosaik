# XIO schema resolution loop

- Objective: verify that the published XIO schema graph resolves through a standard JSON Schema registry.
- Branch: `LUCIDA`
- Starting commit: `c103712`
- Scope: schema reference resolution and tests only; no transport, host, GUI, GPU, or automatic actions.
- Observed issue: relative refs under URN `$id` values failed with `jsonschema` before instance validation.
- Method change: normalize the XIO graph and its overlay-update dependency to registered URN IDs.
- Evidence: focused overlay/XIO suite `49 passed`; complete suite `116 passed`; all repository schemas parse; XIO result, overlay fixture, and overlay report validate with a local `$id` registry; `git diff --check` clean.
- Published: commits `291fd67`, `ddc819f`, and `1cb63c8` pushed to `origin/LUCIDA`; process check returned none for `C:\IA\VJ`.
- Closure: the XIO and shared overlay contract graphs now resolve through registered URN IDs without network or path-based resolution during a show.
