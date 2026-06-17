# /release-resource

> Finalize a resource — merge to master in kale-wiki, update registry, optionally generate LinkedIn post.

**Usage:** `/release-resource [slug]`

**Examples:**
- `/release-resource cold-email-deliverability`
- `/release-resource inbox-provisioning`

---

## Step 1: Identify the Resource

Parse `$ARGUMENTS` to get the slug. If empty, check kale-wiki for open resource branches:

```bash
cd ../kale-wiki && git branch -r | grep "origin/resource/"
```

List the branches and ask the user which one to release.

If a slug is provided, verify the branch `resource/[slug]` exists in kale-wiki:

```bash
cd ../kale-wiki && git branch -r | grep "origin/resource/[slug]"
```

## Step 2: Locate the MDX File

Find the resource's MDX file. It could be in any section:

```bash
cd ../kale-wiki && find content -name "[slug].mdx"
```

Read the file to confirm it exists and has content. Note the section (e.g., `knowledge`, `systems`, `playbooks`).

If the file is not found, inform the user and suggest checking the branch or slug.

## Step 3: Final Build Check

Ensure the resource builds cleanly:

```bash
cd ../kale-wiki && git checkout resource/[slug] && npm run build
```

If the build fails, fix errors before proceeding.

## Step 4: LinkedIn Extraction (Optional)

Ask the user: "Generate a LinkedIn post from this resource? (y/n)"

If yes, read `.claude/skills/kale-content/SKILL.md` for the LinkedIn extraction rules, then:

1. Read the finished `../kale-wiki/content/[section]/[slug].mdx`
2. Extract the single most transferable insight
3. Follow the Operator's Diary format:
   - `Operator's Diary #[n]` opening
   - Hook line (concrete, specific)
   - Context/situation → The shift → How it works now
   - Non-obvious takeaway + punchline
   - Soft CTA / series signal
4. Apply all LinkedIn writing rules from the skill:
   - 150-250 words target
   - No emoji, no hashtag spam
   - AI as supporting character, not hero
   - Strip all proprietary detail
5. Save to `resources/[slug]/linkedin.md` in kale-workspace (create the directory if needed)

For the diary number, check existing resources for the latest number used:

```bash
grep -r "Operator's Diary #" resources/*/linkedin.md 2>/dev/null
```

If none found, start at #1. Otherwise increment from the highest.

## Step 5: Update Resource Registry

Read `resources/index.md` in kale-workspace and add an entry for this resource:

```markdown
| [Title](https://wiki.kaleacquisition.com/[section]/[slug]) | Released | wiki.kaleacquisition.com/[section]/[slug] | YYYY-MM-DD |
```

The URL points to the wiki, not a Workers subdomain.

## Step 6: Merge to Master in kale-wiki

If a draft PR exists for `resource/[slug]`, mark it ready and merge via GitHub:

```bash
cd ../kale-wiki && gh pr ready && gh pr merge --merge --no-delete-branch -m "Merge resource/[slug]: [Title]"
```

Then pull locally to stay in sync:

```bash
cd ../kale-wiki && git checkout master && git pull
```

If no PR exists, merge locally and push:

```bash
cd ../kale-wiki && git checkout master && git merge resource/[slug] --no-ff -m "Merge resource/[slug]: [Title]" && git push
```

If there are merge conflicts, inform the user and help resolve them.

Do NOT delete the branch automatically — let the user decide.

## Step 7: Commit Registry Update in kale-workspace

Back in kale-workspace, commit the registry update (and LinkedIn post if generated):

```bash
git add resources/index.md resources/[slug]/
git commit -m "release: [slug] resource (wiki)"
```

## Step 8: Summary

Present the result:

```
## Resource Released: [Title]

| Detail | Value |
|--------|-------|
| URL | https://wiki.kaleacquisition.com/[section]/[slug] |
| Status | Released |
| LinkedIn draft | resources/[slug]/linkedin.md (or "skipped") |
| Registry | Updated in resources/index.md |
| Branch | resource/[slug] merged to master in kale-wiki |

**Next steps:**
- The resource is live at the URL above (deploys in ~1 min)
- Review the LinkedIn draft and post when ready
- Branch `resource/[slug]` can be deleted when no longer needed:
  `cd ../kale-wiki && git branch -d resource/[slug]`
```
